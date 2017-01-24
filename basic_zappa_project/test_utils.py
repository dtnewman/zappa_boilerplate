# -*- coding: utf-8 -*-
'''Helper utilities for testing.'''


import unittest

from basic_zappa_project import settings
from basic_zappa_project.app import create_app
from basic_zappa_project.database import db_session, init_db, drop_db


class BaseTestCase(unittest.TestCase):

    def create_app(self):
        app = create_app(config_object=settings.Test)
        return app

    def setUp(self):
        self.app = self.create_app()
        self.session = db_session
        print(db_session)
        print(db_session.bind)
        init_db()

    def tearDown(self):
        self.session.close()
        drop_db()
        self.session.remove()
