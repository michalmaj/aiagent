from google.genai import types

# importy realnych implementacji:
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_files import run_python_file
from functions.write_files import write_file

# routing: nazwa -> funkcja
FUNCTIONS = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

WORKING_DIR = "calculator"  # twardo wymagane przez zadanie

def call_function(function_call_part, verbose: bool = False):
    """Wywołuje odpowiednią funkcję na podstawie FunctionCall od LLM i zwraca types.Content z odpowiedzią narzędzia."""
    function_name = getattr(function_call_part, "name", None)
    args = dict(getattr(function_call_part, "args", {}) or {})

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    fn = FUNCTIONS.get(function_name)
    if not fn:
        # zwrotka w formacie tool-response (wymaga dict)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name or "unknown_function",
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # wstrzykuj working_directory – LLM nie kontroluje tego pola
    args = dict(args)
    args["working_directory"] = WORKING_DIR

    # drobna normalizacja: dla run_python_file brak args -> []
    if function_name == "run_python_file" and "args" not in args:
        args["args"] = []

    try:
        function_result = fn(**args)
    except Exception as e:
        function_result = f"Error: {e}"

    # zapakuj wynik jako function_response (response MUSI być dict)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )