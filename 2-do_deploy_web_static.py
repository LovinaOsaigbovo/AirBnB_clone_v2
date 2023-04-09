#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
import os.path
from fabric.api import env, put, run, local

env.hosts = ['3.90.83.66', '100.25.205.254']


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not os.path.isfile(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')
        filename = os.path.basename(archive_path)
        dirname = '/data/web_static/releases/' + filename[:-4]
        run('mkdir -p {}'.format(dirname))
        run('tar -xzf /tmp/{} -C {}'.
            format(filename, dirname))
        run('rm /tmp/{}'.format(filename))
        run('mv {}/web_static/* {}/'.format(dirname, dirname))
        run('rm -rf {}/web_static'.format(dirname))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.
            format(dirname))
        return True
    except:
        return False
