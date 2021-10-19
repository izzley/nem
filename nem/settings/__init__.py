from configparser import ConfigParser, SectionProxy
from logging import config
from typing import Dict, Optional
from pathlib import Path
from pkgutil import get_data
from nem.utils.proc import running_as_scrapy
import yaml
import logging


# setup root logger
def logroot() -> Optional[dict]:
    """
    Logger instance from yaml file
    https://kingspp.github.io/design/2017/11/06/the-head-and-tail-of-logging.html
    """
    # path to yaml from project root
    logyaml = get_data("nem", "settings/logconfig.yaml")
    config = yaml.safe_load(logyaml)
    # create logger instance
    logging.config.dictConfig(config)

LOGGING_CONFIG = logroot()

logger = logging.getLogger("Settings")
# filepath to .ini file for auth credentials
p = Path('.') / 'nem/settings/nem.ini'
config_path = p.absolute()
if not p.exists():
    logger.critical("nem.ini doesn't exist. Make one!")

def config_dict(filename: Path = config_path, section: str = None) -> Dict:
    """
    read ini file and return section dict. 
    """
    # create a parser and read file
    parser = ConfigParser()
    parser.read(filename)

    # Checks to see if section of parser exists
    if not parser.has_section(section):
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    params = parser.items(section)
    return {param[0]: param[1] for param in params}


# Opennem solution for silencing logger during scrapy
# if LOGGING_CONFIG and not running_as_scrapy():
#     # don't mess with scrapy logging

#     logging.config.dictConfig(LOGGING_CONFIG)

#     log_level = logging.getLevelName(settings.log_level)

#     # set root log level
#     logging.root.setLevel(log_level)

#     opennem_logger = logging.getLogger("opennem")
#     opennem_logger.setLevel(log_level)

#     # other misc loggers
#     logging.getLogger("PIL").setLevel(logging.ERROR)
# if __name__ == '__main__':
#     print(p)
#     print(config_dict(section="FILEPATHS"))
