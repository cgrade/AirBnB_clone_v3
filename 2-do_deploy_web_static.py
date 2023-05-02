#!/usr/bin/python3
from datetime import datetime
from fabric.api import env, local, put, run
from os import path


env.hosts = ['54.224.21.248', '100.25.28.51']


def do_pack():
    """
    Compress web_static folder contents into a tgz archive
    """

    # create the directory if it doesn't exist
    local("mkdir -p versions")

    # create the file name using the current date and time
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(timestamp)

    # compress the contents of web_static and save in versions directory
    local("tar -czvf versions/{} web_static".format(archive_name))

    # return the path of the archive
    return path.join("versions", archive_name)


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """

    if not path.exists(archive_path):
        return False

    # get the file name and directory name from the archive path
    file_name = path.basename(archive_path)
    dir_name = path.splitext(file_name)[0]

    # upload the archive to the /tmp/ directory of the web server
    put(archive_path, "/tmp/{}".format(file_name))

    # create the directory for the new version
    run("mkdir -p /data/web_static/releases/{}/".format(dir_name))

    # extract the contents of the archive into the new directory
    run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file_name, dir_name))

    # delete the archive from the server
    run("rm /tmp/{}".format(file_name))

    # move the contents of web_static into the new directory
    run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(dir_name, dir_name))

    # remove the old web_static directory
    run("rm -rf /data/web_static/releases/{}/web_static".format(dir_name))

    # delete and recreate the symbolic link to the new version
    run("rm -rf /data/web_static/current")
    run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(dir_name))

    return True
