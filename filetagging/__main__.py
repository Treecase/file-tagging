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
"""filetagging script entry point."""

import sys
from inspect import cleandoc
from pathlib import Path

from .filetagging import ls_tags, filter_tags, add_tag, rm_tag, __version__


def print_help(long: bool=False) -> None:
    """Print program help information.

    Keyword arguments:
    long -- whether to print full usage details (default False)
    """
    print(f"Usage: {sys.argv[0]} [OPTIONS] COMMANDS")
    if long:
        print("")
        print(cleandoc(
        """
        OPTIONS
          --help
          | Display this help information.

          --version
          | Display version information.

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
    f"""Tag {__version__}
    Copyright (C) 2022 Trevor Last
    License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.
    """))


def handle_argv(argv: list[str]) -> None:
    """Handle argv and return a list of supplied commands, if any."""
    while argv:
        match argv:
            case "--help", *rest:
                argv = rest
                print_help(long=True)
                sys.exit()

            case "--version", *rest:
                argv = rest
                print_version()
                sys.exit()

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

            case unrecognized, *rest:
                argv = rest
                raise RuntimeError(f"unrecognized option '{unrecognized}'")


def main(argv: list[str]) -> int:
    """Package main."""
    if not argv:
        sys.exit(print_help(long=False))
    handle_argv(argv)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
