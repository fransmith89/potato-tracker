
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
- Run `python manage.py loaddata site --app_id potato-tracker` to populate the site with the [following data](tracker/site/fixtures/site.json)
- Run the application with `python manage.py runserver --app_id potato-tracker`

To watch for front-end changes:
- Make sure you have [npm](https://www.npmjs.com/get-npm) and bower (`npm install -g bower`) installed
- Install the node modules: `npm install`
- Install the bower component: `bower install`
- Run `gulp` in a separate terminal and it will watch (and build) any changes to .scss files

*Note: Before committing run the linter, using `flake8 tracker/site`, and fix any issues it finds*

## Testing

### Run the tests
Run the tests with: `python manage.py test --app_id potato-tracker`

### Run the tests with coverage
- Install coverage: `pip install coverage`
- Run the tests with coverage: `coverage run manage.py test --app_id potato-tracker`
- To view the report:
    - In the console run: `coverage report`
    - In the browser run: `coverage html` and then open the index.html file located in the htmlcov directory (`firefox htmlcov/index.html`)

## Deployment
### First Deployment
In the browser:
- Navigate to https://console.cloud.google.com and sign in with your google account
- Create a new project

On your machine:
- Install [Google Cloud SDK](https://cloud.google.com/sdk/downloads)
- In the potato-tracker directory, run `gcloud init` and follow through the instructions (make sure you select the project you created before)
- To deploy the application, run `gcloud app deploy` and follow the prompts
- Once it has finished, go to the address provided to view your application

### Update Deployment
In the potato-tracker directory:
- Build any front-end changes with `gulp build`
- Deploy with `gcloud app deploy` and follow the prompts
- Once it has finished, go to the address provided to view your application
