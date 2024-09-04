import yaml

def load_language_config(file_path):
    """
    Load the language config file
    :param file_path: a string. The path of the file about language settings
    :return config: a dictionary. The language settings
    """
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def infer_language(file_path, config):
    """
    looking up the programming language associated with the file extension of the provided file name.
    :param file_path: a string. The path of the file from which to infer the language
    :param config: a dictionary. The language settings
    :return language: a string. The inferred programming language, or 'GENERIC' if the extension is not recognized
    """
    ext = file_path.split('.')[-1].lower()
    for language, settings in config.items():
        extensions = settings['extension']
        if isinstance(extensions, str):
            if ext == extensions.lower():
                return language
        elif ext in [x.lower() for x in extensions]:
            return language
    return 'GENERIC'
