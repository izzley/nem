"""
logging yaml config class called throughout nem project
"""

import logging
import logging.config
import yaml
from nem.settings import config_dict
from pathlib import Path

class LoggingDict:
    """
    Read logconfig.yaml file in settings
    """

    # non relative filepath to local logconfig.py
    local_logpath = config_dict(section="FILEPATHS")
    path = Path(local_logpath["logconfig"])

    def readyaml(self):
        with open(self.path, "r") as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)

if __name__ == "__main__":
    LoggingDict().readyaml()
    logging.debug("test")
