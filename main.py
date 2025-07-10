import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions
from call_function import call_function
from config import MAX_ITERS
from prompts import system_prompt

def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "how do I fix the calculator?"')
        sys.exit(1)
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    iters = 0
    while True:
        iters+=1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final respons:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")
    
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    if len(sys.argv) > 2:
        if verbose:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)
    
    if not response.function_calls:
        return response.text
    
    function_responses=[] 
    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if not hasattr(result.parts[0],"function_response"):
            raise Exception("No function response")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting")
    messages.append(types.Content(role="tool", parts=function_responses))

if __name__ == "__main__":
    main()