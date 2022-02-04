import subprocess
import time
import traceback
import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

"""
SCRIPT FOR MYSQL DATABASE BACKUP AND IMPORT
    - Don't forget to set the environment variables in the .env file
"""

DATABASE = ["analysis_db", "comms_db", "commons_db", "ewi_db"]

REMOTE_USERNAME = os.getenv("REMOTE_USERNAME")
REMOTE_PASSWORD = os.getenv("REMOTE_PASSWORD")
REMOTE_HOST = os.getenv("REMOTE_HOST")
LOCAL_USERNAME = os.getenv("LOCAL_USERNAME")
LOCAL_PASSWORD = os.getenv("LOCAL_PASSWORD")

def BackupAndImport():
    print("STARTING DATABASE BACKUP:")

    for db in DATABASE:
        time_start = time.perf_counter()

        print(f"\nCreating dump file for {db}")
        command = ['mysqldump', f'-u{REMOTE_USERNAME}', f'-p{REMOTE_PASSWORD}', f'-h{REMOTE_HOST}', '--column-statistics=0', '--verbose', f'{db}']
        with open('ewi_db.sql', 'w') as outfile:
            subprocess.run(command, stdout = outfile)

        print(f"\nImporting {db} to MySQL")
        file = Path(f'{db}.sql')
        file.touch(exist_ok=True)
        with open(f'{db}.sql', 'r') as f: 
            command = ['mysql', f'-u{LOCAL_USERNAME}', f'-p{LOCAL_PASSWORD}', f'{db}']
            proc = subprocess.Popen(command, stdin = f)
            stdout, stderr = proc.communicate()
        
        time_delta = time.perf_counter() - time_start
        print(f"Done! Total time elapsed: {time_delta} seconds")
        print("-"*64)
    
    print(f"\nDATABASE BACKUP COMPLETE. \nOperation took {time.perf_counter() - time_start} seconds")


def main():
    try:
        BackupAndImport()
    except Exception as exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()