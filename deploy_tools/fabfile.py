import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run
import os

REPO_URL = 'https://github.com/axdr3/supertodolists.git'

# TODOLATER: change python version from 3.6 to chosen


# deploy()
# You’ll want to update the REPO_URL variable with the URL of your own Git repo on its code-sharing site.
# env.user will contain the username you’re using to log in to the server; env.host will be the address
# of the server we’ve specified at the command line (e.g., superlists.ottg.eu).
# run is the most common Fabric command. It says "run this shell command on the server". The run commands
# in this chapter will replicate many of the commands we did manually in the last two.
# mkdir -p is a useful flavour of mkdir, which is better in two ways: it can create directories several
# levels deep, and it only creates them if necessary. So, mkdir -p /tmp/foo/bar will create the directory
# bar but also its parent directory foo if it needs to. It also won’t complain if bar already exists.
# cd is a fabric context manager that says "run all the following statements inside this working directory".


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()
        _provide_server_config()

# _get_latest_source()
# The end result of this is that we either do a git clone if it’s a
# fresh deploy, or we do a git fetch + git reset --hard if a previous
# version of the code is already there; the equivalent of the git pull
# we used when we did it manually, but with the reset --hard to force overwriting any local changes.


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')

# _update_virtualenv()
# We look inside the virtualenv folder for the pip executable as a way
# of checking whether it already exists.
# Then we use pip install -r like we did earlier.


def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run(f'python3.8 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt')

# _create_or_update_dotenv()
# The append command conditionally adds a line to a file, if that line isn’t already there.
# For the secret key we first manually check whether there’s already an entry in the file…​
# And if not, we use our little one-liner from earlier to generate a new one
# (we can’t rely on the append's conditional logic here because our new key and any potential
# existing one won’t be the same).


def _create_or_update_dotenv():

    run('rm -r .env')
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')
    email_password = os.environ.get('EMAIL_PASSWORD')
    append('.env', f'EMAIL_PASSWORD={email_password}')
    db_pass = os.environ.get('DB_PASS')
    append('.env', f'DB_PASS={db_pass}')
    # run(f'echo {db_pass}')
    run(f"export DB_PASS='{db_pass}'")

# _update_static_files()
# We use the virtualenv version of Python whenever we need to run a Django manage.py command,
# to make sure we get the virtualenv version of Django, not the system one.


def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput')

# update_database
# The --noinput removes any interactive yes/no confirmations that Fabric would find hard
# to deal with.


def _update_database():
    run('./virtualenv/bin/python manage.py makemigrations')
    run('./virtualenv/bin/python manage.py migrate --noinput')


def _provide_server_config():
    print('\nWould you like to add config files for gunicorn and nginx? (y|n)')
    x = input()
    if x == 'y':
        state = run(f'sh ./deploy_tools/provision_script.sh {env.host} {env.user}')
        if state == 1:
            return 0
    pass
