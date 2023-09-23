#!/usr/bin/python3
"""fabric config module  manage static web deployment

This module contain
    function:
    do_pack:  bundles and compresses all content of 
            web_static to  version folder
    do_deploy: takes parameter 'archive_path' which is
            location of the archive file
    deploy: that dynamically call do_pack and then deploy the archive
            as required
    do_clean : takes an argument "number" and reduce the number
            of archive to that number
"""
import os
import re
import fabric.api as api
from datetime import datetime
from pathlib import Path

env.hosts = ['34.229.56.92', '54.236.27.183']


def do_pack():
    """Bundles convert contents of web_static directory to tgz
    """
    version_dir = Path('./versions')
    if not version_dir.exists():
        os.mkdir(version_dir)
    now = datetime.now()

    # absolute path to the compressed file
    file_name = version_dir / "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day,
            now.hour, now.minute, now.second)
    try:
        api.local(f"tar -zcvf {file_name.absolute()} -C web_static .")
        return str(file_name.absolute())
    except Exception:
        return None


def do_deploy(archive_path):
    """Deploy archive path to production
    """
    if not Path(archive_path).exists():
        return False
    try:
        file_name = archive_path.split('/')[-1]
        file_name_no_ext = file_name.split('.')[0]
        old_path = '/data/web_static/releases/{}/web_static'.format(
                file_name_no_ext)
        new_path = '/data/web_static/releases/{}'.format(
                file_name_no_ext)
        curr_path = '/data/web_static/current'

        run_locally = os.getenv("run_locally", None)
        if run_locally is None:
            api.local(f'mkdir -p {new_path}')
            api.local(f'tar -zxf {archive_path} -C {new_path}')
            api.local(f'rm -rfR {curr_path}')
            api.local(f'ln -s {new_path} {curr_path}')
            os.environ['run_locally'] = "True"

        api.put(archive_path, '/tmp/')
        api.run(f'mkdir -p {new_path}')
        api.run(f'tar -zxf /tmp/{file_name} -C {new_path}')
        api.run(f'rm /tmp/{file_name}')
        api.run(f'rm -rfR {curr_path}')
        api.run(f'ln -s {new_path} {curr_path}')
        return True
    except Exception:
        return False


def deploy():
    """ Deploy archive dynamically
    """
    archive_path = os.getenv('archive_path', None)
    if archive_path is None:
        archive_path = do_pack()
        os.environ['archive_path'] = archive_path

    if archive_path is None:
        return False
    result = do_deploy(archive_path)
    return result


def do_clean(number=0):
    """Delete all archives except recent num of counts
    """
    number = int(number)
    number = 1 if number <= 1 else number
    release_path = '/data/web_static/releases/'

    to_keep = os.getenv('to_keep', None)

    if to_keep is None:
        versions = [
                re.findall(r'\d+', version)[0] for version in
                os.listdir('./versions')]

        to_keep = '|'.join(sorted(versions)[-number:])

        os.environ['to_keep'] = to_keep

        api.local((
            "find {} -maxdepth 1 -name \"{}\" " +
            "-type d | grep -Ev \"{}\" | xargs rm -rf").format(
            release_path, "web_static*", to_keep))

        api.local((
            "find versions -maxdepth 1 -name" +
            " \"{}\" -type f | grep -Ev \"{}\" | xargs rm -rf").format(
                "web_static*", to_keep))

    # clean up the remote hosts
    api.run((
            "find {} -maxdepth 1 -name \"{}\" " +
            "-type d | grep -Ev \"{}\" | xargs rm -rf").format(
            release_path, "web_static*", to_keep))
