
basic_zappa_project
===================

[![Build Status](https://travis-ci.org/dtnewman/basic_zappa_project.svg?branch=master)](https://travis-ci.org/dtnewman/basic_zappa_project) 
[![Coverage Status](https://coveralls.io/repos/github/dtnewman/basic_zappa_project/badge.svg?branch=master)](https://coveralls.io/github/dtnewman/basic_zappa_project?branch=master)

This repo is meant to demonstrate how to setup a **serverless** web application using [Flask](http://flask.pocoo.org/) and [Zappa](https://github.com/Miserlou/Zappa). I created a simple web application with a Postgres database that is meant to be a starting point for more complex projects.

A demo of the deployed code (deployed using Zappa) can be found [here](https://svvikpbodk.execute-api.us-east-1.amazonaws.com/dev/).

Quickstart
----------

**Step 1:** Clone the repo and install requirements (you probably want to do this with a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) with a name like *basic_zappa_project_venv*):

```
$ git clone git@github.com:dtnewman/basic_zappa_project.git
$ cd basic_zappa_project
$ pip install -r requirements.txt
```

**Step 2:** Create local and local test databases:

```
$ psql -c 'create database basic_zappa_project;' -U postgres
$ psql -c 'create database basic_zappa_project_test;' -U postgres
```

**Step 3:** Setup the local database:

This repo uses flask-Migrate to handle database migrations. The following commands will setup the initial database: 

```
$ python manage.py db init     # this will add a migrations folder to your application
$ python manage.py db migrate  # run initial migrations
$ python manage.py db upgrade  # apply initial migrations to the database
```

See the [flask-Migrate documentation](https://flask-migrate.readthedocs.io/en/latest/) for more details information on this step.

**Step 4:** Run the application on a local server:

```
$ python manage.py runserver
```

Then go to [http://localhost:5000/](http://localhost:5000/) in your browser to test out the application running locally.

**Step 5:** Run tests: 
 
```
$ python manage.py test
```

You can also run tests directly with [nose](http://nose.readthedocs.io):

```
$ nosetests
```


**Step 6:** Deploy to AWS using Zappa:

Instructions coming soon...

Acknowledgements
----------------
The structure of this code borrows heavily from the [cookiecutter-flask](https://github.com/sloria/cookiecutter-flask) repo.