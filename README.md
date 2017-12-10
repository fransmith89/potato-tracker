
# Potato Tracker
Backend developer test for potato. The instructions for the test can be found [here](INSTRUCTIONS.md).

## Prerequisites:
- python 2.7
- pip
- git

## Development
The application is written using the [Djangae](http://djangae.readthedocs.org/en/latest/) project.

To run the application locally:
- Run `./install_deps` (this will pip install requirements, and download the App Engine SDK)
- Run `python manage.py loaddata site` to populate the site with the [following data](tracker/site/fixtures/site.json)
- Run the application with `python manage.py runserver`

*Note: Before committing run the linter, using `flake8 tracker/site`, and fix any issues it finds*

## Testing

### Run the tests
Run the tests with: `python manage.py test`

### Run the tests with coverage
- Install coverage: `pip install coverage`
- Run the tests with coverage: `coverage run manage.py test`
- To view the report:
    - In the console run: `coverage report`
    - In the browser run: `coverage html` and then open the index.html file located in the htmlcov directory (`firefox htmlcov/index.html`)
