#!/usr/bin/env python3
# Tag.py -- Manage tags on files.
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

import sys
import json
import pathlib
import os


VERSION = "0.1.0"


class TagsFile:
    """Tags file Context Manager."""
    def __init__(self, directory: pathlib.PurePath) -> None:
        """Create a tags Context Manager."""
        self.changed = False
        self.filepath = directory.joinpath("tags.json")
        try:
            with open(self.filepath, mode="r") as file:
                self.tags = json.load(file)
        except FileNotFoundError:
            self.tags = dict()

    def get_tags(self, filename: str) -> list[str]:
        """Get the tags associated with a file."""
        return self.tags[filename]

    def add_tag(self, filename: str, tag: str) -> None:
        """Add a tag to a file."""
        if filename in self.tags:
            if tag not in self.tags[filename]:
                self.tags[filename].append(tag)
        else:
            self.tags[filename] = [tag]
        self.changed = True

    def remove_tag(self, filename: str, tag: str) -> None:
        """Delete a tag from a file."""
        if tag in self.tags[filename]:
            self.tags[filename].remove(tag)
            self.changed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.changed:
            with open(self.filepath, mode="w") as file:
                file.write(json.dumps(self.tags, indent=4))


def open_tags(filepath: str) -> TagsFile:
    """Open the tags file associated with the given file path."""
    return TagsFile(pathlib.PurePath(filepath).parent)



def print_help(long=False) -> None:
    """Print program help information."""
    print(f"Usage: {sys.argv[0]} [OPTIONS] COMMAND")
    if long:
        print(f"")
        print(f"COMMANDS")
        print(f"  ls <file>")
        print(f"  | List the tags associated with a file.")
        print(f"")
        print(f"  filter <tag>")
        print(f"  | List files tagged with a tag.")
        print(f"")
        print(f"  add <tag> <file>")
        print(f"  | Add a tag to a file.")
        print(f"")
        print(f"  rm <tag> <file>")
        print(f"  | Remove a tag from a file.")

def print_version() -> None:
    """Print program version information."""
    print(f"Tag {VERSION}")
    print(f"Copyright (C) 2022 Trevor Last")
    print(f"License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>")
    print(f"This is free software: you are free to change and redistribute it.")
    print(f"There is NO WARRANTY, to the extent permitted by law.")


def ls_tags(filepath: str) -> None:
    """Print the tags attached to the file."""
    with open_tags(filepath) as tags:
        k = pathlib.PurePath(filepath).name
        for tag in tags.get_tags(k):
            print(tag)

def filter_tags(tag: str) -> None:
    """Print all files that match the tag."""
    with open_tags(os.getcwd()) as tags:
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
        key = pathlib.PurePath(filepath).name
        tags.add_tag(key, tag)

def rm_tag(tag: str, filepath: str) -> None:
    """Remove a tag from the file."""
    with open_tags(filepath) as tags:
        key = pathlib.PurePath(filepath).name
        tags.remove_tag(key, tag)


def run_command(command: list[str]) -> None:
    """Execute a tagging command."""
    match command:
        case "ls", filepath:
            ls_tags(filepath)

        case "filter", tag:
            filter_tags(tag)

        case "add", tag, filepath:
            add_tag(tag, filepath)

        case "rm", tag, filepath:
            rm_tag(tag, filepath)

        case unrecognized:
            print(f"""Unrecognized command '{" ".join(unrecognized)}'""")

def main(args: list[str]):
    if not args:
        print_help(long=False)
        exit()
    elif "--help" in args:
        print_help(long=True)
        exit()
    elif "--version" in args:
        print_version()
        exit()
    else:
        run_command(args)


if __name__ == '__main__':
    main(sys.argv[1:])
