import os

def get_files_info(working_directory, directory="."):
    try:
        absolute_dir_path = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(absolute_dir_path, directory))
        is_valid_target_directory = os.path.commonpath([absolute_dir_path, target_directory]) == absolute_dir_path

        if not is_valid_target_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        directory_list = os.listdir(target_directory)
        directory_info = []

        for item in directory_list:
            full_path = os.path.join(target_directory, item)
            if os.path.isdir(full_path):
                size = os.path.getsize(full_path)
                directory_info.append(f"- {item}: file_size={size} bytes, is_dir=True")
            elif os.path.isfile(full_path):
                size = os.path.getsize(full_path)
                directory_info.append(f"- {item}: file_size={size} bytes, is_dir=False")

        

        return "\n".join(directory_info)
    except Exception as e:
        return f"Error: {e}"

