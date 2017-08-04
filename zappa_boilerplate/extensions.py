# -*- coding: utf-8 -*-
"""
Extensions module. Each extension is initialized in the app factory located in app.py
"""


from flask_login import LoginManager
login_manager = LoginManager()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_migrate import Migrate
migrate = Migrate()
