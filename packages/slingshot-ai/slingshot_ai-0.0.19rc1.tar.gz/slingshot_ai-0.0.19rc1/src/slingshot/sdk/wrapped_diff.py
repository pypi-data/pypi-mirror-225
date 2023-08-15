"""
Helper classes to wrap a DeepDiff object into a more usable format, allowing for easier conflict resolution.
"""
from __future__ import annotations

import abc
import re
from typing import Any

from deepdiff import DeepDiff
from pydantic import BaseModel


def perform_diff(base_obj: dict[str, Any], new_obj: dict[str, Any]) -> list[DiffItem]:
    diff = DeepDiff(base_obj, new_obj, ignore_order=True)
    result_diff: list[DiffItem] = []
    for key_path in diff.get("dictionary_item_added", []):
        value, path = _key_path_to_path_nodes(new_obj, key_path)
        result_diff.append(DictionaryItemAdded(value=value, path=path))
    for key_path in diff.get("dictionary_item_removed", []):
        value, path = _key_path_to_path_nodes(base_obj, key_path)
        result_diff.append(DictionaryItemRemoved(value=value, path=path))
    for key_path, value in diff.get("iterable_item_added", {}).items():
        value, path = _key_path_to_path_nodes(new_obj, key_path)
        result_diff.append(IterableItemAdded(value=value, path=path))
    for key_path, value in diff.get("iterable_item_removed", {}).items():
        value, path = _key_path_to_path_nodes(base_obj, key_path)
        result_diff.append(IterableItemRemoved(value=value, path=path))
    for key_path, value in diff.get("values_changed", {}).items():
        new_value, path = _key_path_to_path_nodes(new_obj, key_path)
        old_value, _ = _key_path_to_path_nodes(base_obj, key_path)
        result_diff.append(ValueChanged(new_value=new_value, old_value=old_value, path=path))
    for key_path, value in diff.get("type_changes", {}).items():
        new_value, path = _key_path_to_path_nodes(new_obj, key_path)
        old_value, _ = _key_path_to_path_nodes(base_obj, key_path)
        result_diff.append(TypeChanges(new_value=new_value, old_value=old_value, path=path))
    return result_diff


def _key_path_to_path_nodes(dict_obj: dict[str, Any], key_path: str) -> tuple[Any, list[PathNode]]:
    """Returns the value at the given key path, and the path to that value as a list of PathNodes."""
    keys = _parse_keys(key_path)
    path: list[PathNode] = []
    current_walked_obj: Any = dict_obj
    for k in keys:
        if isinstance(k, str):
            path.append(PathNodeKey(key=k))
        elif isinstance(k, int):
            name = _get_name(current_walked_obj[k])
            path.append(PathNodeIndex(index=k, name=name))
        else:
            raise ValueError(f"Unexpected type {type(k)}")
        current_walked_obj = current_walked_obj[k]
    return current_walked_obj, path


def _get_name(obj: Any) -> str:
    """Returns the name of the given resource, or a hash of the resource if it has no name."""
    if isinstance(obj, str):
        # If it's a string, it's value is the name
        return obj
    if isinstance(obj, dict):
        # Name is for most resources (app specs, environments, etc.), path is for mounts
        return obj.get("name", None) or obj.get("id", None) or obj.get("path", None) or str(hash(str(obj)))
    raise ValueError(f"Cannot get name from {obj}, unexpected type {type(obj)}")


def _parse_keys(key_path: str) -> list[str | int]:
    """Parses a key path string into a list of keys."""
    """
    >>> _parse_keys("root['key1']['key2']")
    ['key1', 'key2']
    >>> _parse_keys("root['key1'][0]['key2']")
    ['key1', 0, 'key2']
    """
    return [eval(k) for k in re.findall(r"\[([^]]+)]", key_path)]


class PathNodeKey(BaseModel):
    key: str

    def __str__(self) -> str:
        return self.key

    @property
    def access_key(self) -> str:
        return self.key


class PathNodeIndex(BaseModel):
    index: int
    name: str

    def __str__(self) -> str:
        return self.name

    @property
    def access_key(self) -> str | int:
        return self.index


PathNode = PathNodeKey | PathNodeIndex


class DiffItem(abc.ABC):
    def __init__(self, value: Any, path: list[PathNode]):
        self.value = value
        self.path = path

    @property
    def identifier(self) -> str:
        id_parts = []
        for path_part in self.path:
            id_parts.append(str(path_part))
        return ".".join(id_parts)

    def has_conflict(self, other: DiffItem) -> bool:
        # If the identifiers are the same, there is a conflict if the values are different
        if self.identifier == other.identifier:
            return type(self) != type(other) or self.value != other.value

        # If the identifiers overlap, there must be a conflict because the same value is being changed in both
        if self.identifier.startswith(other.identifier) or other.identifier.startswith(self.identifier):
            return True

        return False

    @abc.abstractmethod
    def apply_in_place(self, root: dict[str, Any] | list[Any]) -> None:
        ...

    def _walk_to_last_path_node(self, root: dict[str, Any] | list[Any]) -> Any:
        current_walked_obj: Any = root
        for path_part in self.path[:-1]:
            current_walked_obj = current_walked_obj[path_part.access_key]
        return current_walked_obj


class DictionaryItemAdded(DiffItem):
    def apply_in_place(self, root: dict[str, Any] | list[Any]) -> None:
        current_walked_obj = self._walk_to_last_path_node(root)
        current_walked_obj[self.path[-1].access_key] = self.value


class DictionaryItemRemoved(DiffItem):
    def apply_in_place(self, root: dict[str, Any] | list[Any]) -> None:
        current_walked_obj = self._walk_to_last_path_node(root)
        del current_walked_obj[self.path[-1].access_key]


class IterableItemAdded(DiffItem):
    def apply_in_place(self, root: dict[str, Any] | list[Any]) -> None:
        current_walked_obj = self._walk_to_last_path_node(root)
        current_walked_obj.append(self.value)


class IterableItemRemoved(DiffItem):
    def apply_in_place(self, root: dict[str, Any] | list[Any]) -> None:
        current_walked_obj = self._walk_to_last_path_node(root)
        del current_walked_obj[self.path[-1].access_key]


class ValueChanged(DiffItem):
    def __init__(self, old_value: Any, new_value: Any, path: list[PathNode]):
        super().__init__(new_value, path)
        self.old_value = old_value

    def apply_in_place(self, root: dict[str, Any] | list[Any]) -> None:
        current_walked_obj = self._walk_to_last_path_node(root)
        current_walked_obj[self.path[-1].access_key] = self.value


class TypeChanges(DiffItem):
    def __init__(self, old_value: Any, new_value: Any, path: list[PathNode]):
        super().__init__(new_value, path)
        self.old_value = old_value

    def apply_in_place(self, root: dict[str, Any] | list[Any]) -> None:
        current_walked_obj = self._walk_to_last_path_node(root)
        current_walked_obj[self.path[-1].access_key] = self.value
