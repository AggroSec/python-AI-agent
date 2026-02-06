import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_dir_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(absolute_dir_path, file_path))
        is_valid_target_file_path = os.path.commonpath([absolute_dir_path, target_file_path]) == absolute_dir_path

        if not is_valid_target_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]

        if args != None:
            command.extend(args)

        results = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output_string = ""

        if results.returncode != 0:
            output_string += f"Process exited with code {results.returncode}\n"

        if not results.stderr and not results.stdout:
            output_string += f"No output produced\n"
        else:
            if results.stdout:
                output_string += f"STDOUT:\n{results.stdout}"
            if results.stderr:
                output_string += f"STDERR:\n{results.stderr}"

        return output_string

    except Exception as e:
        return f"Error: {e}"