import errno
from pathlib import Path
from datetime import datetime
import logging
import os

LOG_BASE_DIR = Path(Path(__file__).resolve().parent.parent, 'logs').resolve()


def format_date_dirname(dt: datetime) -> str:
    return "%4d-%02d-%02d/%02d-%02d-%02d-%d" % (
        dt.year,
        dt.month,
        dt.day,
        dt.hour,
        dt.minute,
        dt.second,
        dt.microsecond
    )


def new_log_file(dir: Path, name: str) -> str:
    path = Path(dir, name + '.log').resolve()
    file = open(path, 'x')
    file.close()
    return str(path)


def build_django_config(debug=False):
    # Make a fresh log dir for the run
    os.makedirs(LOG_BASE_DIR, exist_ok=True)
    run_log_base_dir = Path(LOG_BASE_DIR, format_date_dirname(datetime.now())).resolve()
    os.makedirs(run_log_base_dir)

    # Set log dir shortcut to new dir
    latest_link = Path(LOG_BASE_DIR, 'latest')
    try:
        os.symlink(run_log_base_dir, latest_link, target_is_directory=True)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(latest_link)
            os.symlink(run_log_base_dir, latest_link)
        else:
            raise e

    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[{asctime} {levelname} {name}] {message}',
                'style': '{',
            }
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'console': {
                'level': logging.INFO,
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            },
            'file_full': {
                'level': logging.DEBUG,
                'formatter': 'default',
                'class': 'logging.FileHandler',
                'filename': new_log_file(run_log_base_dir, 'full'),
            },
            'file_website': {
                'level': logging.DEBUG,
                'formatter': 'default',
                'class': 'logging.FileHandler',
                'filename': new_log_file(run_log_base_dir, 'website'),
            },
        },
        'loggers': {
            'website': {
                'handlers': ['console', 'file_full', 'file_website'],
                'level': logging.DEBUG if debug else logging.INFO
            },
            'django': {
                'handlers': ['console', 'file_full'],
                'level': logging.DEBUG if debug else logging.WARN,
                'propagate': True,
            },
        }
    }