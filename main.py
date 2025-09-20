import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types


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
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    if verbose:
        print(f'User prompt: {user_prompt}')
        # „na każdej iteracji” — tu jest jedna, ale jeśli dodasz pętlę,
        # te linie będą logować statystyki dla każdej odpowiedzi.
        usage = response.usage_metadata
        # Dostępne atrybuty zwykle obejmują:
        # prompt_token_count, candidates_token_count, total_token_count
        print("Prompt tokens:", getattr(usage, "prompt_token_count", "N/A"))
        print("Response tokens:", getattr(usage, "candidates_token_count", "N/A"))

    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
