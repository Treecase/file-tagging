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
from pathlib import PurePath
from os import getcwd
from inspect import cleandoc
from functools import partial


VERSION = "0.1.0"


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
            with open(self.filepath, mode="w", encoding="utf-8") as file:
                file.write(json.dumps(self.tags, indent=4))


def open_tags(filepath: str) -> TagsFile:
    """Open the tags file associated with the given file path."""
    return TagsFile(PurePath(filepath).parent)



def print_help(long=False) -> None:
    """Print program help information."""
    print(f"Usage: {sys.argv[0]} [OPTIONS] COMMAND")
    if long:
        print("")
        print(cleandoc(
        """
        COMMANDS
          ls <file>
          | List the tags associated with a file.

          filter <tag>
          | List files tagged with a tag.

          add <tag> <file>
          | Add a tag to a file.

          rm <tag> <file>
          | Remove a tag from a file.
        """))

def print_version() -> None:
    """Print program version information."""
    print(cleandoc(
    f"""Tag {VERSION}
    Copyright (C) 2022 Trevor Last
    License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.
    """))


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


def handle_argv(argv: list[str]) -> list:
    """Handle argv and return a list of supplied commands, if any."""
    COMMANDS = {
        "ls":ls_tags,
        "filter":filter_tags,
        "add":add_tag,
        "rm":rm_tag,
    }

    commands = []

    cmd: partial = None
    arg_count = -1

    for arg in argv:
        if cmd is not None:
            if len(cmd.args) < arg_count:
                cmd = partial(cmd, arg)
            elif len(cmd.args) == arg_count:
                commands.append(cmd)
                cmd = None
                arg_count = -1
        else:
            match arg:
                case "--help":
                    print_help(long=True)
                    sys.exit()

                case "--version":
                    print_version()
                    sys.exit()

                case unrecognized:
                    if unrecognized in COMMANDS:
                        c = COMMANDS[unrecognized]
                        cmd = partial(c)
                        arg_count = c.__code__.co_argcount
                    else:
                        raise Exception(f"Unrecognized option '{unrecognized}'")

    if cmd is not None:
        commands.append(cmd)
    return commands

def main(args: list[str]):
    if not args:
        print_help(long=False)
        sys.exit()
    commands = handle_argv(args)
    for command in commands:
        command()


if __name__ == '__main__':
    main(sys.argv[1:])
