"""
Configuration Reader Module
============================

Provides centralized configuration management for the test framework.
Loads environment-specific settings from YAML configuration files.

Features:
    - Multi-environment support (qa, uat, prod)
    - Environment variable based switching (TEST_ENV)
    - Lazy loading with singleton pattern
    - Sensitive data masking in logs

Configuration File:
    configs/config.yaml - Contains settings for all environments

Environment Variable:
    TEST_ENV - Set to 'qa', 'uat', or 'prod' (default: 'qa')

Example:
    >>> # Set environment
    >>> os.environ['TEST_ENV'] = 'qa'
    >>> 
    >>> # Get configuration values
    >>> url = ConfigReader.get_config('login_url')
    >>> browser = ConfigReader.get_config('browser')
"""

import os
import logging
from pathlib import Path
from typing import Any, Optional

import yaml

_logger = logging.getLogger(__name__)


class ConfigReader:
    """
    Singleton configuration reader for YAML-based settings.
    
    Loads configuration once on first access and caches it for
    subsequent calls. Supports multiple environments through
    the TEST_ENV environment variable.
    
    Class Attributes:
        _data: Cached configuration dictionary.
        _env: Current environment name.
        
    Example:
        >>> ConfigReader.get_config('login_url')
        'https://example.com/login'
        >>> ConfigReader.get_config('credentials')
        {'email': 'test@example.com', 'password': 'secret'}
    """
    
    _data: Optional[dict] = None
    _env: Optional[str] = None

    @classmethod
    def _load_config(cls) -> None:
        """
        Load configuration from YAML file based on TEST_ENV.
        
        Reads the config.yaml file and extracts the section
        corresponding to the current environment.
        
        Environment:
            TEST_ENV: Environment name (default: 'qa')
            
        Raises:
            FileNotFoundError: If config.yaml doesn't exist.
            KeyError: If the environment section is not found in config.
        """
        cls._env = os.getenv("TEST_ENV", "qa")
        root_dir = Path(__file__).resolve().parent.parent
        config_file_path = root_dir / 'configs' / 'config.yaml'

        _logger.info(f"ConfigReader: Loading configuration | Environment: {cls._env} | File: {config_file_path}")

        with open(config_file_path, "r") as f:
            all_envs = yaml.safe_load(f)

        cls._data = all_envs[cls._env]
        _logger.info(f"ConfigReader: Configuration loaded successfully | Environment: {cls._env} | Keys: {list(cls._data.keys())}")
        _logger.debug(f"ConfigReader: Config data: {cls._data}")

    @classmethod
    def get_config(cls, key: str) -> Any:
        """
        Get a configuration value by key.
        
        Lazy loads the configuration on first access.
        Masks sensitive data (passwords, credentials) in log output.
        
        Args:
            key: Configuration key to retrieve.
            
        Returns:
            The configuration value, or None if key not found.
            
        Example:
            >>> url = ConfigReader.get_config('login_url')
            >>> print(url)
            'https://example.com/login'
            
            >>> creds = ConfigReader.get_config('credentials')
            >>> print(creds['email'])
            'user@example.com'
        """
        if cls._data is None:
            _logger.debug("ConfigReader: Configuration not loaded. Loading now...")
            cls._load_config()

        value = cls._data.get(key)
        if value is None:
            _logger.warning(f"ConfigReader: Key '{key}' not found in {cls._env} config")
        else:
            # Mask sensitive data in logs
            if key in ('password', 'credentials'):
                _logger.debug(f"ConfigReader: Retrieved '{key}' = [MASKED]")
            else:
                _logger.debug(f"ConfigReader: Retrieved '{key}' = {value}")
        return value
