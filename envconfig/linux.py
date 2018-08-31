#!/usr/bin/env python

import os
from util import run

apt_conf = "/etc/apt/apt.conf"
bash_conf = os.path.join(os.environ['HOME'], ".bashrc")

def is_configured(config_file, config_str):
    if not os.path.exists(config_file):
        return False
    with open(config_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if config_str in line:
                return True
    return False

def set_apt_proxy(proxy, port):
    print("# Start set apt proxy")
    if is_configured(apt_conf, "Acquire::http::proxy"):
        print("apt proxy exists")
        return

    with open(apt_conf, "a+") as f:
        f.write('# apt proxy\n')
        f.write('Acquire::http::proxy "http://%s:%s";\n' % (proxy, port))
        f.write('Acquire::https::proxy "http://%s:%s";\n' % (proxy, port))
        f.write('Acquire::ftp::proxy "ftp://%s:%s";\n' % (proxy, port))
        print("apt proxy set successfully")

def set_bash_proxy(proxy, port):
    print("# Start set bash proxy")
    if is_configured(bash_conf, "export http_proxy"):
        print("http proxy exists")
        return

    with open(bash_conf, "a+") as f:
        f.write('\n# proxy\n')
        f.write('export http_proxy="http://%s:%s";\n' % (proxy, port))
        f.write('export https_proxy="http://%s:%s";\n' % (proxy, port))
        print("bash proxy set successfully")

def apt_lock_remove():
    locks = [
        "/var/lib/dpkg/lock",
        "/var/lib/apt/lists/lock",
        "/var/cache/apt/archives/lock"
    ]
    for lock in locks:
        if os.path.exists(lock):
            os.remove(lock)

def apt_install(apt_list):
    apt_lock_remove()
    run(["apt", "update"])
    run(["apt", "upgrade"], input=b"yes")
    for apt in apt_list:
        run(["apt", "install", apt], input=b"y")

def git_config(author, email):
    # author info
    run(["git", "config", "--global", "user.name", author])
    run(["git", "config", "--global", "user.email", email])
    # text editor
    run(["git", "config", "--global", "core.editor", "vim"])
    # CRLF to LF in end of line
    run(["git", "config", "--global", "core.safecrlf", "true"])
    run(["git", "config", "--global", "core.autocrlf", "input"])

def existed_command(cmd):
    try:
        run([cmd, "--version"])
        return True
    except Exception:
        return False

def config(config_data):
    if "proxy" in config_data and "port" in config_data:
        set_apt_proxy(config_data["proxy"], config_data["port"])
        set_bash_proxy(config_data["proxy"], config_data["port"])
    if "apt_lists" in config_data:
        apt_install(config_data["apt_lists"])
    if existed_command("git"):
        git_config(config_data["author"], config_data["email"])
