# runcommand.py

import subprocess

def execute_command(command):
    completed_process = subprocess.run(command, shell=True, text=True, capture_output=True)
    output = completed_process.stdout
    error = completed_process.stderr
    return_code = completed_process.returncode
    return output, error, return_code
