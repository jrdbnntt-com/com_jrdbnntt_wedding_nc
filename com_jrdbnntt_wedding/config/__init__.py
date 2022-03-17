import os
from configparser import ConfigParser
from pathlib import Path

os.environ.setdefault('RUNTIME_ENVIRONMENT', 'DEVELOPMENT')
RUNTIME_ENVIRONMENT = os.environ.get('RUNTIME_ENVIRONMENT')
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE_DIR = Path(BASE_DIR, 'com_jrdbnntt_wedding/config')
CONFIG_FILES = {
    'base': Path(CONFIG_FILE_DIR, 'base.cfg'),
    'PRODUCTION': Path(CONFIG_FILE_DIR, 'production.cfg'),
    'TEST': Path(CONFIG_FILE_DIR, 'test.cfg'),
    'DEVELOPMENT': Path(CONFIG_FILE_DIR, 'development.cfg')
}

# Sections
SECTION_DJANGO = 'django'
SECTION_RECAPTCHA = 'recaptcha'
SECTION_EMAIL = 'email'
SECTION_EVENT_DETAILS = 'event_details'
SECTION_TASKS = 'tasks'
SECTION_DATABASE = 'database'


def load(runtime_environment_override=None) -> ConfigParser:
    config = ConfigParser()

    # Read in environment configuration settings
    active_runtime_environment = RUNTIME_ENVIRONMENT
    if runtime_environment_override is not None:
        active_runtime_environment = runtime_environment_override

    print("CONFIG: Configuring for runtime: ", active_runtime_environment)

    config_file = CONFIG_FILES[active_runtime_environment]
    print("CONFIG: Loading base config file: ", CONFIG_FILES['base'])
    if not config_file.exists():
        raise EnvironmentError("Missing config file: ", config_file.absolute())
    config.read(CONFIG_FILES['base'])
    if active_runtime_environment in CONFIG_FILES.keys():
        config_file = CONFIG_FILES[active_runtime_environment]
        print(
            "CONFIG: Loading {} environment config file: {}".format(active_runtime_environment, config_file.absolute()))
        if not config_file.exists():
            raise EnvironmentError("Missing config file: ", config_file.absolute())
        config.read(config_file)
    else:
        raise EnvironmentError('Invalid RUNTIME_ENVIRONMENT')
    return config


def assert_defined(config_section: str, config_key: str, value: str):
    if value is None or value == "":
        raise AssertionError("Invalid configuration: Missing {}.{}".format(config_section, config_key))
