# vault-api
Vault parser and API, used primarily to automate my portfolio.

## Create Cron job
To automatically pull once a day (fallback in case the webhook doesn't work) run:
`0 0 * * * /usr/bin/python3 /path-to-folder/daily_pull.py`
