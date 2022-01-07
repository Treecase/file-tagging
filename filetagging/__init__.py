#!/usr/bin/env python3
# __init__.py -- filetagging initialization.
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
Utilities to manage file tags.
"""

from .filetagging import (
    main,
    ls_tags,
    filter_tags,
    add_tag,
    rm_tag,
    open_tags,
    TagsFile,
    __version__
)

__all__ = [
    "main",
    "ls_tags",
    "filter_tags",
    "add_tag",
    "rm_tag",
    "open_tags",
    "TagsFile"
]
__author__ = "Trevor Last"
