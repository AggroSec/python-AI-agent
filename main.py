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

from call_function import available_functions, call_function

def model_call(args):
    if not hasattr(model_call, "messages") or model_call.messages is None:
        model_call.messages = [
            types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
        ]

    response = client.models.generate_content(
        model=model_name, 
        contents=model_call.messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.3,
            tools=[available_functions]
            ),
        )

    if response.usage_metadata != None:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {str(response.usage_metadata.prompt_token_count)}")
            print(f"Response tokens: {str(response.usage_metadata.candidates_token_count)}")
    else:
        raise RuntimeError("Usage Metadata not present, possible failed API call")
    
    if response.candidates:
        for candidate in response.candidates:
            model_call.messages.append(candidate.content)

    if response.function_calls:
        function_results = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)
            if function_call_result.parts == None:
                raise Exception("Error: no part returned")
            if function_call_result.parts[0].function_response == None:
                raise Exception("Error: function response not returned")
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("Error: function response's response not returned")
            
            function_results.append(function_call_result.parts[0])

            if args.verbose == True:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
            model_call.messages.append(types.Content(role="user", parts=function_results))
    else:
        print(response.text)
        return True

    return False

def main():
    if api_key == None:
        raise RuntimeError("API key was not found")
    
    parser = argparse.ArgumentParser(description="AI agent powered by Gemini, used to assist with coding.")
    parser.add_argument("user_prompt", type=str, help="Enter your AI prompt telling the agent what you want it to do.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    for _ in range(20):
        #used to call the model, and handle the responses
        is_model_call_finished = model_call(args)
        if is_model_call_finished == True:
            return


if __name__ == "__main__":
    main()
