import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    try:
        target_file = os.path.abspath(os.path.join(working_directory, file_path))
        if not target_file.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(target_file):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        result = subprocess.run(["python3", target_file], timeout=30, capture_output=True, text=True, cwd=working_directory)
        final_output = f"STDOUT: {result.stdout} \nSTDERR: {result.stderr}"
        if result.returncode != 0:
            return final_output + f"\nProcess exited with code {result.returncode} "
        if result.stdout == "" and result.stderr == "":
            return f"No output produced"
        
        return final_output
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
