import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types
from config import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_files import schema_run_python_file
from functions.write_files import schema_write_file
from functions.call_function import call_function


def main():   
    # Check if an argument is provided before accessing it
    args = sys.argv[1:]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    # Get itnput from command line as an argument
    message = sys.argv[1]
    verbose = False

    if len(sys.argv) >= 3 and sys.argv[2] == "--verbose":
        verbose = True
        

    # Load enviroment variables from .env file
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Check if api key is available
    if not api_key:
        raise ValueError("Brak GEMINI_API_KEY w .env")

    # Create a Gemini client
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, user_prompt, verbose)


def generate_content(client, messages, user_prompt, verbose):
    # 1) Zdefiniuj dostępne narzędzia (4 schematy)
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    max_iters = 20

    for step in range(max_iters):
        try:
            # 2) Każde wywołanie dostaje CAŁĄ historię `messages`
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )

            if verbose:
                usage = getattr(response, "usage_metadata", None)
                print(f"User prompt: {user_prompt}") if step == 0 else None
                if usage:
                    print("Prompt tokens:", getattr(usage, "prompt_token_count", "N/A"))
                    print("Response tokens:", getattr(usage, "candidates_token_count", "N/A"))

            # 3) Jeśli model zwrócił finalny tekst — drukujemy i kończymy
            if getattr(response, "text", None) and response.text.strip():
                print(response.text)
                break

            # 4) Dodajemy wszystkie odpowiedzi-kandydatów (asystenta) do historii
            #    oraz obsługujemy ewentualne wywołania funkcji
            made_any_call = False

            for candidate in getattr(response, "candidates", []) or []:
                content = getattr(candidate, "content", None)
                if not content:
                    continue

                # a) dodaj asystenta (jego plan / function_call) do rozmowy
                messages.append(content)

                # b) sprawdź, czy w częściach jest function_call
                for part in getattr(content, "parts", []) or []:
                    func_call = getattr(part, "function_call", None)
                    if not func_call:
                        continue

                    made_any_call = True

                    # 5) Wykonaj funkcję (tu następuje realne działanie)
                    function_call_result = call_function(func_call, verbose=verbose)

                    # 6) Wyciągnij formalne function_response (name + response dict)
                    try:
                        fr = function_call_result.parts[0].function_response
                    except Exception as e:
                        raise RuntimeError(f"Fatal: tool response missing or malformed: {e}")

                    # 7) Zgodnie z instrukcją: zamień odpowiedź narzędzia
                    #    na WIADOMOŚĆ z rolą 'user' i dołóż do historii.
                    #    (to “oddaje” wynik modelowi jako kolejny krok konwersacji)
                    messages.append(
                        types.Content(
                            role="user",
                            parts=[types.Part.from_function_response(name=fr.name, response=fr.response)],
                        )
                    )

                    # 8) Debug wyników narzędzi w trybie verbose
                    if verbose:
                        print(f"-> {fr.response}")

            # 9) Jeśli nie było żadnego function_call i nie było finalnego tekstu,
            #    nie ma po co kręcić pętli dalej.
            if not made_any_call and not (getattr(response, "text", None) and response.text.strip()):
                if verbose:
                    print("(no function call and no final text; stopping)")
                break

        except Exception as e:
            # 10) Błędy nie mogą wieszać pętli
            print(f"Error: {e}")
            break
    else:
        # pętla dobiegła do max_iters
        if verbose:
            print("Reached max iterations without final text.")

if __name__ == "__main__":
    main()
