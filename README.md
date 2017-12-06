
# Potato Tracker
Backend developer test for potato. The instructions for the test can be found [here](INSTRUCTIONS.md).

## Prerequisites:
- python 2.7
- pip
- git

## Setup

- Run `./install_deps` (this will pip install requirements, and download the App Engine SDK)
- `python manage.py loaddata site`
- `python manage.py runserver`

The application is written using the [Djangae](http://djangae.readthedocs.org/en/latest/) project.

## Testing

### Run the tests
Run the tests with: `python manage.py test`

### Run the tests with coverage
- Install coverage: `pip install coverage`
- Run the tests with coverage: `coverage run manage.py test`
- To view the report:
    - In the console run: `coverage report`
    - In the browser run: `coverage html` and then open the index.html file located in the htmlcov directory (`firefox htmlcov/index.html`)
