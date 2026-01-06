"""Tests for notifications module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from api_monitor.notifier import NotificationConfig, NotificationService, create_notifier_from_config
from api_monitor.checker import CheckResult


class TestNotificationConfig:
    """Tests for NotificationConfig."""
    
    def test_notification_config_defaults(self):
        """Test default values."""
        config = NotificationConfig()
        assert config.email_enabled is False
        assert config.push_enabled is False
        assert config.notify_on_failure is True
        assert config.notify_on_recovery is True
        assert config.email_to == []
    
    def test_notification_config_custom(self):
        """Test custom configuration."""
        config = NotificationConfig(
            email_enabled=True,
            email_smtp_host='smtp.gmail.com',
            email_to=['test@example.com']
        )
        assert config.email_enabled is True
        assert config.email_smtp_host == 'smtp.gmail.com'
        assert config.email_to == ['test@example.com']


class TestNotificationService:
    """Tests for NotificationService."""
    
    def test_should_notify_on_first_failure(self):
        """Test notification on first failure."""
        config = NotificationConfig(notify_on_failure=True)
        service = NotificationService(config)
        
        assert service.should_notify('API1', True) is True
        assert service.last_notified_state['API1'] is True
    
    def test_should_notify_on_recovery(self):
        """Test notification on recovery."""
        config = NotificationConfig(notify_on_recovery=True)
        service = NotificationService(config)
        
        # First failure
        service.should_notify('API1', True)
        # Then recovery
        assert service.should_notify('API1', False) is True
        assert service.last_notified_state['API1'] is False
    
    def test_should_not_notify_on_same_state(self):
        """Test no notification on same state."""
        config = NotificationConfig(notify_on_all_failures=False)
        service = NotificationService(config)
        
        # First failure
        assert service.should_notify('API1', True) is True
        # Same failure again
        assert service.should_notify('API1', True) is False
    
    def test_should_notify_on_all_failures(self):
        """Test notification on every failure."""
        config = NotificationConfig(notify_on_all_failures=True)
        service = NotificationService(config)
        
        # Every failure should notify
        assert service.should_notify('API1', True) is True
        assert service.should_notify('API1', True) is True
        assert service.should_notify('API1', True) is True
    
    @patch('api_monitor.notifier.smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        """Test successful email sending."""
        config = NotificationConfig(
            email_enabled=True,
            email_smtp_host='smtp.gmail.com',
            email_smtp_port=587,
            email_smtp_user='user@gmail.com',
            email_smtp_password='password',
            email_from='from@example.com',
            email_to=['to@example.com']
        )
        service = NotificationService(config)
        
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = service.send_email('Test Subject', 'Test Body')
        
        assert result is True
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('user@gmail.com', 'password')
        mock_server.send_message.assert_called_once()
    
    def test_send_email_disabled(self):
        """Test email sending when notifications disabled."""
        config = NotificationConfig(email_enabled=False)
        service = NotificationService(config)
        
        result = service.send_email('Test', 'Body')
        assert result is False
    
    def test_format_email_body(self):
        """Test email body formatting."""
        config = NotificationConfig()
        service = NotificationService(config)
        
        results = [
            CheckResult('API1', 'https://api1.com', 200, 100.5, True),
            CheckResult('API2', 'https://api2.com', None, 50.0, False, error='Connection error')
        ]
        
        text_body, html_body = service.format_email_body(results)
        
        assert 'API1' in text_body
        assert 'API2' in text_body
        assert 'Connection error' in text_body
        assert '<html>' in html_body
        assert 'API1' in html_body
        assert 'API2' in html_body
    
    def test_notify_with_failures(self):
        """Test notification with failures."""
        config = NotificationConfig(
            email_enabled=True,
            email_smtp_host='smtp.gmail.com',
            email_to=['test@example.com'],
            notify_on_failure=True
        )
        service = NotificationService(config)
        
        results = [
            CheckResult('API1', 'https://api1.com', None, 50.0, False, error='Error')
        ]
        
        with patch.object(service, 'send_email', return_value=True):
            result = service.notify(results)
            assert result is True
    
    def test_notify_no_failures(self):
        """Test no notification when no failures."""
        config = NotificationConfig(notify_on_failure=True, notify_on_recovery=False)
        service = NotificationService(config)
        
        results = [
            CheckResult('API1', 'https://api1.com', 200, 100.5, True)
        ]
        
        result = service.notify(results)
        assert result is False


class TestCreateNotifier:
    """Tests for create_notifier_from_config."""
    
    def test_create_notifier_with_email(self):
        """Test creating notifier with email."""
        config_data = {
            'email': {
                'enabled': True,
                'smtp_host': 'smtp.gmail.com',
                'to': ['test@example.com']
            }
        }
        
        notifier = create_notifier_from_config(config_data)
        assert notifier is not None
        assert notifier.config.email_enabled is True
    
    def test_create_notifier_disabled(self):
        """Test creating notifier when notifications disabled."""
        config_data = {
            'email': {'enabled': False},
            'push': {'enabled': False}
        }
        
        notifier = create_notifier_from_config(config_data)
        assert notifier is None
    
    def test_create_notifier_empty_config(self):
        """Test creating notifier with empty config."""
        notifier = create_notifier_from_config(None)
        assert notifier is None
        
        notifier = create_notifier_from_config({})
        assert notifier is None

