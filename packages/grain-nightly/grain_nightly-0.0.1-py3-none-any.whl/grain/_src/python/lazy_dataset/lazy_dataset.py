# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""LazyDataset base classes.

There are 3 main classes:
- `LazyMapDataset` define a dataset that supports efficient random access. It
  has 3 important properties:
  - `__len__()` returns the length of a single epoch over the dataset.
  - `__getitem__()` will return the element at any given (positive) index. The
    "true" length of a `LazyMapDataset` is infinite. Many implementations will
    simply loop but exceptions exists (e.g. `ShuffleLazyMapDataset` will loop
    with a different order).
  - The dataset is lazy and individual elements are only created when calling
    `__getitem__()`. Most `LazyMapDatasets`s are statements and will not hold
    elements.
- `LazyIterDataset` defines a dataset that does not support efficient random
  access. It can still be iterated over. A `LazyMapDataset` can be turned into
  a `LazyIterDataset` but going from `LazyIterDataset` to `LazyMapDataset` might
  be as expensive as materializing the whole dataset.
  A `LazyIterDataset` can have known, unknown or infinite length.
- `LazyDatasetIterator` defines a stateful iterator over `LazyIterDataset`. The
  state of the iterator can be saved and restored.

Using the interfaces defined in `collections.abc` you can think of
LazyMapDataset as (infinite) Sequence, LazyIterDataset as Iterable and
LazyDatasetIterator as Iterator.
"""
from __future__ import annotations

import abc
import collections
from collections.abc import Iterable, Iterator, Sequence
import dataclasses
import functools
from typing import Any, Callable, Optional, TypeVar

from concurrent import futures
from grain._src.core import sharding


T = TypeVar("T")
_MAX_PREFETCH_THREADS = 1000


class LazyMapDataset(Sequence[T], abc.ABC):
  """Abstract base class for all LazyMapDataset classes."""

  _functions: dict[str, Callable[[LazyMapDataset], Any]] = {}

  @property
  @abc.abstractmethod
  def sparse(self) -> bool:
    """Returns True if this dataset can contain None elements."""

  @abc.abstractmethod
  def __len__(self) -> int:
    """Returns the length of this dataset."""

  @abc.abstractmethod
  def __getitem__(self, index: int) -> Optional[T]:
    """Returns the element for the index or None if missing."""

  @classmethod
  def register_function(
      cls, name: str, function: Callable[[LazyMapDataset], Any]
  ):
    if name in cls._functions:
      raise ValueError(
          f"Cannot register {function} as dataset function '{name}' since it's"
          " already taken by {cls._functions[name]}."
      )
    cls._functions[name] = function

  def __getattr__(self, attribute_name: str):
    if attribute_name in LazyMapDataset._functions:
      return functools.partial(LazyMapDataset._functions[attribute_name], self)
    raise AttributeError(
        f"'{self.__class__.__name__}' object has no attribute"
        f" '{attribute_name} :("
    )

  def __iter__(self) -> LazyDatasetIterator[T]:
    return self.to_iter_dataset().__iter__()

  def to_iter_dataset(self) -> LazyIterDataset[T]:
    """Syntactic sugar to construct a LazyIterDataset."""
    return PrefetchLazyIterDataset(self, prefetch=128)


class LazyIterDataset(Iterable[T], abc.ABC):
  """Abstract base class for all LazyIterDataset classes."""

  _functions: dict[str, Callable[[LazyIterDataset], Any]] = {}

  @abc.abstractmethod
  def __iter__(self) -> LazyDatasetIterator[T]:
    """Returns an iterator for this dataset."""

  @classmethod
  def register_function(
      cls, name: str, function: Callable[[LazyIterDataset], Any]
  ):
    if name in cls._functions:
      raise ValueError(
          f"Cannot register {function} as dataset function '{name}' since it's"
          " already taken by {cls._functions[name]}."
      )
    cls._functions[name] = function

  def __getattr__(self, attribute_name: str):
    if attribute_name in LazyIterDataset._functions:
      return functools.partial(LazyIterDataset._functions[attribute_name], self)
    raise AttributeError(
        f"'{self.__class__.__name__}' object has no attribute"
        f" '{attribute_name} :("
    )


def lazy_map_dataset_function(name: str):
  def _fn(cls):
    LazyMapDataset.register_function(name=name, function=cls)
    return cls

  return _fn


def lazy_iter_dataset_function(name: str):
  def _fn(cls):
    LazyIterDataset.register_function(name=name, function=cls)
    return cls

  return _fn


class LazyDatasetIterator(Iterator[T], abc.ABC):
  """Abstract base class for all LazyIterDataset iterator classes."""

  def __iter__(self) -> LazyDatasetIterator[T]:
    return self

  # __next__ abstract method since we inherit from Iterator[T].

  @abc.abstractmethod
  def get_state(self) -> dict[str, Any]:
    """Returns the current state of the iterator."""

  @abc.abstractmethod
  def set_state(self, state: dict[str, Any]):
    """Sets the current state of the iterator."""


@lazy_map_dataset_function("prefetch")
@dataclasses.dataclass(frozen=True)
class PrefetchLazyIterDataset(LazyIterDataset[T]):
  """Iterable dataset that uses a thread pool for prefetching."""

  parent: LazyMapDataset[T]
  prefetch: int

  def __iter__(self) -> LazyDatasetIterator[T]:
    return PrefetchLazyDatasetIterator(self.parent, self.prefetch)


class PrefetchLazyDatasetIterator(LazyDatasetIterator[T]):
  """Iterator that performs prefetching using a thread pool."""

  def __init__(self, dataset: LazyMapDataset[T], prefetch: int):
    super().__init__()
    self._dataset = dataset
    self._dataset_length = len(dataset)
    self._next_index = 0
    self._prefetch = prefetch
    if self._prefetch > 0:
      self._buffer = None
      self._executor = futures.ThreadPoolExecutor(
          max_workers=_MAX_PREFETCH_THREADS
      )

  def __next__(self) -> T:
    # We loop here to skip all None elements (in case the underlying dataset
    # is sparse).
    while True:
      if self._next_index == self._dataset_length:
        break
      if self._prefetch > 0:
        if not self._buffer:
          indices = range(
              self._next_index,
              min(self._next_index + self._prefetch, self._dataset_length),
          )
          self._buffer = collections.deque(
              self._executor.submit(self._dataset.__getitem__, i)
              for i in indices
          )
        element = self._buffer.popleft()
        if self._next_index + self._prefetch < self._dataset_length:
          self._buffer.append(
              self._executor.submit(
                  self._dataset.__getitem__, self._next_index + self._prefetch
              )
          )
        element = element.result()
      else:
        element = self._dataset[self._next_index]
      self._next_index += 1
      if element is not None:
        return element
    raise StopIteration

  def get_state(self):
    return {"next_index": self._next_index}

  def set_state(self, state):
    self._next_index = state["next_index"]
    if self._prefetch > 0:
      self._buffer = None


@dataclasses.dataclass(frozen=False)
class RangeLazyMapDataset(LazyMapDataset[int]):
  """Range data source, similar to python range() function."""

  start: int
  stop: int | None = None
  step: int = 1

  def __post_init__(self):
    if self.stop is None:
      self.stop = self.start
      self.start = 0

  @property
  def sparse(self) -> bool:
    return False

  @functools.cached_property
  def _length(self) -> int:
    return len(range(self.start, self.stop, self.step))

  def __len__(self) -> int:
    return self._length

  def __getitem__(self, index: int) -> int:
    return self.start + (index % self._length) * self.step

  def to_iter_dataset(self) -> LazyIterDataset[int]:
    """Syntactic sugar to construct a LazyIterDataset."""
    return PrefetchLazyIterDataset(self, prefetch=0)


# Deprecated: This class should not be used for new code. It's used to
# implement the stateless Sampler.
# For new code the PrefetchLazyMapDataset should be used to implement sharding.
class ShardLazyDataset(LazyMapDataset[T]):
  """Shards the parent into consecutive pieces."""

  def __init__(
      self, parent: LazyMapDataset[T], shard_options: sharding.ShardOptions
  ):
    super().__init__()
    self._parent = parent
    self._start, self._end = sharding.even_split(
        len(self._parent), shard_options
    )

  @property
  def sparse(self) -> bool:
    return self._parent.sparse

  def __len__(self) -> int:
    return self._end - self._start

  def __getitem__(self, index: int) -> Optional[T]:
    epoch = index // len(self)
    index_in_epoch = index % len(self)
    index = epoch * len(self._parent) + index_in_epoch + self._start
    return self._parent[index]
