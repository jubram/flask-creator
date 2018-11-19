# -*- coding: utf-8 -*-

import sys
import os
import argparse
import shutil
import jinja2
import codecs
import subprocess
import platform
from datetime import datetime

# Globals #

cwd = os.getcwd()
script_dir = os.path.dirname(os.path.realpath(__file__))
template_loader = jinja2.FileSystemLoader(searchpath=os.path.join(script_dir, 'templates'))
template_env = jinja2.Environment(loader=template_loader)

def get_arguments(argv):
    parser = argparse.ArgumentParser(description='Scaffold a Flask Skeleton')
    parser.add_argument('appname', help='The application name')
    parser.add_argument('-p', '--path', help='The full path to the project directory')
    parser.add_argument('-s', '--skeleton', help='The skeleton directory to use')
    parser.add_argument('-l', '--list-skeletons', help='List the skeletons available', action='store_true', dest='list')
    parser.add_argument('-v', '--virtualenv', help='Create a new Virtual Environment', action='store_true')
    parser.add_argument('-g', '--git', help='Initialize GIT for the project', action='store_true')
    parser.add_argument('-d', '--database-name', help='The database name for the project', dest='db_name')
    return parser.parse_args()

def list_skeletons():
    template = template_env.get_template('skeletons.jinja2')
    skeletons = os.listdir(os.path.join(script_dir, 'skeleton'))
    print(template.render(skeletons=skeletons))


def write_log(step, error):
    with open('{}_error.log'.format(step), 'a') as fd:
        now = datetime.now()
        fd.write('{} -- {}\n'.format(now, error.decode('utf-8')))
        print('An error occurred with {}'.format(step))
        sys.exit(2)

def create_virtual_env(fullpath):
    output, error = subprocess.Popen(
        ['virtualenv', '-p', 'python3.6', os.path.join(fullpath, 'venv')],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).communicate()
    if error:
        write_log('virtualenv', error)
    venv_bin = os.path.join(fullpath, 'venv/bin')
    output, error = subprocess.Popen(
        [
            os.path.join(venv_bin, 'pip3'),
            'install', '--upgrade', 'pip'
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).communicate()
    if error:
        write_log('pip', error)
    output, error = subprocess.Popen(
        [
            os.path.join(venv_bin, 'pip3'),
            'install', '-r',
            os.path.join(fullpath, 'requirements.txt')
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).communicate()
    if error:
        write_log('pip', error)

def create_git(fullpath):
    # Git init
    output, error = subprocess.Popen(
        ['git', 'init', fullpath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).communicate()
    if error:
        write_log('git', error)
    shutil.copyfile(
        os.path.join(script_dir, 'templates', '.gitignore'),
        os.path.join(fullpath, '.gitignore')
    )

def generate_brief(template_var):
    template = template_env.get_template('brief.jinja2')
    return template.render(template_var)

def main(args):

    # Variables #

    appname = args.appname
    dbname = args.db_name or appname
    if args.path:
        fullpath = args.path
    else:
        fullpath = os.path.join(cwd, appname)
    if args.skeleton:
        skeleton_dir = os.path.join(script_dir, 'skeleton', args.skeleton)
    else:
        skeleton_dir = os.path.join(script_dir, 'skeleton', 'base/')
    srcpath = os.path.join(script_dir, skeleton_dir)

    # Tasks #

    # Copy files and folders
    print('Copying files and folders...')
    print('Source path:\n{}\n'.format(srcpath))
    print('Destination path:\n{}\n'.format(fullpath))

    shutil.copytree(os.path.join(script_dir, skeleton_dir), fullpath)

    # Create config.py
    print('Creating the config file...')
    secret_key = codecs.encode(os.urandom(32), 'hex').decode('utf-8')
    template = template_env.get_template('config.jinja2')
    template_var = {
        'secret_key': secret_key,
        'db_name': dbname
    }
    with open(os.path.join(fullpath, 'config.py'), 'w+') as fd:
        fd.write(template.render(template_var))

    # Create the Virtual Environment
    virtualenv = args.virtualenv
    if virtualenv:
        print('Creating the virtual environment...')
        create_virtual_env(fullpath)

    # Create a GIT init
    if args.git:
        print('Initializing Git...')
        create_git(fullpath)

    template_var = {
        'pyversion': platform.python_version(),
        'appname': appname,
        'virtualenv': args.virtualenv,
        'skeleton': args.skeleton,
        'path': fullpath,
        'git': args.git
    }

    print(generate_brief(template_var))

if __name__ == '__main__':
    arguments = get_arguments(sys.argv)
    if arguments.list:
        list_skeletons()
        sys.exit(0)
    main(arguments)