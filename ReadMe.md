![Django Logo](/src/django-banner.jpg)



## About
Django is a web-framework written in Python and runs the backend for many of the internet's most popular websites. This is a multi-user type auth app, it is built ontop of Django 3.1.1 


This app features the following:

-- AbstractUser for custom user authentication


-- Authentication Backend configured to authenticate users, using email and password


-- CreateUser Type Teacher or Student at signup


-- Signup With Email Verification Token


-- Login


-- Very basic profile dashboard


-- simple permission to restrict unauthenticate users and unauthorized access


## Technology and Requirements
1. Django 3.1.1
2. Python3
3. Boostrap 4.3.x (for front end)

## Installations
1. [installing Python3](https://www.python.org/downloads/)
2. [installing Django 3.0](https://docs.djangoproject.com/en/3.0/topics/install/)
3. [installing Virtualenv](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/)
5. installing requirements from requirements.txt. After activating vitualenv run:

`(venv)path/to/app/src$ pip install -r requirements.txt
`

6. [psycopg2](http://initd.org/psycopg/docs/install.html)


## Run App
1. After cloning this repo, make sure your virtualenv is ativated and change your path to $app_root/.

`
(venv)path/to/app$
`

2. install packages required by running
`(venv)path/to/app$ pip install -r requirements.txt
`

3. change director to src/ make sure you are in the same directory where manage.py is then run

`(venv)path/to/app/src$ python manage.py makemigrations
`

4. The migrate the app
`(venv)path/to/app/src$ python manage.py migrate
`

5. To run the development server
`(venv)path/to/app/src$ python manage.py runserver
`

6. go to your web browser and enter 127.0.0.1:8000 

## Recommendations
This App is not designed to be used full in deployement. You are free to make any adjustments to it and include in you project
 


## Resources
1. [Django 3.x Doc](https://docs.djangoproject.com/en/3.1/)
2. [My Previous Repo](https://github.com/codeOlam/multi-user-auth-django)

### Other Resources
1. [Customizing authentication in Django](https://docs.djangoproject.com/en/3.1/topics/auth/customizing/) 

