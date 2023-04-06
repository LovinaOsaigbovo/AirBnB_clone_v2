#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers,
using the function do_deploy
"""

import os
from fabric.api import *
from fabric.operations import run, put, sudo
from datetime import datetime


env.user = os.environ.get('ubuntu')
env.hosts = [os.environ.get('54.82.173.1'), os.environ.get('54.83.128.241')]
env.key_filename = os.environ.get('~/.ssh/id_rsa')
env.colorize_errors = True


def do_pack():
    """Function to compress the contents of the web_static folder"""
    try:
        time_now = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        file_name = "versions/web_static_{}.tgz".format(time_now)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None


def do_deploy(archive_path):
    """Function to distribute archive to web servers"""
    if not os.path.isfile(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    try:
        put(archive_path, '/tmp/{}'.format(file_name))
        run('mkdir -p /data/web_static/releases/{}'.format(file_name[:-4]))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(file_name, file_name[:-4]))
        run('rm /tmp/{}'.format(file_name))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(file_name[:-4], file_name[:-4]))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(file_name[:-4]))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{} /data/web_static/current'
            .format(file_name[:-4]))
        return True
    except:
        return False

def deploy():
    """Function to run the full deployment process"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    deploy_status = do_deploy(archive_path)
    if deploy_status is False:
        return False
    print("New version deployed!")
    return True


def do_clean(number=0):
    """Function to delete out-of-date archives"""
    if number == 0 or number == 1:
        number = 1
    else:
        number = int(number)

    with cd('/data/web_static/releases'):
        # Delete all unnecessary archives in the /data/web_static/releases folder
        # on both web servers
        run("ls -1t | tail -n +{} | xargs rm -rf".format(number + 1))

    with cd('/usr/local/var/www/'):
        # Delete all unnecessary archives in the /usr/local/var/www/ folder
