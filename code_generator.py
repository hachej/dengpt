
import os 
import ast
import argparse
from utils import write_file, clean_dir, generate_response

def generate_file(filename, filepaths_string=None, shared_dependencies=None, prompt=None):
    """ generate code for a single file """

    filecode = generate_response(
        f"""You are an AI developer who is trying to write a program that will generate code for the user based on their intent.
        
    the app is: {prompt}

    the files we have decided to generate are: {filepaths_string}

    the shared dependencies (like filenames and variable names) we have decided on are: {shared_dependencies}
    
    only write valid code for the given filepath and file type, and return only the code.
    do not add any other explanation, only return valid code for that file type.
    """,
        f"""
    We have broken up the program into per-file generation. 
    Now your job is to generate only the code for the file {filename}. 
    Make sure to have consistent filenames if you reference other files we are also generating.
    
    Remember that you must obey 3 things: 
       - you are generating code for the file {filename}
       - do not stray from the names of the files and the shared dependencies we have decided on
       - MOST IMPORTANT OF ALL - the purpose of our app is {prompt} - every line of code you generate must be valid code. Do not include code fences in your response, for example
    
    Bad response:
    ```javascript 
    console.log("hello world")
    ```
    
    Good response:
    console.log("hello world")
    
    Begin generating the code now.

    """,
    )

    return filename, filecode


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This is a demo script.")
    parser.add_argument('--p','-prompt', type=str, help='prompt file')
    parser.add_argument('--f', '-file', type=str, help='file to update')
    args = parser.parse_args()

    provider = "OEC"
    dataset_name = "ECI_trade"
    base_directory = "./pipelines"
    lambda_name = "lambda_data_to_s3"
    directory = f"{base_directory}/provider={provider}/dataset_name={dataset_name}"
    frequency = "every day at 21:00"
    bucket_name = f'sumeo-provider-{provider}-data'.lower()
    prompt = f"""
    1- Lambda Function:
        Develop a Python file named 'lambda_handler'. This function should act as a Lambda function handler and accept two arguments: event and context.
        Invoke the endpoint url saved in env variable {provider}_{dataset_name}_ENDPOINT and store the response payload in a bucket named 'sumeo-{provider}' within the directory data_profile=raw/dataset_name={dataset_name}/.
        Generate the file name by creating an MD5 hash of the data.
        Save the file in the bucket {bucket_name}, using the path data_profile=raw/provider_name={provider}/dataset_name={dataset_name}/request_time=request_day/, where request_day is the day of the request in UTC.
        Append metadata to the file with the following information:
            Request time in UTC
            Provider: {provider}
            Dataset name: {dataset_name}
        The function should return a dictionary with statusCode set to 200.
        Ensure all import statements are at the top of the file.
        Create a requirements.txt file containing the necessary dependencies (excluding hashlib, which is already imported).

    2- Deployment on AWS using the Serverless Framework:
        Generate a serverless.yml file in the base directory. This file should define:
            A Lambda function named {lambda_name} triggered at a certain {frequency}.
            An S3 bucket named {bucket_name} lowercase with read and write access for the Lambda function.
            Set useDotenv: true at the top of the file
            A shell script file to install the required Serverless plugins globally
            The AWS region set to 'eu-west-1'.
            use plugin serverless-python-requirements:
                custom:
                pythonRequirements:
                    dockerizePip: true

    3- .env File:
        Construct a .env.template file in the base directory, housing the necessary environment variables for the serverless.yml file.   
    """

    # print the prompt in green color
    print("\033[92m" + prompt + "\033[0m")

    # call openai api with this prompt
    filepaths_string = generate_response(
        """You are an AI developer who is trying to write a program that will generate code for the user based on their intent.
        
        When given their intent, create a complete, exhaustive list of filepaths that the user would write to make the program.
        
        only list the filepaths you would write, and return them as a python list of strings. 
        do not add any other explanation, only return a python list of strings.
    """,
        prompt,
    )

    print(filepaths_string)

    # parse the result into a python list
    list_actual = []

    try:
        list_actual = ast.literal_eval(filepaths_string)

        # if shared_dependencies.md is there, read it in, else set it to None
        shared_dependencies = None
        if os.path.exists("shared_dependencies.md"):
            with open("shared_dependencies.md", "r") as shared_dependencies_file:
                shared_dependencies = shared_dependencies_file.read()

        if args.f is not None :
            ## update one file 
            print("file", args.f )
            filename, filecode = generate_file(args.f , filepaths_string=filepaths_string, shared_dependencies=shared_dependencies, prompt=prompt)
            write_file(filename, filecode, directory)
        else:
            ## generate complete codebase
            clean_dir(directory)

            # understand shared dependencies
            shared_dependencies = generate_response(
                """You are an AI developer who is trying to write a program that will generate code for the user based on their intent.
                
            In response to the user's prompt:

            ---
            the app is: {prompt}
            ---
            
            the files we have decided to generate are: {filepaths_string}

            Now that we have a list of files, we need to understand what dependencies they share.
            Please name and briefly describe what is shared between the files we are generating, including exported variables, data schemas, id names of every DOM elements that javascript functions will use, message names, and function names.
            Exclusively focus on the names of the shared dependencies, and do not add any other explanation.
            """,
                prompt,
            )
            print(shared_dependencies)
            
            # write shared dependencies as a md file inside the generated directory
            write_file("shared_dependencies.md", shared_dependencies, directory)
            
            # Existing for loop
            files_to_generate = []
            for filename in list_actual:
                filename, filecode = generate_file(filename, filepaths_string=filepaths_string, shared_dependencies=shared_dependencies, prompt=prompt)
                write_file(filename, filecode, directory)

    except ValueError:
        print("Failed to parse result: " + filepaths_string)