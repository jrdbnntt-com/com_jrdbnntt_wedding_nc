import os
from configparser import ConfigParser
from pathlib import Path

# Read in environment configuration settings
os.environ.setdefault('RUNTIME_ENVIRONMENT', 'DEVELOPMENT')
RUNTIME_ENVIRONMENT = os.environ.get('RUNTIME_ENVIRONMENT')
print("Configuring for runtime: ", RUNTIME_ENVIRONMENT)

# Read config for environment
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_SECTION_DJANGO = 'django'
config = ConfigParser()
CONFIG_FILE_DIR = Path(BASE_DIR, 'com_jrdbnntt_wedding/config')
CONFIG_FILES = {
    'base': Path(CONFIG_FILE_DIR, 'base.cfg'),
    'PRODUCTION': Path(CONFIG_FILE_DIR, 'production.cfg'),
    'TEST': Path(CONFIG_FILE_DIR, 'test.cfg'),
    'DEVELOPMENT': Path(CONFIG_FILE_DIR, 'development.cfg')
}
config_file = CONFIG_FILES[RUNTIME_ENVIRONMENT]
print("Loading base config file: ", CONFIG_FILES['base'])
if not config_file.exists():
    raise EnvironmentError("Missing config file: ", config_file.absolute())
config.read(CONFIG_FILES['base'])
if RUNTIME_ENVIRONMENT in CONFIG_FILES.keys():
    config_file = CONFIG_FILES[RUNTIME_ENVIRONMENT]
    print("Loading {} environment config file: {}".format(RUNTIME_ENVIRONMENT, config_file.absolute()))
    if not config_file.exists():
        raise EnvironmentError("Missing config file: ", config_file.absolute())
    config.read(config_file)
else:
    raise EnvironmentError('Invalid RUNTIME_ENVIRONMENT')
