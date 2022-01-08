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
filetagging script entry point.
"""

import sys
from functools import partial
from inspect import cleandoc

from .filetagging import ls_tags, filter_tags, add_tag, rm_tag, __version__


def print_help(long: bool=False) -> None:
    """Print program help information.

    Keyword arguments:
    long -- whether to print full usage details (default False)
    """
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
    f"""Tag {__version__}
    Copyright (C) 2022 Trevor Last
    License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.
    """))


def handle_argv(argv: list[str]) -> list[partial]:
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


def main(argv: list[str]) -> int:
    """Package main."""
    if not argv:
        print_help(long=False)
        sys.exit()
    for command in handle_argv(argv):
        command()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
