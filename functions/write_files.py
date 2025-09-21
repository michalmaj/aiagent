import os
from google.genai import types


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


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            ),
        },
    ),
)