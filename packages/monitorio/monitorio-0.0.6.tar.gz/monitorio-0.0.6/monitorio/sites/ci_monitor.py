#!/usr/bin/env python3

""" Monitor Checkmk CI

local
 - diskspace / cpu

remote: fra / win / nexus / ci / tstbuild / review
 - diskspace / cpu

fra
 - docker
   - total cpu / ram
   - number of containers
   - per container
       - start / stop
       - cpu / ram
       - volumes
       - associated jenkins job
       -
   - number of images
   - number of volumes

jenkins
   - job tree
   - warning about certain job results

nexus

actions
 - rebuild
 - kill/delete containers/volumes/tags/images
 - open/close branches

"""

from monitorio.builder import Host, Monitor, iterate, process_output, view
from monitorio.plugins import parse_df, parse_du

hosts = (
    Host("localhost", ssh_name="root"),
    Host("build-fra-001", ssh_name="root"),
    Host("build-fra-002", ssh_name="root"),
    Host("build-fra-003", ssh_name="root"),
    Host("ci", ssh_name="root"),
    Host("review", ssh_name="root"),
    Host("artifacts", ssh_name="root"),
    Host("bazel-cache", ssh_name="root"),
    Host("tstbuilds-artifacts", ssh_name="root"),
    Host("devpi", ssh_name="root"),
)

with Monitor("ci_dashboard"):

    @view("host", hosts)
    async def local_resources(host):
        state = {}
        async for name, lines in iterate(
            ps=process_output(host, "ps wauxw", "5"),
            df=process_output(host, "df -P", "60"),
        ):
            state[name] = parse_df(lines) if name == "df" else parse_du(lines)
            yield state
