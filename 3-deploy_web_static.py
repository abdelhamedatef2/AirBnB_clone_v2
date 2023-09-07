#!/usr/bin/python3
"""fab script that deploy compress file """
from fabric.api import *
from datetime import datetime
import os

env.hosts = ["54.236.27.183", "34.229.56.92"]
env.user = "ubuntu"


def do_pack():
    """ func compress static web folder"""
    n = datetime.now()
    t = f"web_static_{n.year}{n.month}{n.day}{n.hour}{n.minute}{n.second}.tgz"
    local("mkdir -p versions")
    with lcd("./versions"):
        res = local(f"tar -czvf {t} ../web_static")
        if res.succeeded:
            return f"versions/{t}"
    return None


def do_deploy(archive_path):
    """func deploy archive file """
    if not os.path.exists(archive_path):
        return False
    res = put(local_path=archive_path, remote_path="/tmp/")
    if res.failed:
        return False
    file_name = archive_path.split("/")[-1]
    remote_path = f"/tmp/{file_name}"
    with cd("/data/web_static/releases/"):
        res = sudo(f"tar -xzvf {remote_path}")
        if res.failed:
            return False
    res = sudo(f"rm {remote_path}")
    if res.failed:
        return False
    res = sudo("rm /data/web_static/current")
    if res.failed:
        return False
    folder_old = "/data/web_static/releases/web_static"
    folder_new = f"/data/web_static/releases/{file_name.split('.')[0]}"
    res = sudo(f"mv {folder_old} {folder_new}")
    if res.failed:
        return False
    res = sudo(f"ln -s {folder_new} /data/web_static/current")
    if res.failed:
        return False
    return True


def deploy():
    """ full deploy with 2 previous func"""
    pack = do_pack()
    if pack is None:
        return False
    res = do_deploy(pack)
    return res
