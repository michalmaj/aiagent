import os
import subprocess, sys


def run_python_file(working_directory, file_path, args=[]):
    base = os.path.realpath(working_directory)
    target = os.path.realpath(os.path.join(base, file_path))

    if os.path.commonpath([base, target]) != base:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(
            [sys.executable, target, *args],
            cwd=base,
            capture_output=True,
            text=True,
            timeout=30,
            check=False
        )

        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()
        code = completed_process.returncode

        if not stdout and not stderr:
            return "No output produced."

        parts = []
        if stdout:
            parts.append(f"STDOUT:\n{stdout}")
        if stderr:
            parts.append(f"STDERR:\n{stderr}")
        if code != 0:
            parts.append(f"Process exited with code {code}")

        return "\n".join(parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"