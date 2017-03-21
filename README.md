# Organisation-api
This service is responsible for organisation details and is connected to by deed-api
when a Borrower has signed in and is viewing a deed.

See: deed-api at 
 
### Contents

- [Usage](#usage)
- [Available routes](#available-routes)
- [Useful Curl commands](#useful-curl-commands)
- [Quick start](#quick-start)
- [Unit tests](#unit-tests)

## Usage

In its current state, you can use the service to retrieve, post or delete an organisation name to a local database. This is used
to display an organisation name on a deed in the Borrower Frontend that does not have any unnecessary information within it.

## Available routes

```
get     /organisation-name/<organisation_id>    # Get a friendly organisation name
post    /organisation/                          # Create an organisation by posting a json object reflecting the schema in the organisation_name views module
delete  /organisation/<organisation_id>         # Delete a friendly organisation name
```

## Useful Curl commands
### Get
curl localhost:9060/organisation-name/10.1.1

### Post
curl -X POST -d '{"organisation_name": "Bananas",  "organisation_id": "10.1.1"}' -H "Content-Type: application/json" http://localhost:9060/organisation-name

### Delete
curl -X "DELETE" localhost:9060/organisation-name/10.1.1

## Quick start 

```shell
### For Flask CLI
export FLASK_APP=organisation_api/main.py
export FLASK_DEBUG=1
### For Python
export PYTHONUNBUFFERED=yes
### For gunicorn
export PORT=9060
### For app's config.py
export FLASK_LOG_LEVEL=DEBUG
export COMMIT=LOCAL

### Run the app
flask run
```

or run the shell command:

```bash
make run
```

## Unit tests

These bashin instructions apply only for our development environment

```
bashin organisation-api
```

```
make unittest
```
