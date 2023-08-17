#!/usr/bin/env python3
#            _       _
#  _ __ ___ (_)_ __ (_)_ __ ___   ___  _ __
# | '_ ` _ \| | '_ \| | '_ ` _ \ / _ \| '_ \
# | | | | | | | | | | | | | | | | (_) | | | |
# |_| |_| |_|_|_| |_|_|_| |_| |_|\___/|_| |_|
#
# minimon - a minimal monitor
# Copyright (C) 2023 - Frans Fürst
#
# minimon is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# minimon is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details
# at <http://www.gnu.org/licenses/>.
#

""" Some little helper functions for checks
"""


def parse_df(lines):
    """
    Filesystem     1K-blocks      Used Available Use% Mounted on
    /dev/dm-0      981723644 814736524 117044544  88% /
    """
    return [
        f"{mountpoint} ({device}) {use}"
        for line in lines[1:]
        for elems in (line.split(),)
        if len(elems) > 5
        for mountpoint, device, use in ((elems[5], elems[0], int(elems[4][:-1])),)
        if use > 80
    ]


def parse_du(lines):
    """
    USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    root           1  0.0  0.0 173724  9996 ?        Ss   Aug13   0:04 /usr/lib/systemd/systemd rhgb --switched-root --system --deserialize 31
    """
    return [
        f"{user} {cpu} {mem} {cmd.split(maxsplit=1)[0]}"
        for line in lines[1:]
        for elems in (line.split(maxsplit=10),)
        if len(elems) > 10
        for user, cpu, mem, cmd in ((elems[0], float(elems[2]), float(elems[3]), elems[10]),)
        if cpu > 10
    ]
