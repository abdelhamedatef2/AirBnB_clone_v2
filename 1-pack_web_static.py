#!/usr/bin/python3
"""fabric config module to manage static web deployment

That module contain func do_pack that bundles and compresses
all content of web_static to  version folder
"""
import os
import fabric.api as api
from datetime import datetime
from pathlib import Path


def do_pack():
    """Bundle convert contents of web_static direct to tgz
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
