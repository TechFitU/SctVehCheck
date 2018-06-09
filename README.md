# [SctVehCheck][docs]

[![Build Status](https://travis-ci.org/arocks/edge.svg?branch=master)](https://travis-ci.org/arocks/edge)

**A web application for vehicle inspection registration.**
It is built with [Python][0] using the [Django Web Framework][1].
## Features

* Manage the information about vehicles, owner and inspection.  
* Ready Bootstrap-themed pages
* User Registration/Sign up
* Better Security with [12-Factor](http://12factor.net/) recommendations
* Logging/Debugging Helpers
* Works on Python 2.7 or 3.4

## Quick start:

To set up a development environment quickly, first install Python 3. It
comes with virtualenv built-in. So create a virtual env by:

1. `$ python3 -m venv sctvehcheck`
2. `$ . sctvehcheck/bin/activate`

Clone the project using the git link and go to the folder where is located.
After this got to the project folder and install all dependencies:
    
3. `$ cd sctvehcheck`
4. `$ pip install -r requirements.txt `
    
Make a copy the of the settings in the local environment file, and customize it according to your needs.

5. `$ cp sctvehcheck/settings/local.sample.env sctvehcheck/settings/local.env` (New!) 

Run migrations:

5.`$ python manage.py migrate`

Run the project.

7. `$ python manage.py runserver`


## Recommended Installation (with `pipenv`)
1. [Install pipenv system-wide or locally](https://docs.pipenv.org/) but outside a virtualenv
2. Download it or clone the project. Go to the download folder using the command bellow.
3. `$ cd sctvehcheck`
4. `$ pipenv install --dev`
4. `$ pipenv shell`
4. `$ cd src`
5. `$ cp sctvehcheck/settings/local.sample.env sctvehcheck/settings/local.env` (New!)
6. `$ python manage.py migrate`
7. `$ python manage.py runserver`

If you need to keep `requirements.txt` updated then run

    pipenv lock --requirements > requirements/base.txt
    echo "-r base.txt" > requirements/development.txt
    pipenv lock --requirements --dev >> requirements/development.txt


### Detailed instructions
Take a look at the docs for more information.

[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
