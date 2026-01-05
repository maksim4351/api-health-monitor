"""Tests for configuration loading module."""

import pytest
import tempfile
import yaml
from pathlib import Path
from api_monitor.loader import load_config, APIConfig, Config


class TestAPIConfig:
    """Tests for APIConfig class."""
    
    def test_api_config_defaults(self):
        """Test default values."""
        config = APIConfig(name="Test", url="https://example.com")
        assert config.name == "Test"
        assert config.url == "https://example.com"
        assert config.method == "GET"
        assert config.timeout == 5.0
        assert config.expected_status == 200
        assert config.headers == {}
    
    def test_api_config_custom(self):
        """Test custom values."""
        headers = {"User-Agent": "test"}
        config = APIConfig(
            name="Test",
            url="https://example.com",
            method="POST",
            timeout=10.0,
            expected_status=201,
            headers=headers
        )
        assert config.method == "POST"
        assert config.timeout == 10.0
        assert config.expected_status == 201
        assert config.headers == headers


class TestLoadConfig:
    """Tests for load_config function."""
    
    def test_load_valid_config(self):
        """Test loading valid configuration."""
        config_data = {
            'apis': [
                {
                    'name': 'Test API',
                    'url': 'https://example.com',
                    'method': 'GET',
                    'timeout': 5.0,
                    'expected_status': 200
                }
            ],
            'output_format': 'json'
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            config = load_config(config_path)
            assert len(config.apis) == 1
            assert config.apis[0].name == 'Test API'
            assert config.apis[0].url == 'https://example.com'
            assert config.output_format == 'json'
        finally:
            Path(config_path).unlink()
    
    def test_load_config_defaults(self):
        """Test default values."""
        config_data = {
            'apis': [
                {
                    'name': 'Test API',
                    'url': 'https://example.com'
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            config = load_config(config_path)
            assert config.apis[0].method == 'GET'
            assert config.apis[0].timeout == 5.0
            assert config.apis[0].expected_status == 200
            assert config.output_format == 'table'
        finally:
            Path(config_path).unlink()
    
    def test_load_config_file_not_found(self):
        """Test handling missing file."""
        with pytest.raises(FileNotFoundError):
            load_config("nonexistent.yaml")
    
    def test_load_config_missing_apis(self):
        """Test handling missing apis section."""
        config_data = {'output_format': 'table'}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            with pytest.raises(ValueError, match="must contain 'apis' section"):
                load_config(config_path)
        finally:
            Path(config_path).unlink()
    
    def test_load_config_empty_apis(self):
        """Test handling empty API list."""
        config_data = {'apis': []}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            with pytest.raises(ValueError, match="cannot be empty"):
                load_config(config_path)
        finally:
            Path(config_path).unlink()
    
    def test_load_config_missing_name(self):
        """Test handling missing name field."""
        config_data = {
            'apis': [
                {'url': 'https://example.com'}
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            with pytest.raises(ValueError, match="must have 'name' and 'url'"):
                load_config(config_path)
        finally:
            Path(config_path).unlink()
    
    def test_load_config_missing_url(self):
        """Test handling missing url field."""
        config_data = {
            'apis': [
                {'name': 'Test API'}
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            with pytest.raises(ValueError, match="must have 'name' and 'url'"):
                load_config(config_path)
        finally:
            Path(config_path).unlink()
    
    def test_load_config_invalid_output_format(self):
        """Test handling invalid output format."""
        config_data = {
            'apis': [
                {'name': 'Test', 'url': 'https://example.com'}
            ],
            'output_format': 'invalid'
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            with pytest.raises(ValueError, match="Invalid output format"):
                load_config(config_path)
        finally:
            Path(config_path).unlink()
    
    def test_load_config_invalid_timeout(self):
        """Test handling invalid timeout."""
        config_data = {
            'apis': [
                {
                    'name': 'Test',
                    'url': 'https://example.com',
                    'timeout': -1
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            with pytest.raises(ValueError, match="timeout must be a positive number"):
                load_config(config_path)
        finally:
            Path(config_path).unlink()
    
    def test_load_config_invalid_status(self):
        """Test handling invalid expected_status."""
        config_data = {
            'apis': [
                {
                    'name': 'Test',
                    'url': 'https://example.com',
                    'expected_status': 999
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            with pytest.raises(ValueError, match="expected_status must be a valid HTTP status"):
                load_config(config_path)
        finally:
            Path(config_path).unlink()
    
    def test_load_config_invalid_yaml(self):
        """Test handling invalid YAML."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content: [")
            config_path = f.name
        
        try:
            with pytest.raises(ValueError, match="YAML parsing error"):
                load_config(config_path)
        finally:
            Path(config_path).unlink()
    
    def test_load_config_with_headers(self):
        """Test loading configuration with headers."""
        config_data = {
            'apis': [
                {
                    'name': 'Test API',
                    'url': 'https://example.com',
                    'headers': {
                        'User-Agent': 'test-agent',
                        'Authorization': 'Bearer token'
                    }
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            config = load_config(config_path)
            assert config.apis[0].headers['User-Agent'] == 'test-agent'
            assert config.apis[0].headers['Authorization'] == 'Bearer token'
        finally:
            Path(config_path).unlink()
    
    def test_load_config_multiple_apis(self):
        """Test loading multiple APIs."""
        config_data = {
            'apis': [
                {'name': 'API 1', 'url': 'https://api1.com'},
                {'name': 'API 2', 'url': 'https://api2.com'},
                {'name': 'API 3', 'url': 'https://api3.com'}
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            config = load_config(config_path)
            assert len(config.apis) == 3
            assert config.apis[0].name == 'API 1'
            assert config.apis[1].name == 'API 2'
            assert config.apis[2].name == 'API 3'
        finally:
            Path(config_path).unlink()

