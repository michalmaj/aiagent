import os
from google.genai import types

def get_files_info(working_directory, directory="."):

    base = os.path.realpath(working_directory)
    target = os.path.realpath(os.path.join(base, directory))

    # check sandbox boundary
    if os.path.commonpath([base, target]) != base:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'        

    # check if it's actually a directory
    if not os.path.isdir(target):
        return f'Error: "{directory}" is not a directory'

    entries = sorted(os.listdir(target))

    lines = []
    for name in entries:
        path = os.path.join(target, name)
        size = os.path.getsize(path)
        is_dir = os.path.isdir(path)
        lines.append(f"- {name}: file_size={size} bytes, is_dir={str(is_dir)}")

    return "\n".join(lines)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)