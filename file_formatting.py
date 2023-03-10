import os

def format_files(description, filepaths, debug_or_improve='debug'):
    """
    Formats a list of files as a string.

    :param error_description: Description of the error to be reported.
    :type error_description: str
    :param filepaths: A list of file paths.
    :type filepaths: list
    :return: A string with the contents of each file and its name formatted.
    :rtype: str
    """
    if debug_or_improve=='debug':
      files_str = f"""I am going to give you an error description, and files in the format listed. Please fix the bug.
      ### Error Description 
      CODE ERROR

      ### file1
      CODE HERE

      ### file 2
      CODE HERE

      ### Error Description
      {description}\n\nFiles giving the error:\n\n"""
    else:
      files_str = f"""Please update any of the files so I can get what I want to happen:
      ### What I'd like to happen 
      WHAT I WANT TO HAPPEN

      ### file1
      CODE HERE

      ### file 2
      CODE HERE

      ### What I'd like to happen
      {description}\n\nCurrent Files:\n\n"""

    for filepath in filepaths:
        filename = os.path.basename(filepath)
        with open(filepath, 'r') as f:
            contents = f.read()
        files_str += f'### {filename}\n{contents}\n'
    return files_str

# Format the files as a string
error = """Traceback (most recent call last):
  File "/Users/kevin/Desktop/Github/gptdebug/venv/lib/python3.8/site-packages/openai/openai_object.py", line 59, in __getattr__
    return self[k]
KeyError: 'conversation_id'

During handling of the above exception, another exception occurred:"""

what_i_want = """
The issue with the current code is that it finishes with mean= rather than mean=bmi. How cann this be fixed?
"""

specific="Please only show the code after this section in the html"

# Set the list of file paths to upload
filepaths = ['/Users/kevin/Desktop/Github/openai-quickstart-python/app.py',
             '/Users/kevin/Desktop/Github/openai-quickstart-python/templates/index.html']

# files_str = format_files(error, filepaths, debug_or_improve='debug')
files_str = format_files(what_i_want, filepaths, debug_or_improve='improve')

# output to text file
with open("output.txt", 'w') as f:
    f.write(files_str)



# Set the API endpoint for uploading files
# import requests
# upload_endpoint = 'https://api.chatgpt.com/upload'

# Send a POST request to the ChatGPT API endpoint with the formatted files as the request body
# response = requests.post(upload_endpoint, data=files_str)

# # Check if the upload was successful
# if response.status_code == 200:
#     print('Files uploaded successfully')
# else:
#     print(f'Error uploading files: {response.status_code}')
