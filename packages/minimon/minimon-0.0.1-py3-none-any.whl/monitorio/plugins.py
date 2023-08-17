#!/usr/bin/env python3

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
        f"{user} {cpu} {mem} {cmd}"
        for line in lines[1:]
        for elems in (line.split(maxsplit=10),)
        if len(elems) > 10
        for user, cpu, mem, cmd in ((elems[0], float(elems[2]), float(elems[3]), elems[10]),)
        if cpu > 10
    ]
