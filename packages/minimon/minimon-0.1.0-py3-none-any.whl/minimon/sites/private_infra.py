#!/usr/bin/env python3

""" Monitor my private infrastructure
"""

from minimon.builder import Host, Monitor, iterate, process_output, view
from minimon.plugins import parse_df, parse_du

hosts = (
    Host("localhost", ssh_name="root"),
    Host("om-office.de", ssh_name="frans", ssh_port=2222),
    # Host("zentrale", ssh_name="frans"),
    # Host("remarkable", ssh_name="frans"),
    # Host("handy", ssh_name="frans"),
)

with Monitor("Private inf"):

    @view("host", hosts)
    async def local_resources(host):
        state = {}
        async for name, lines in iterate(
            ps=process_output(host, "ps wauxw", "1"),
            df=process_output(host, "df -P", "2"),
        ):
            state[name] = parse_df(lines) if name == "df" else parse_du(lines)
            yield state
