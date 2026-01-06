"""Tests for CLI module."""

import pytest
import sys
import tempfile
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock
from api_monitor.cli import run_command, setup_logging


class TestRunCommand:
    """Tests for run_command function."""
    
    @pytest.fixture
    def valid_config_file(self):
        """Creates temporary valid configuration file."""
        config_data = {
            'apis': [
                {
                    'name': 'Test API',
                    'url': 'https://httpbin.org/status/200',
                    'expected_status': 200
                }
            ],
            'output_format': 'table'
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        yield config_path
        
        Path(config_path).unlink()
    
    @patch('api_monitor.cli.check_all_apis')
    @patch('api_monitor.cli.load_config')
    @patch('api_monitor.cli.print_report')
    def test_run_command_success(self, mock_print, mock_load, mock_check, valid_config_file):
        """Test successful command execution."""
        from api_monitor.loader import Config, APIConfig
        from api_monitor.checker import CheckResult
        
        mock_config = Config(
            apis=[APIConfig("Test API", "https://example.com")],
            output_format='table'
        )
        mock_load.return_value = mock_config
        
        mock_check.return_value = [
            CheckResult("Test API", "https://example.com", 200, 100.0, True)
        ]
        
        exit_code = run_command(valid_config_file)
        
        assert exit_code == 0
        mock_load.assert_called_once()
        mock_check.assert_called_once()
        mock_print.assert_called_once()
    
    def test_run_command_file_not_found(self):
        """Test handling missing file."""
        exit_code = run_command("nonexistent.yaml")
        assert exit_code == 1
    
    @patch('api_monitor.cli.load_config')
    def test_run_command_invalid_config(self, mock_load):
        """Test handling invalid configuration."""
        mock_load.side_effect = ValueError("Invalid config")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("test")
            config_path = f.name
        
        try:
            exit_code = run_command(config_path)
            assert exit_code == 1
        finally:
            Path(config_path).unlink()
    
    @patch('api_monitor.cli.load_config')
    @patch('api_monitor.cli.check_all_apis')
    @patch('api_monitor.cli.print_report')
    def test_run_command_custom_format(self, mock_print, mock_check, mock_load, valid_config_file):
        """Test using custom format."""
        from api_monitor.loader import Config, APIConfig
        from api_monitor.checker import CheckResult
        
        mock_config = Config(
            apis=[APIConfig("Test API", "https://example.com")],
            output_format='table'
        )
        mock_load.return_value = mock_config
        
        mock_check.return_value = [
            CheckResult("Test API", "https://example.com", 200, 100.0, True)
        ]
        
        exit_code = run_command(valid_config_file, output_format='json')
        
        assert exit_code == 0
        # Check that custom format was passed
        call_args = mock_print.call_args
        assert call_args[0][1] == 'json'  # Second argument is format
    
    @patch('api_monitor.cli.load_config')
    @patch('api_monitor.cli.check_all_apis')
    @patch('api_monitor.cli.print_report')
    def test_run_command_invalid_format(self, mock_print, mock_check, mock_load, valid_config_file):
        """Test handling invalid format."""
        from api_monitor.loader import Config, APIConfig
        
        mock_config = Config(
            apis=[APIConfig("Test API", "https://example.com")],
            output_format='invalid'
        )
        mock_load.return_value = mock_config
        
        exit_code = run_command(valid_config_file)
        
        assert exit_code == 1


class TestSetupLogging:
    """Tests for setup_logging function."""
    
    def test_setup_logging_default(self):
        """Test default logging setup."""
        setup_logging()
        # If function executed without errors, test passed
    
    def test_setup_logging_with_file(self, tmp_path):
        """Test logging setup with file."""
        log_file = tmp_path / "test.log"
        setup_logging(str(log_file))
        # If function executed without errors, test passed

