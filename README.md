# Job Trend Analyzer API Lambda

## Table of Contents

- [Job Trend Analyzer API Lambda](#job-trend-analyzer-api-lambda)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Setup your database](#setup-your-database)
  - [Run](#run)
  - [Run tests](#run-tests)
  - [Deploying to AWS Lambda](#deploying-to-aws-lambda)
    - [Required environment variables](#required-environment-variables)
    - [Package this manually to zip for uploading to AWS Lambda](#package-this-manually-to-zip-for-uploading-to-aws-lambda)

## Prerequisites

You can quickly run this app using [Poetry](https://python-poetry.org/).

```bash
pip install poetry
```

Then install packages:

```bash
poetry install --sync
```

## Setup your database

You need a database setup for [job_post_counts_scraper](https://github.com/TakumaKira/job_post_counts_scraper#setup-your-database). **This app works only with PostgreSQL database so Sqlite3 database won't work. Please prepare local PostgreSQL database like [this](https://postgresapp.com/)**

## Run

To run this app in production, you need to provide some environment variables like the following:

```bash
DB_USER=your_db_app_user_name \
DB_PASS=your_db_app_user_pass \
DB_HOST=your_db_host_name \
DB_PORT=your_db_port \
DB_NAME=your_db_name \
poetry run python src/app/lambda_function.py
```

## Run tests

To run the tests, run:

```bash
poetry run python -m pytest -s
```

*You can omit `-s` if you don't need prints.*

## Deploying to AWS Lambda

### Required environment variables

`FUNCTION_ENVIRONMENT` needs to be `aws_lambda`.
`AWS_RDS_ENDPOINT` has to tell your RDS database endpoint.
`AWS_DB_SECRETS_NAME`	has to tell your AWS Secrets Manager secrets name which contains `username` / `password` / `port` / `dbname` of your target database.

### Package this manually to zip for uploading to AWS Lambda

I set up GitHub actions workflow to package and deploy this to AWS lambda, but you can also do it manually with the following commands **if your environment is Linux**;

*Packaging needs to be executed on Linux to make psycopg2 work on the Lambda environment. See <https://stackoverflow.com/a/46366104>*

```bash
rm -rf dist && mkdir -p dist/lambda-package
rm -rf .venv && poetry install --only main --sync
cp -r .venv/lib/python*/site-packages/* dist/lambda-package/
cp -r src/app/* dist/lambda-package/
rm -rf dist/lambda-package/**/__pycache__
cd dist/lambda-package
zip -r ../lambda.zip .
cd ../..
```

The above makes your packages only for production (which means excluding packages for development purposes such as testing).
So you'd better revert it to the development environment ASAP with the below:

```bash
rm -rf .venv && poetry install --sync
```
