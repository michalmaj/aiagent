import os


def write_file(working_directory, file_path, content):
    base = os.path.realpath(working_directory)
    target = os.path.realpath(os.path.join(base, file_path))

    if os.path.commonpath([base, target]) != base:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        dirpath = os.path.dirname(target)
        os.makedirs(dirpath, exist_ok=True)
    except Exception as e:
        return f"Error: {e}"
    
    try:
        with open(target, "w", encoding="utf-8", errors="replace") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"
    else:
       return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
