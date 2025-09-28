from ast import parse
import os
import hmac, hashlib

from dotenv import load_dotenv
from http.client import HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException

from logger import logger
from email_utils import send_email
from md_parser import parse_markdown_table
from git_utils import clone_repo, is_data_stale, last_commit_time, pull_and_check, REPO_PATH as DATA_PATH

# load envvars
load_dotenv()
GITHUB_SECRET = os.getenv('GITHUB_SECRET').encode('utf-8')

# clone the repository
# note that this requires the user be already authenticated on this machine. 
# this is fine for my use case but it's probably best to move to auth through
# a key or something
clone_repo() 

# create app
app = FastAPI()

# utility functions
def send_error_email(message='Not Applicable'):
    """
    Sends a generic warning email to myself.
    Message is optional
    """
    send_email(
        'Vault API Generic Error.',
        'Vault API failed! Please check logs (VAULT-API/logs/notes_api.log) for more details.' +
        f'\nMessage (if any): {message}'
    )

def parse_notes_md_table(table_name):
    """
    Shorthand to parse a markdown table from the table name directly.
    """
    return parse_markdown_table(f'../data/notes/Databases/{table_name}.md')

def handle_table_read(table_name):
    # parse the table
    try:
        table = parse_notes_md_table(table_name)
    except Exception as e:
        # respond to issues if any
        logger.error(f'Server failed to parse data: {e}')
        send_error_email()
        raise HTTPException(status_code=500, detail=f'Server failed to parse data.')

    # return table
    return table

# endpoints
@app.get('/projects')
def get_projects():
    projects = handle_table_read(table_name='Projects')
    return projects

@app.get('/reading-list')
def get_reading_list():
    books = handle_table_read(table_name='Reading List')
    return books

@app.get('/blog')
def get_blog():
    raise HTTPException(status_code=501, detail='This endpoint is not implemented yet')

@app.get('/currently-working-on')
def get_currently_working_on():
    cwo = handle_table_read('Currently Working On')
    return cwo

@app.get('/status')
def get_status():
    last = last_commit_time()
    return {
        'last_commit': last.isoformat() if last else None,
        'stale': is_data_stale()
    }

# GitHub webhooj
@app.post('/github-webhook')
async def gh_webhook(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()
    signature = request.headers.get('X-Hub-Signature-256')

    if signature is None:
        raise HTTPException(status_code=400, detail='Missing signature')

    if GITHUB_SECRET:
        mac = hmac.new(GITHUB_SECRET, msg=body, digestmod=hashlib.sha256)
        expected = 'sha256=' + mac.hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise HTTPException(status_code=400, detail='Invalid signature')
        
    background_tasks.add_task(pull_and_check)
    return {'status': 'ok'}

