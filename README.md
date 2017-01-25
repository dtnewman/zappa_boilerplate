
basic_zappa_project
===================

[![Build Status](https://travis-ci.org/dtnewman/basic_zappa_project.svg?branch=master)](https://travis-ci.org/dtnewman/basic_zappa_project) 
[![Coverage Status](https://coveralls.io/repos/github/dtnewman/basic_zappa_project/badge.svg?branch=master)](https://coveralls.io/github/dtnewman/basic_zappa_project?branch=master)

This repo is meant to demonstrate how to setup a **serverless** web application using [Flask](http://flask.pocoo.org/) and [Zappa](https://github.com/Miserlou/Zappa). I created a simple web application with a Postgres database that is meant to be a starting point for more complex projects.

A demo of the deployed code (deployed using Zappa) can be found [here](https://u7qxl040d3.execute-api.us-east-1.amazonaws.com/dev/).

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

*Before you begin, make sure you have a valid AWS account and your [AWS credentials file](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks/) is properly installed.*

First you will need to setup a hosted Postgres database. [ElephantSQL](https://www.elephantsql.com/) and [Heroku](https://www.heroku.com/postgres) both allow you to setup limited databases for free. Once you have that setup,
you will need to get the database connection string (typically in the format *"postgresql://user:secret@host/db_name"*) from the hosting service.

Next you will need to setup a bucket with a name of your choice on S3 (I used "basic-zappa-project-example-bucket" for mine. You'll need to choose a bucket name that isn't taken). This can be done with the [AWS command line interface](https://aws.amazon.com/cli/) with the following command:

```
$ aws s3 mb s3://your-bucket-name
```

You most likely don't want to commit the database connection string to source control (if you do, you can just modify the SQLALCHEMY_DATABASE_URI values in settings.py). So we will use
environment variables to set this value. To do this, we generate a file called "config_secrets.json" and upload it to our S3 bucket. The "remote_env" value in zappa_settings.json will
tell Zappa to grab environment variables from that file. We can generate the file and upload it to S3 as follows:

```
$ echo '{ "DB_CONNECTION_STRING": "<YOUR SUPER SECRET DB CONNECTION STRING GOES HERE>" }' > config_secrets.json
$ aws s3 cp config_secrets.json s3://your-bucket-name
```

Later, you can expand this file with other environment variables for things that shouldn't be committed to source control.

Now, we just need to update the file zappa_settings.json with your newly created bucket name. Simply change the strings in the fields "s3_bucket" and "remote_env" to match your bucket name.

You are now ready to deploy! To do so, simply run the command:

```
$ zappa deploy 
```

When the process finishes, it will give you the URL of your newly deployed application!

Making Changes 
--------------
If you wish to deploy new changes to your repo simply update the code and then run:

```
$ zappa update 
```

Undeploy
--------
Undeploying your code is simple. Just run the following command:
```
$ zappa undeploy 
```

Advanced Features
-----------------
This project is simply meant to be boilerplate template to get you started, but Zappa has a bunch of cool features that I did not touch in this repo. Checkout the [Zappa](https://github.com/Miserlou/Zappa) repository for more cool features.


Acknowledgements
----------------
The structure of this code borrows heavily from the [cookiecutter-flask](https://github.com/sloria/cookiecutter-flask) repo.