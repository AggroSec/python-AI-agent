import os
from config import MAX_CHARS
from google import genai
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        absolute_dir_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(absolute_dir_path, file_path))
        is_valid_target_file_path = os.path.commonpath([absolute_dir_path, target_file_path]) == absolute_dir_path

        if not is_valid_target_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file = open(target_file_path, "r")
        file_contents = file.read(MAX_CHARS)
        if file.read(1):
            file_contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return file_contents

    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Used to read the contents of a specified file relative to the working directory, truncating at constant variable of MAX_CHARS (currently set to 10000)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the specified file relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)