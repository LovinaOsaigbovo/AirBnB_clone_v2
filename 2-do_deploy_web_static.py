#!/usr/bin/env python3
"""
Fabric script that distributes an archive to your web servers.
"""
from fabric.api import *
from os import path

env.user = 'ubuntu'
env.hosts = ['54.82.173.1', '54.83.128.241']
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not path.exists(archive_path):
        return False

    filename = path.basename(archive_path)
    name = filename.split('.')[0]
    remote_path = '/tmp/{}'.format(filename)

    put(archive_path, remote_path)
    run('mkdir -p /data/web_static/releases/{}'.format(name))
    run('tar -xzf {} -C /data/web_static/releases/{}/'.format(remote_path, name))
    run('rm {}'.format(remote_path))
    run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(name, name))
    run('rm -rf /data/web_static/releases/{}/web_static'.format(name))
    run('rm -rf /data/web_static/current')
    run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(name))
    
    print("New version deployed!")
    return True
