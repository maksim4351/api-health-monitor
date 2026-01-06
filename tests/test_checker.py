"""Tests for API checking module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from api_monitor.checker import check_api, check_all_apis, CheckResult
from api_monitor.loader import APIConfig


class TestCheckAPI:
    """Tests for check_api function."""
    
    @patch('api_monitor.checker.requests.request')
    def test_check_api_success(self, mock_request):
        """Test successful request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response
        
        api_config = APIConfig(
            name="Test API",
            url="https://example.com",
            expected_status=200
        )
        
        result = check_api(api_config)
        
        assert result.success is True
        assert result.status_code == 200
        assert result.error is None
        assert result.timeout is False
        assert result.latency_ms >= 0
        mock_request.assert_called_once_with(
            method='GET',
            url='https://example.com',
            headers={},
            timeout=5.0
        )
    
    @patch('api_monitor.checker.requests.request')
    def test_check_api_wrong_status(self, mock_request):
        """Test wrong status code."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_request.return_value = mock_response
        
        api_config = APIConfig(
            name="Test API",
            url="https://example.com",
            expected_status=200
        )
        
        result = check_api(api_config)
        
        assert result.success is False
        assert result.status_code == 404
        assert result.error is None
        assert result.timeout is False
    
    @patch('api_monitor.checker.requests.request')
    def test_check_api_timeout(self, mock_request):
        """Test timeout handling."""
        import requests
        mock_request.side_effect = requests.exceptions.Timeout()
        
        api_config = APIConfig(
            name="Test API",
            url="https://example.com",
            timeout=1.0
        )
        
        result = check_api(api_config)
        
        assert result.success is False
        assert result.status_code is None
        assert "Timeout" in result.error
        assert result.timeout is True
        assert result.latency_ms >= 0
    
    @patch('api_monitor.checker.requests.request')
    def test_check_api_connection_error(self, mock_request):
        """Test connection error handling."""
        import requests
        mock_request.side_effect = requests.exceptions.ConnectionError()
        
        api_config = APIConfig(
            name="Test API",
            url="https://example.com"
        )
        
        result = check_api(api_config)
        
        assert result.success is False
        assert result.status_code is None
        assert result.error == "Connection error"
        assert result.timeout is False
    
    @patch('api_monitor.checker.requests.request')
    def test_check_api_request_exception(self, mock_request):
        """Test RequestException handling."""
        import requests
        mock_request.side_effect = requests.exceptions.RequestException("Test error")
        
        api_config = APIConfig(
            name="Test API",
            url="https://example.com"
        )
        
        result = check_api(api_config)
        
        assert result.success is False
        assert result.status_code is None
        assert "Test error" in result.error
        assert result.timeout is False
    
    @patch('api_monitor.checker.requests.request')
    def test_check_api_unexpected_error(self, mock_request):
        """Test unexpected error handling."""
        mock_request.side_effect = ValueError("Unexpected error")
        
        api_config = APIConfig(
            name="Test API",
            url="https://example.com"
        )
        
        result = check_api(api_config)
        
        assert result.success is False
        assert result.status_code is None
        assert "Unexpected error" in result.error
        assert result.timeout is False
    
    @patch('api_monitor.checker.requests.request')
    def test_check_api_with_headers(self, mock_request):
        """Test request with headers."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response
        
        api_config = APIConfig(
            name="Test API",
            url="https://example.com",
            headers={"User-Agent": "test"}
        )
        
        result = check_api(api_config)
        
        assert result.success is True
        mock_request.assert_called_once_with(
            method='GET',
            url='https://example.com',
            headers={"User-Agent": "test"},
            timeout=5.0
        )
    
    @patch('api_monitor.checker.requests.request')
    def test_check_api_custom_method(self, mock_request):
        """Test custom HTTP method."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_request.return_value = mock_response
        
        api_config = APIConfig(
            name="Test API",
            url="https://example.com",
            method="POST",
            expected_status=201
        )
        
        result = check_api(api_config)
        
        assert result.success is True
        assert result.status_code == 201
        mock_request.assert_called_once_with(
            method='POST',
            url='https://example.com',
            headers={},
            timeout=5.0
        )


class TestCheckAllAPIs:
    """Tests for check_all_apis function."""
    
    @patch('api_monitor.checker.check_api')
    def test_check_all_apis(self, mock_check_api):
        """Test handling multiple APIs."""
        mock_check_api.side_effect = [
            CheckResult("API 1", "https://api1.com", 200, 100.0, True),
            CheckResult("API 2", "https://api2.com", 404, 150.0, False),
            CheckResult("API 3", "https://api3.com", 200, 200.0, True)
        ]
        
        api_configs = [
            APIConfig("API 1", "https://api1.com"),
            APIConfig("API 2", "https://api2.com"),
            APIConfig("API 3", "https://api3.com")
        ]
        
        results = check_all_apis(api_configs)
        
        assert len(results) == 3
        assert mock_check_api.call_count == 3
        assert results[0].name == "API 1"
        assert results[1].name == "API 2"
        assert results[2].name == "API 3"
    
    @patch('api_monitor.checker.check_api')
    def test_check_all_apis_empty_list(self, mock_check_api):
        """Test handling empty list."""
        results = check_all_apis([])
        
        assert len(results) == 0
        mock_check_api.assert_not_called()

