from configparser import ConfigParser, SectionProxy
from logging import config
from typing import Dict
from pathlib import Path

# filepath to .ini file for auth credentials
p = Path('.') / 'nem/settings/nem.ini'
config_path = p.absolute()
print(config_path)

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

if __name__ == '__main__':
    print(p)
    print(config_dict(section="FILEPATHS"))