import os

def get_file_content(working_directory, file_path):
    try:
        target_file = os.path.abspath(os.path.join(working_directory, file_path))
        if not target_file.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        MAX_CHARS = 10000

        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) == 10000:
            return file_content_string + f'[...File "{file_path}" truncated at 10000 characters]'

        return file_content_string
    except Exception as e:
        return f"Error listing files: {e}"
