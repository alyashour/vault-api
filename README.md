# VAULT-API
Vault parser and API, used primarily to automate my portfolio.

## Env Variables
For this to work you'll need `.env` variables defined.
To do this
1. Create a `.env` file in the root of this repo.
2. Add the following:
```env
# MAIL
# This API automatically sends mail on failure
# Set up for GMAIL by default
EMAIL_FROM=
EMAIL_TO=
APP_PASSWORD= # set one up in Google account details

# GIT
REPO_NAME= # name of the repository
REPO_PATH= # the path where the repo will be cloned
REPO_URL= # the http address of the repo

# GITHUB
# This api uses a webhook to stay up to date
# Addthe secret for the webhook below:
GITHUB_SECRET= 

# LOGGING
LOG_FILE= # where to write logs (rotating, default=../logs/notes_api.log)
```

## Create Cron job
There is a script here that you can use as a service or for cron. Some extra work is required to set up the service that I haven't done yet but it shouldn't be too bad. Use `src/daily_pull.py` for this.

