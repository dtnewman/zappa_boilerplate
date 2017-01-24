
basic_zappa_project
===================

[![Build Status](https://travis-ci.org/dtnewman/basic_zappa_project.svg?branch=master)](https://travis-ci.org/dtnewman/basic_zappa_project)
    
Code for a basic Flask application to be deployed with [Zappa](https://github.com/Miserlou/Zappa).


Quickstart
----------

First, set your app's secret key as an environment variable. For example, example add the following to ``.bashrc`` or ``.bash_profile``.

.. code-block:: bash

    export PERSONAL_HOMEPAGE_SECRET = 'something-really-secret'


Then run the following commands to bootstrap your environment.


::

    git clone https://github.com/dtnewman/personal_homepage
    cd personal_homepage
    pip install -r requirements/dev.txt
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py server



Deployment
----------

In your production environment, make sure the ``PERSONAL_HOMEPAGE_ENV`` environment variable is set to ``"prod"``.


Shell
-----

To open the interactive shell, run ::

    python manage.py shell

By default, you will have access to ``app``, ``db``, and the ``User`` model.


Running Tests
-------------

To run all tests, run ::

    python manage.py test


Migrations
----------

Whenever a database migration needs to be made. Run the following commmands:
::

    python manage.py db migrate

This will generate a new migration script. Then run:
::

    python manage.py db upgrade

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``.
