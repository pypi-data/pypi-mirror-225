import yaml
import os


def loadConfig():
    config = {}
    config_file = 'swxtools.cfg'
    if not os.path.isfile(config_file):
        config_file = os.path.expanduser('~/.swxtools.cfg')
    if os.path.isfile(config_file):
        config = yaml.safe_load(open(config_file))
        return config, config_file
    else:
        raise FileNotFoundError('No configuration file found')


config, config_file = loadConfig()
