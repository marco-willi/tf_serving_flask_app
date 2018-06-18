import os
import json


def get_env_var_setting(env_var_name, default_value):
    '''
    Returns specified environment variable value. If it does not exist,
    returns a default value

    :param env_var_name: environment variable name
    :param default_value: default value to be returned if a variable does not exist
    :return: environment variable value
    '''
    try:
        env_var_value = os.environ[env_var_name]
    except:
        env_var_value = default_value

    return env_var_value


def read_json(path_to_json):
    """ Read File """
    assert os.path.exists(path_to_json), \
        "Path: %s does not exist" % path_to_json

    try:
        with open(path_to_json, 'r') as f:
            data_dict = json.load(f)
    except Exception as e:
        raise ImportError('Failed to read Json:\n' + str(e))

    return data_dict
