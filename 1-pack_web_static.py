#!/usr/bin/python3
"""Fabric script to pack web_static into a .tgz archive
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """Pack web_static files into a .tgz archive"""
    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")

    # Create the file name with the current date and time
    now = datetime.now()
    file_name = "web_static_{}.tgz".format(
        now.strftime("%Y%m%d%H%M%S")
    )

    # Pack the web_static files into the archive
    result = local("tar -cvzf versions/{} web_static".format(file_name))

    # Return the path to the archive if the archive was created, otherwise None
    if result.succeeded:
        return "versions/{}".format(file_name)
    else:
        return None
