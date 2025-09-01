import os
import yaml
from pathlib import Path
import logging

class ConfigReader:
    _data = None

    @classmethod
    def _load_config(cls):
        """ Loads the configuration from a YAML file based on the environment variable TEST_ENV.
        The default environment is 'qa' if TEST_ENV is not set.
        """
        env = os.getenv("TEST_ENV", "qa")  # default to qa

        # Path(__file__).resolve() - gets the absolute path of the current file
        root_dir = Path(__file__).resolve().parent.parent

        # With pathlib, the / operator is overloaded to mean “join paths”, not a literal slash.
        # The resulting Path object will use the correct separator for the OS.
        config_file_path = root_dir / 'configs' / 'config.yaml'

        with open(config_file_path, "r") as f:
            all_envs = yaml.safe_load(f)
            #print(all_envs)
        cls._data = all_envs[env]
        #print(cls._data)

    @classmethod
    def get_config(cls, key):
        if cls._data is None:
            _logger = logging.getLogger(__name__)
            _logger.debug("Configuration not loaded. Loading now...")
            cls._load_config()
        return cls._data.get(key)



