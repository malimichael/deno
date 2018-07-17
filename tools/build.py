#!/usr/bin/env python
import os
import sys
from os.path import join
from util import run
import distutils.spawn

ccache_path = distutils.spawn.find_executable("ccache")
gn_args = []
if ccache_path:
    gn_args += ["cc_wrapper=\"%s\"" % ccache_path]

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
os.chdir(root_path)
third_party_path = join(root_path, "third_party")
depot_tools_path = join(third_party_path, "depot_tools")
gn_path = join(depot_tools_path, "gn")
ninja_path = join(depot_tools_path, "ninja")
run(["python", "tools/run_hooks.py"], quiet=True)

# TODO(ry) parse argv for --mode and --out-dir.
mode = "default"
out_path = join("out", mode)
target = sys.argv[1] if len(sys.argv) > 1 else "deno"

if not os.path.isdir(out_path):
    gn_cmd = [gn_path, "gen", out_path]
    if len(gn_args) > 0:
        gn_cmd += ["--args=%s" % " ".join(gn_args)]
    run(gn_cmd, quiet=True)
# Travis hangs without -j2 argument to ninja.
run([ninja_path, "-C", out_path, target], quiet=True)
