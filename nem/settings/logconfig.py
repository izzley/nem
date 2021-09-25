"""
logging yaml config class called throughout nem project
"""

import logging
import logging.config
import yaml
from nem.settings import config_dict
from pathlib import Path
import nem
from pkgutil import get_data

# NOTE: should be logging.config.fileconfig rather than custom class instance
# how to dynamically reference logconfig.yaml without being cumbersome
# https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig

class RootLoggerConf:
    """
    Read logconfig.yaml file in settings
    """

    # non relative filepath to local logconfig.py
    # @TODO fix project log - https://gist.github.com/kingspp/9451566a5555fb022215ca2b7b802f19
    logyaml = get_data("nem", "settings/logconfig.yaml")
    # local_logpath = config_dict(section="FILEPATHS")
    # path = Path(local_logpath["logconfig"])

    # def readyaml(self):
        # with open(self.logyaml, "r") as f:
    config = yaml.safe_load(logyaml)
    logging.config.dictConfig(config)

if __name__ == "__main__":
    f = get_data("nem", "settings/logconfig.yaml")
    # LoggingDict().readyaml()
    RootLoggerConf()
    logger = logging.getLogger(__name__)
    logger.debug("test")
