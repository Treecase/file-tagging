#!/usr/bin/env python3
# __main__.py -- Main entry point for filetagging package.
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
"""
Usage: python -m filetagging [OPTIONS]... COMMANDS...

Commands are executed in the order they are specified.

OPTIONS
    -f, --file <file>
    | Execute a series of commands from a file. If the file is given as -, read
    | commands from standard input.

    --help
    | Display this help and exit.

    --version
    | Display version information and exit.

COMMANDS
    ls [<file> | <directory>]
    | List the tags associated with a file or directory. If no path is
    | supplied, list tags in the current directory.

    filter <tag> [directory]
    | List files tagged with a tag.

    add <tag> <file>
    | Add a tag to a file.

    rm <tag> <file>
    | Remove a tag from a file.

    mv <file> <destination>
    | Move or rename a tagged file.
"""

import sys
from inspect import cleandoc
from io import IOBase
from pathlib import Path
from typing import Iterator

from .filetagging import (
    __version__,
    ls_tags,
    filter_tags,
    add_tag,
    rm_tag,
    mv_tagged_file,
)


def print_help(long: bool=False) -> None:
    """Print program help information.

    If ``long`` is ``True``, full usage details will be printed (default
    ``False``).
    """
    shortdoc,longdoc = cleandoc(__doc__).split("\n\n", maxsplit=1)
    print(shortdoc)
    if long:
        print("\n" + longdoc)


def print_version() -> None:
    """Print program version information."""
    print(cleandoc(
    f"""Tag {__version__}
    Copyright (C) 2022 Trevor Last
    License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.
    """))


def parse_quoted(quote_ch: str, iterator: Iterator) -> str:
    """Parse out a quoted string."""
    token = ""
    for char in iterator:
        if char == quote_ch:
            return token
        else:
            token += char
    raise RuntimeError(f"Unmatched {quote_ch}")


def parse_line(batch_data: str) -> list[str]:
    """Parse out a batch file."""
    tokens = []
    token = ""
    iterator = iter(batch_data)
    for char in iterator:
        if char in "\"'":
            if token:
                tokens.append(token)
            token = ""
            tokens.append(parse_quoted(char, iterator))
        elif char.isspace():
            if token:
                tokens.append(token)
            token = ""
        elif char == "\\":
            token += next(iterator)
        else:
            token += char
    if token:
        tokens.append(token)
    return tokens


def run_batchfile(buffer: IOBase) -> None:
    """Run a batchfile."""
    for line in buffer.readlines():
        run_commands(parse_line(line))


def run_interactive() -> None:
    """Run an interactive session."""
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        try:
            run_commands(parse_line(line))
        except Exception as err:
            print(f"ERROR: {err}")


def run_commands(commands: list[str]) -> None:
    """Execute a list of commands."""
    while commands:
        match commands:
            # ls with a path
            case "ls", filepath, *rest:
                commands = rest
                ls_tags(filepath)
            # ls with no path
            case "ls", *rest:
                commands = rest
                ls_tags(".")

            # filter with a directory
            case "filter", tag, directory, *rest if Path(directory).is_dir():
                commands = rest
                filter_tags(tag, directory)
            # filter with no directory
            case "filter", tag, *rest:
                commands = rest
                filter_tags(tag)

            case "add", tag, filepath, *rest:
                commands = rest
                add_tag(tag, filepath)

            case "rm", tag, filepath, *rest:
                commands = rest
                rm_tag(tag, filepath)

            case "mv", file, destination, *rest:
                commands = rest
                mv_tagged_file(file, destination)

            case unrecognized, *rest:
                commands = rest
                raise RuntimeError(f"Unrecognized command '{unrecognized}'")


def handle_argv(argv: list[str]) -> list[str]:
    """Handle argv."""
    unparsed = []
    while argv:
        match argv:
            case ("-f", filepath, *rest) | ("--file", filepath, *rest):
                argv = rest
                if filepath == "-":
                    run_interactive()
                else:
                    with open(filepath, mode="r", encoding="utf-8") as file:
                        run_batchfile(file)

            case "--help", *rest:
                argv = rest
                sys.exit(print_help(long=True))

            case "--version", *rest:
                argv = rest
                sys.exit(print_version())

            case unrecognized, *rest:
                argv = rest
                unparsed.append(unrecognized)
                if unrecognized.startswith("-"):
                    raise RuntimeError(f"Unrecognized option '{unrecognized}'")
    return unparsed


def main(argv: list[str]) -> int:
    """Package main."""
    if not argv:
        return print_help(long=False)

    try:
        run_commands(handle_argv(argv))
    except RuntimeError as err:
        print(err)
        print("Try 'python -m filetagging' for more information.")
        return 1
    except Exception as err:
        print(f"ERROR: {err}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
