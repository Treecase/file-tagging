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

__version__ = "0.1.0"

import json
from os import getcwd
from pathlib import PurePath


class TagsFile:
    """Tags file Context Manager."""
    def __init__(self, directory: PurePath) -> None:
        """Create a tags Context Manager."""
        self.changed = False
        self.filepath = directory.joinpath("tags.json")
        try:
            with open(self.filepath, mode="r", encoding="utf-8") as file:
                self.tags = json.load(file)
        except FileNotFoundError:
            self.tags = {}

    def get_tags(self, filename: str) -> list[str]:
        """Get the tags associated with a file.

        filename should be a file NAME, not a file PATH. Strip the directory
        off first!
        """
        return self.tags[filename]

    def add_tag(self, filename: str, tag: str) -> None:
        """Add a tag to a file.

        filename should be a file NAME, not a file PATH. Strip the directory
        off first!
        """
        if filename in self.tags:
            if tag not in self.tags[filename]:
                self.tags[filename].append(tag)
        else:
            self.tags[filename] = [tag]
        self.changed = True

    def remove_tag(self, filename: str, tag: str) -> None:
        """Delete a tag from a file.

        filename should be a file NAME, not a file PATH. Strip the directory
        off first!
        """
        if tag in self.tags[filename]:
            self.tags[filename].remove(tag)
            self.changed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.changed:
            with open(self.filepath, mode="w", encoding="utf-8") as file:
                file.write(json.dumps(self.tags, indent=4))


def open_tags(filepath: str) -> TagsFile:
    """Open the tags file associated with the given filepath."""
    return TagsFile(PurePath(filepath).parent)


def ls_tags(filepath: str) -> None:
    """Print the tags attached to the file."""
    with open_tags(filepath) as tags:
        k = PurePath(filepath).name
        for tag in tags.get_tags(k):
            print(tag)


def filter_tags(tag: str) -> None:
    """Print all files that match the tag."""
    with open_tags(getcwd()) as tags:
        matches = [
            file
            for (file,file_tags) in tags.tags.items()
            if tag in file_tags
            ]
        for match in matches:
            print(match)


def add_tag(tag: str, filepath: str) -> None:
    """Add a tag to the file."""
    with open_tags(filepath) as tags:
        key = PurePath(filepath).name
        tags.add_tag(key, tag)


def rm_tag(tag: str, filepath: str) -> None:
    """Remove a tag from the file."""
    with open_tags(filepath) as tags:
        key = PurePath(filepath).name
        tags.remove_tag(key, tag)
