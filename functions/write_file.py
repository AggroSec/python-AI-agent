import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        absolute_dir_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(absolute_dir_path, file_path))
        is_valid_target_file_path = os.path.commonpath([absolute_dir_path, target_file_path]) == absolute_dir_path

        if not is_valid_target_file_path:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        file = open(target_file_path, "w")
        file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Used to write to a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the specified file relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents that are to be written into the specified file"
            )
        },
        required=["file_path", "content"]
    ),
)