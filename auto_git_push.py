import subprocess
import time
from datetime import datetime

REPO_PATH = '.'  # Current directory
PUSH_INTERVAL = 300  # 5 minutes in seconds

def git_push():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        subprocess.run(['git', 'add', '.'], cwd=REPO_PATH, check=True)
        subprocess.run(['git', 'commit', '-m', f'Auto-commit at {now}'], cwd=REPO_PATH, check=False)
        subprocess.run(['git', 'push'], cwd=REPO_PATH, check=True)
        print(f'Pushed at {now}')
    except Exception as e:
        print(f'Git push failed: {e}')

def main():
    while True:
        git_push()
        time.sleep(PUSH_INTERVAL)

if __name__ == '__main__':
    main() 