#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand

from zappa_boilerplate.app import create_app
import zappa_boilerplate.models as models
import zappa_boilerplate.settings
from zappa_boilerplate.database import db

env = os.environ.get('env', 'Local')

config_object = getattr(zappa_boilerplate.settings, env)
app = create_app(config_object=config_object)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)

def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'models': models}


@manager.command
def test():
    import subprocess
    command = 'nosetests --cover-erase --with-xunit --with-coverage --cover-package=zappa_boilerplate'.split(' ')
    return subprocess.call(command)

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    sys.stdout.flush()
    manager.run()