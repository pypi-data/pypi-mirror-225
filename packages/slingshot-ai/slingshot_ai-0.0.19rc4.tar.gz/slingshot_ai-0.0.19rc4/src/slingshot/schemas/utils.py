import re
import typing


def has_path_ending_in_filename(path: str) -> bool:
    """
    Checks if the given path string ends with a pattern that looks like a file extension,
    i.e., a sequence of characters that are neither dots nor slashes, followed by a dot,
    and then followed by characters that are neither dots nor slashes until the end of the string.

    Args:
        path (str): The path string to be checked.

    Returns:
        bool: True if the pattern is found, False otherwise.

    Examples:
        >>> has_path_ending_in_filename('file.txt')
        True
        >>> has_path_ending_in_filename('/path/to/file.jpg')
        True
        >>> has_path_ending_in_filename('/path.with.dots/to/file')
        False
        >>> has_path_ending_in_filename('/path.with.dots/...file')
        False
        >>> has_path_ending_in_filename('/path.with.dots/file...')
        False
    """
    return re.search(r'[^./]+\.[^./]+$', path) is not None


def strip_keys_with_none_values(dict: dict[str, typing.Any]) -> dict[str, typing.Any]:
    """
    Strips all keys with None values from the given dictionary. We require this as the remote
    sometimes contain "flat" types, e.g. for the MountSpec type with all properties as optinal,
    whereas the client schema uses specific subclasses, each of which has its own schema for
    validation. By stripping out keys set to None, we avoid triggering complaints about extra
    keys which otherwise would fail the validation.

    Args:
        dict (dict[str, Any]): The dictionary to be stripped.

    Returns:
        dict[str, Any]: The stripped dictionary.

    Examples:
        >>> strip_keys_with_none_values({'a': 1, 'b': None, 'c': 2})
        {'a': 1, 'c': 2}
    """
    return {k: v for k, v in dict.items() if v is not None}


if __name__ == "__main__":
    import doctest

    doctest.testmod()
