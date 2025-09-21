import os
from .config import MAX_FILE_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    try:
        base = os.path.realpath(working_directory)
        target = os.path.realpath(os.path.join(base, file_path))

        try:
            if os.path.commonpath([base, target]) != base:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        except ValueError:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        try:
            with open(target, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception as e:
            return f"Error: {e}"

        if len(content) > MAX_FILE_CHARS:
            return content[:MAX_FILE_CHARS] + f'[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"
    


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read, relative to the working directory.",
            ),
        },
    ),
)