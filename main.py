import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)

import argparse

from prompts import system_prompt

from config import model_name

def main():
    if api_key == None:
        raise RuntimeError("API key was not found")
    
    parser = argparse.ArgumentParser(description="AI agent powered by Gemini, used to assist with coding.")
    parser.add_argument("user_prompt", type=str, help="Enter your AI prompt telling the agent what you want it to do.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model=model_name, 
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0
            ),
        )

    if response.usage_metadata != None:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {str(response.usage_metadata.prompt_token_count)}")
            print(f"Response tokens: {str(response.usage_metadata.candidates_token_count)}")
    else:
        raise RuntimeError("Usage Metadata not present, possible failed API call")
    
    print(response.text)


if __name__ == "__main__":
    main()
