import subprocess
import os 
from dotenv import load_dotenv
from datetime import datetime, timedelta 
from email_utils import send_email

load_dotenv()

REPO_NAME= os.getenv('REPO_NAME')
REPO_PATH = os.getenv('REPO_PATH')
REPO_URL = os.getenv('REPO_URL')

if not REPO_PATH or not REPO_URL or not REPO_URL:
    raise Exception('Failed to load .env variables please check .env is provided and try again.')

STALE_DAYS_COUNT = 7 # after how many days is the current data stale

def clone_repo():
    if not os.path.exists(REPO_PATH):
        subprocess.run(['git', 'clone', REPO_URL, REPO_PATH])

def git_pull():
    try:
        subprocess.run(['git', '-C', REPO_PATH, 'pull', 'origin', 'main'])
        return True
    except subprocess.CalledProcessError:
        return False 
    
def last_commit_time():
    try:
        output = subprocess.check_output(
            ['git', '-C', REPO_PATH, 'log', '-1', '--format=%ct']
        )
        timestamp = int(output.strip())
        return datetime.fromtimestamp(timestamp)
    except Exception:
        return None 
    
def is_data_stale(days=7):
    last = last_commit_time()
    if not last:
        return True
    return datetime.now() - last > timedelta(days=days)

def pull_and_check():
    success = git_pull()
    if not success:
        send_email(
            'Notes API: Git pull failed',
            'Failed to pull from GitHub repo'
        )
    elif is_data_stale():
        send_email(
            'Notes API: Data stale',
            'The notes data is older than 1 week'
        )