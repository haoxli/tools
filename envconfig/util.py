#!/usr/bin/env python

import os
import sys
import subprocess

def make_env(merge_env={}, env=None):
    if env is None:
        env = os.environ
    env = env.copy()
    for key in merge_env.keys():
        env[key] = merge_env[key]
    return env

def run(args, quiet=False, input=None, cwd=None, env=None, merge_env={}):
    args[0] = os.path.normpath(args[0])
    if not quiet:
        print("> %s" % " ".join(args))
    env = make_env(env=env, merge_env=merge_env)
    shell = os.name == "nt"  # Run through shell to make .bat/.cmd files work.
    proc = subprocess.Popen(args, stdin=subprocess.PIPE, shell=shell, cwd=cwd, env=env)
    if input:
        proc.stdin.write(input)
    proc.communicate()
    rc = proc.returncode
    if rc != 0:
        sys.exit(rc)

def get_platform():
    return {
        "linux"  : "linux",
        "linux2" : "linux",
        "linux3" : "linux",
        "win32"  : "windows",
        "cygwin" : "windows",
        "darwin" : "mac"
    }.get(sys.platform, "other")
