import os


def get_config_folder_path():
    home_directory = os.path.expanduser("~")
    folder_path = os.path.join(home_directory, '.pastewin')
    return folder_path


def get_config_file_path(file='bucket'):
    return os.path.join(get_config_folder_path(), file)


def write_config_to_file(config_content, file='bucket'):
    config_folder = get_config_folder_path()

    if not os.path.exists(config_folder):
        os.makedirs(config_folder)

    with open(get_config_file_path(file), 'w') as config_file:
        config_file.write(config_content)


def read_config_from_file(file='bucket'):
    with open(get_config_file_path(file), 'r') as config_file:
        return config_file.read()
