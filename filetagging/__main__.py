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
    ls <file>
    | List the tags associated with a file.

    filter <tag>
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

def parse_line(batch_data: str) -> None:
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
    handle_argv(tokens)


def run_batchfile(buffer) -> None:
    """Run a batchfile."""
    while True:
        line = buffer.readline()
        if line == "":
            break
        parse_line(line)


def handle_argv(argv: list[str]) -> None:
    """Handle argv."""
    while argv:
        match argv:
            case ("-f", filepath, *rest) | ("--file", filepath, *rest):
                argv = rest
                if filepath == "-":
                    run_batchfile(sys.stdin)
                else:
                    with open(filepath, mode="r", encoding="utf-8") as file:
                        run_batchfile(file)

            case "--help", *rest:
                argv = rest
                sys.exit(print_help(long=True))

            case "--version", *rest:
                argv = rest
                sys.exit(print_version())

            case "ls", filepath, *rest:
                argv = rest
                ls_tags(filepath)

            case "filter", tag, *rest:
                if rest and Path(rest[0]).exists():
                    argv = rest[1:]
                    filter_tags(tag, rest[0])
                else:
                    argv = rest
                    filter_tags(tag)

            case "add", tag, filepath, *rest:
                argv = rest
                add_tag(tag, filepath)

            case "rm", tag, filepath, *rest:
                argv = rest
                rm_tag(tag, filepath)

            case "mv", file, destination, *rest:
                argv = rest
                mv_tagged_file(file, destination)

            case unrecognized, *rest:
                argv = rest
                print(f"Unrecognized option '{unrecognized}'")
                print("Try 'python -m filetagging' for more information.")
                sys.exit()


def main(argv: list[str]) -> int:
    """Package main."""
    if not argv:
        sys.exit(print_help(long=False))
    handle_argv(argv)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
