import os
from dotenv import load_dotenv
from google import genai


def main():
    # Load enviroment variables from .env file
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Check if api key is available
    if not api_key:
        raise ValueError("Brak GEMINI_API_KEY w .env")

    # Create a Gemini client
    client = genai.Client(api_key=api_key)

    # Send a message to the model
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents='Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.')
    
    # Print the response
    print(response.text)

    # Check how many tokens were used
    usage = response.usage_metadata
    print(f"Prompt tokens: {usage.prompt_token_count}")
    print(f"Response tokens: {usage.candidates_token_count}")

if __name__ == "__main__":
    main()
