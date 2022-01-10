#!/usr/bin/env python3
# filetagging.py -- Manage tags on files.
# Copyright (C) 2022 Trevor Last
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""filetagging implementation."""

__version__ = "0.1.0"

import json
from pathlib import Path, PurePath


class TagsFile:
    """Tags file Context Manager.

    ``self.tags`` is a dict containing files and their associated tags.
    """

    def __init__(self, directory: str, create_new: bool=False) -> None:
        """Create a tags file Context Manager for ``directory``.

        ``create_new`` specifies whether a ``FileNotFoundError`` should be
        raised if the tags.json file doesn't already exist (default ``False``).
        """
        self._filepath = Path(directory/"tags.json")
        if self._filepath.exists():
            self.tags = json.loads(self._filepath.read_text(encoding="utf-8"))
        else:
            if create_new:
                self.tags = {}
            else:
                raise FileNotFoundError(
                    f"Missing file '{directory}'")
        self.tags = _validate_tags_data(self.tags)

    def get_tags(self, filename: str) -> set[str]:
        """Get the tags associated with a file.

        ``filename`` should be a file NAME, not a file PATH. Strip the
        directory off first!
        """
        return self.tags[filename]

    def set_tags(self, filename: str, tags: set[str]) -> None:
        """Set the tags associated with a file.

        ``filename`` should be a file NAME, not a file PATH. Strip the
        directory off first!
        """
        self.tags[filename] = set(tags)
        if not self.tags[filename]:
            del self.tags[filename]

    def add_tag(self, filename: str, tag: str) -> None:
        """Add a tag to a file.

        ``filename`` should be a file NAME, not a file PATH. Strip the
        directory off first!
        """
        if filename in self.tags:
            self.tags[filename].add(tag)
        else:
            self.tags[filename] = {tag}

    def remove_tag(self, filename: str, tag: str) -> None:
        """Remove a tag from a file.

        ``filename`` should be a file NAME, not a file PATH. Strip the
        directory off first!
        """
        self.tags[filename].discard(tag)
        if not self.tags[filename]:
            del self.tags[filename]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # save the tagsfile if the tags are not empty
        if self.tags:
            self._filepath.write_text(
                json.dumps(
                    {k:list(v) for k,v in self.tags.items()},
                    indent=4,
                    sort_keys=True),
                encoding="utf-8")
        # if the tags are empty, and the tagsfile exists, delete it
        elif self._filepath.exists():
            self._filepath.unlink()


def _validate_tags_data(data: dict) -> dict[str, set[str]]:
    """Validate and return a formatted JSON dump.

    ``data`` must be of format: ``dict[str, list[str]]``. If it does not match
    this format, a ``TypeError`` will be raised.
    """
    for key,value in data.items():
        if not isinstance(key, str):
            raise TypeError(
                "tags data contains key of non-string type "
                + type(key).__name__)
        if not isinstance(value, list):
            raise TypeError(
                f'"{key}" is of non-list type {type(value).__name__}')
        if not all(isinstance(i, str) for i in value):
            raise TypeError(f'"{key}" list contains non-string elements')
    return {k:set(str(i) for i in v) for k,v in data.items()}


def open_tags(filepath: str, create_new: bool=False) -> TagsFile:
    """Open the tags file associated with ``filepath``.

    ``create_new`` specifies whether a ``FileNotFoundError`` should be raised
    if the tags.json file doesn't already exist (default ``False``).
    """
    path = Path(filepath)
    if path.is_dir():
        return TagsFile(path, create_new=create_new)
    else:
        return TagsFile(path.parent, create_new=create_new)


def ls_tags(filepath: str) -> None:
    """Print the tags attached to the file."""
    with open_tags(filepath) as tags:
        k = PurePath(filepath).name
        for tag in tags.get_tags(k):
            print(tag)


def filter_tags(tag: str, directory: str=".") -> None:
    """Print all files that match the tag.

    ``directory`` is the directory read the tags from. (default is the current
    directory).
    """
    with open_tags(directory) as tags:
        matches = [
            file
            for (file,file_tags) in tags.tags.items()
            if tag in file_tags
        ]
        for match in matches:
            print(match)


def add_tag(tag: str, filepath: str) -> None:
    """Add a tag to the file."""
    with open_tags(filepath, create_new=True) as tags:
        key = PurePath(filepath).name
        tags.add_tag(key, tag)


def rm_tag(tag: str, filepath: str) -> None:
    """Remove a tag from the file."""
    with open_tags(filepath) as tags:
        key = PurePath(filepath).name
        tags.remove_tag(key, tag)


def mv_tagged_file(file: str, destination: str) -> None:
    """Move or rename a tagged file."""
    path1,path2 = PurePath(file), PurePath(destination)
    # rename file
    if path1.parent == path2.parent:
        with open_tags(file) as tagfile:
            key1,key2 = path1.name, path2.name
            tagfile.set_tags(key2, tagfile.get_tags(key1))
            tagfile.set_tags(key1, set())
    # move file
    else:
        with (  open_tags(file) as tf1,
                open_tags(destination, create_new=True) as tf2):
            key1,key2 = path1.name, path2.name
            tf2.set_tags(key2, tf1.get_tags(key1))
            tf1.set_tags(key1, set())
    Path(file).rename(destination)
