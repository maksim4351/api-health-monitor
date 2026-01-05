"""Module for loading configuration from YAML."""

import yaml
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class APIConfig:
    """Configuration for a single API check."""
    name: str
    url: str
    method: str = "GET"
    timeout: float = 5.0
    expected_status: int = 200
    headers: Dict[str, str] = None

    def __post_init__(self):
        if self.headers is None:
            self.headers = {}


@dataclass
class Config:
    """Main monitoring configuration."""
    apis: List[APIConfig]
    output_format: str = "table"  # table, json, csv
    log_file: str = None
    interval: int = None  # for periodic checks (seconds)
    notifications: Dict[str, Any] = None  # notification settings


def load_config(config_path: str) -> Config:
    """
    Loads configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Config object with loaded data
        
    Raises:
        FileNotFoundError: If file not found
        yaml.YAMLError: If file contains invalid YAML
        ValueError: If configuration is incorrect
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"YAML parsing error: {e}")
    
    if not data or 'apis' not in data:
        raise ValueError("Configuration must contain 'apis' section")
    
    if not isinstance(data['apis'], list):
        raise ValueError("'apis' section must be a list")
    
    if len(data['apis']) == 0:
        raise ValueError("API list cannot be empty")
    
    # Output format validation
    valid_formats = ['table', 'json', 'csv', 'html']
    output_format = data.get('output_format', 'table')
    if output_format not in valid_formats:
        raise ValueError(f"Invalid output format: {output_format}. Valid: {', '.join(valid_formats)}")
    
    apis = []
    for idx, api_data in enumerate(data['apis']):
        if not isinstance(api_data, dict):
            raise ValueError(f"API #{idx + 1}: must be an object (dictionary)")
        
        if 'name' not in api_data or 'url' not in api_data:
            raise ValueError(f"API #{idx + 1}: must have 'name' and 'url'")
        
        # Basic URL validation
        url = api_data['url']
        if not isinstance(url, str) or not url.strip():
            raise ValueError(f"API '{api_data.get('name', 'unknown')}': URL must be a non-empty string")
        
        # Timeout validation
        timeout = api_data.get('timeout', 5.0)
        try:
            timeout = float(timeout)
        except (ValueError, TypeError):
            raise ValueError(f"API '{api_data['name']}': timeout must be a number")
        if timeout <= 0:
            raise ValueError(f"API '{api_data['name']}': timeout must be a positive number")
        
        # Expected status validation
        expected_status = api_data.get('expected_status', 200)
        try:
            expected_status = int(expected_status)
        except (ValueError, TypeError):
            raise ValueError(f"API '{api_data['name']}': expected_status must be an integer")
        if expected_status < 100 or expected_status >= 600:
            raise ValueError(f"API '{api_data['name']}': expected_status must be a valid HTTP status (100-599)")
        
        # Headers validation
        headers = api_data.get('headers', {})
        if headers is not None and not isinstance(headers, dict):
            raise ValueError(f"API '{api_data['name']}': headers must be a dictionary")
        
        api_config = APIConfig(
            name=api_data['name'],
            url=url.strip(),
            method=api_data.get('method', 'GET'),
            timeout=timeout,
            expected_status=expected_status,
            headers=headers or {}
        )
        apis.append(api_config)
    
    return Config(
        apis=apis,
        output_format=output_format,
        log_file=data.get('log_file'),
        interval=data.get('interval'),
        notifications=data.get('notifications')
    )


def save_config(config: Config, config_path: str) -> None:
    """
    Saves configuration to YAML file.
    
    Args:
        config: Config object to save
        config_path: Path to configuration file
        
    Raises:
        IOError: If failed to write file
    """
    path = Path(config_path)
    
    # Create data structure for YAML
    data = {
        'output_format': config.output_format,
        'apis': []
    }
    
    if config.log_file:
        data['log_file'] = config.log_file
    
    if config.interval:
        data['interval'] = config.interval
    
    if config.notifications:
        data['notifications'] = config.notifications
    
    # Convert APIConfig to dictionaries
    for api in config.apis:
        api_dict = {
            'name': api.name,
            'url': api.url,
            'method': api.method,
            'timeout': api.timeout,
            'expected_status': api.expected_status
        }
        
        # Add headers only if they are not empty
        if api.headers:
            api_dict['headers'] = api.headers
        
        data['apis'].append(api_dict)
    
    # Save to YAML
    try:
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    except IOError as e:
        raise IOError(f"Failed to save configuration: {e}")


