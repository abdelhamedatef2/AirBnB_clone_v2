#!/usr/bin/python3
""" fab script """
from datetime import datetime
from fabric.api import local, lcd


def do_pack():
    """ func compres static web folder"""
    n = datetime.now()
    t = f"web_static_{n.year}{n.month}{n.day}{n.hour}{n.minute}{n.second}.tgz"
    local("mkdir -p versions")
    with lcd("./versions"):
        res = local(f"tar -czvf {t} ../web_static")
        if res.succeeded:
            return f"versions/{t}"
    return None
