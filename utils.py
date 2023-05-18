import tiktoken
import os 
import openai
from dotenv import load_dotenv
load_dotenv()

openai_model = os.environ.get("OPENAI_MODEL")
openai_model_max_tokens = 2000
openai.api_key = os.environ["OPENAI_API_KEY"]

def reportTokens(prompt):
    encoding = tiktoken.encoding_for_model(openai_model)
    # print number of tokens in light gray, with first 10 characters of prompt in green
    print("\033[37m" + str(len(encoding.encode(prompt))) + " tokens\033[0m" + " in prompt: " + "\033[92m" + prompt[:50] + "\033[0m")
  
def write_file(filename, filecode, directory):
    # Output the filename in blue color
    print("\033[94m" + filename + "\033[0m")
    print(filecode)
    
    file_path = directory + "/" + filename
    dir = os.path.dirname(file_path)
    os.makedirs(dir, exist_ok=True)

    # Open the file in write mode
    with open(file_path, "w") as file:
        # Write content to the file
        file.write(filecode)


def clean_dir(directory):
    import shutil

    extensions_to_skip = ['.env','.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.ico', '.tif', '.tiff']  # Add more extensions if needed
    folders_to_skip = [".serverless", "node_modules", ".git", ".idea", ".vscode", ".venv", "venv", "env", "envs", "virtualenv", "virtualenvs"]
    # Check if the directory exists
    if os.path.exists(directory):
        # If it does, iterate over all files and directories
        for root, dirs, files in os.walk(directory):
            if not root.split("/")[-1] in folders_to_skip:
                for file in files:
                    _, extension = os.path.splitext(file)
                    if extension not in extensions_to_skip and file not in extensions_to_skip:
                        os.remove(os.path.join(root, file))
    else:
        os.makedirs(directory, exist_ok=True)

# Generate a response from the OpenAI API
def generate_response(system_prompt, user_prompt, *args):
    messages = []
    messages.append({"role": "system", "content": system_prompt})
    reportTokens(system_prompt)
    messages.append({"role": "user", "content": user_prompt})
    reportTokens(user_prompt)
    
    # loop thru each arg and add it to messages alternating role between "assistant" and "user"
    role = "assistant"
    for value in args:
        messages.append({"role": role, "content": value})
        reportTokens(value)
        role = "user" if role == "assistant" else "assistant"
    
    params = {
        "model": openai_model,
        "messages": messages,
        "max_tokens": openai_model_max_tokens,
        "temperature": 0,
    }

    # Send the API request
    response = openai.ChatCompletion.create(**params)

    # Get the reply from the API response
    reply = response.choices[0]["message"]["content"]
    return reply
