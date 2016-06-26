# encoding: utf-8
from fabric.api import *
import time

# env.hosts = ['ttc@www.kbstreet.com']

env.roledefs = {
    'production_main': ['root@120.27.156.44', ],
}

env.password = ''

"========================================================================="
"||                           Production Main                           ||"
"========================================================================="


@roles('production_main')
def supervisor_start():
    sudo('supervisord -c /home/django-scrapy/supervisord.conf')


@roles('production_main')
def supervisor_stop():
    sudo('supervisorctl stop all')
    sudo('unlink /tmp/supervisor.sock')



@roles('production_main')
def supervisor_restart():
    supervisor_stop()
    supervisor_start()


@roles('production_main')
def nginx_start():
    sudo('nginx -c /home/django-scrapy/nginx.conf')


@roles('production_main')
def nginx_stop():
    with settings(warn_only=True):
        sudo('nginx -s stop')


@roles('production_main')
def nginx_reload():
    """如nginx未开启则会报异常"""
    sudo('nginx -s reload')


@roles('production_main')
def gunicorn_start():
    # sudo('workon superworm')
    with prefix("workon superworm;cd /home/django-scrapy/"):
        sudo('gunicorn super_worm.wsgi:application  -w 4 -b 127.0.0.1:8081 -k gevent --max-requests 500')


@roles('production_main')
def gunicorn_stop():
    with settings(warn_only=True):
        sudo('pkill gunicorn')


@roles('production_main')
def uwsgi_restart():
    gunicorn_stop()
    time.sleep(1)
    gunicorn_start()


@roles('production_main')
def collectstatic():
    with cd('/home/django-scrapy/'):
        sudo('python manage.py collectstatic --noinput')


@roles('production_main')
def git_pull():
    with cd('/home/django-scrapy/'):
        sudo('git pull')


@roles('production_main')
def git_update():
    git_pull()
    collectstatic()


@roles('production_main')
def git_reset():
    with cd('/home/django-scrapy/'):
        sudo('git reset --hard')


@roles('production_main')
def migrate():
    with cd('/home/django-scrapy/'):
        sudo('python manage.py makemigrations')
        sudo('python manage.py migrate')


@roles('production_main')
def start():
    gunicorn_start()
    nginx_start()


@roles('production_main')
def stop():
    nginx_stop()
    gunicorn_stop()


@roles('production_main')
def restart():
    stop()
    time.sleep(1)
    start()


@roles('production_main')
def update():
    gunicorn_stop()
    git_update()
    migrate()
    # gunicorn_start() Because I use the supervisor so I without start it


@roles('production_main')
def update_no_migrate():
    gunicorn_stop()
    git_update()
    # gunicorn_start() Because I use the supervisor so I without start it


@roles('production_main')
def crontab_show():
    with cd('/home/django-scrapy/'):
        sudo('python manage.py crontab show')


@roles('production_main')
def crontab_add():
    with cd('/home/django-scrapy/'):
        sudo('python manage.py crontab add')
