[![CircleCI](https://circleci.com/gh/xiaofeizhang19/ConsumeLess-backend.svg?style=svg)](https://circleci.com/gh/xiaofeizhang19/ConsumeLess-backend)

# ConsumeLess Backend

## Introduction
This application serves as the backend for our final project at Makers Academy. For details of project refer to [ConsumeLess -Frontend](https://github.com/xiaofeizhang19/ConsumeLess-frontend/edit/master/README.md).

The backend has been built in Python and Flask, providing REST APIs for data trasmition. It has been built with CircleCI and deployed on heroku.

## Requirements
> This application runs using python and postgresql as a database.  
> In order to run on a local machine be sure to have a database named **consumeless** on your local machine  
> If you would like to run tests you should also have a test database called **consumeless_test**

## Setup

- clone this repository  
``` $ git clone git@github.com:xiaofeizhang19/ConsumeLess-backend.git ```
- install a virtual environment  
``` $ pip install virtualenv ``` if this does not work try ``` pip3 install virtualenv ```
- cd into the project directory  
``` $ cd ConsumeLess-backend ```
- create a virtual environment  
``` $ virtualenv env ```
- change into/activate this virtual environment  
``` $ source env/bin/activate ```
- install the necessary python extensions using  
``` $ pip install -r requirements.txt ```
- apply the db migrations
``` $ dotenv run python.py db upgrade ```
- to launch the application with approriate run  
``` $ dotenv run python manage.py runserver ```

## Testing
-to run tests with coverage output run  
``` $ dotenv run pytest -v --cov=consumeless ```
