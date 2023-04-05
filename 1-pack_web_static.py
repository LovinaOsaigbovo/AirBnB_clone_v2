#!/usr/bin/python3
"""Fabric script that generates a .tgz archive
from a web_static folder"""

from fabric.api import local, env
from datetime import datetime
import os

env.user = 'ubuntu'
env.hosts = ['34.74.100.166', '34.139.37.135']

def do_pack():
    """This function compresses and archives files"""
    try:
        if not os.path.exists('versions'):
            os.makedirs('versions')
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = 'versions/web_static_{}.tgz'.format(now)
        local('tar -cvzf {} web_static'.format(archive_path))
        return archive_path
    except:
        return None
