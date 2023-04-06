#!/usr/bin/env python3
"""
Script that deploys archive to webservers
"""
from fabric.api import *
import os
from datetime import datetime

env.hosts = ['54.82.173.1', '54.83.128.241']
env.user 'ubuntu'
env.key_filename = '~/.ssh/id_rsa.pub'

def do_pack():
    """generates a tgz archive"""
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        t = datetime.now()
        timestamp = "{}{}{}{}{}{}".format(t.year, t.month, t.day, t.hour, t.minute, t.second)
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except:
        return None

def do_deploy(archive_path):
    """distributes an archive to the two web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        archive_basename = os.path.splitext(archive_filename)[0]
        release_path = "/data/web_static/releases/{}".format(archive_basename)
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(release_path))
        run("sudo tar xzf /tmp/{} -C {} --strip-components=1".format(archive_filename, release_path))
        run("sudo rm /tmp/{}".format(archive_filename))
        run("sudo mv {}/web_static/* {}/".format(release_path, release_path))
        run("sudo rm -rf {}/web_static".format(release_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(release_path))
        return True
    except:
        return False

def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
