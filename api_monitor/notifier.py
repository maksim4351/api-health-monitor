"""Module for sending API status notifications."""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
from .checker import CheckResult


logger = logging.getLogger(__name__)


@dataclass
class NotificationConfig:
    """Notification configuration."""
    email_enabled: bool = False
    email_smtp_host: str = None
    email_smtp_port: int = 587
    email_smtp_user: str = None
    email_smtp_password: str = None
    email_from: str = None
    email_to: List[str] = None
    email_subject_prefix: str = "[API Monitor]"
    push_enabled: bool = False
    notify_on_failure: bool = True
    notify_on_recovery: bool = True
    notify_on_all_failures: bool = False  # Notify on every error or only on state change
    
    def __post_init__(self):
        if self.email_to is None:
            self.email_to = []


class NotificationService:
    """Service for sending notifications."""
    
    def __init__(self, config: NotificationConfig):
        """
        Initializes notification service.
        
        Args:
            config: Notification configuration
        """
        self.config = config
        self.last_notified_state: Dict[str, bool] = {}  # Last notification state for each API
    
    def should_notify(self, api_name: str, is_failed: bool) -> bool:
        """
        Determines if notification should be sent.
        
        Args:
            api_name: API name
            is_failed: Current state (True = error, False = success)
            
        Returns:
            True if notification should be sent
        """
        if not self.config.notify_on_failure and is_failed:
            return False
        
        if not self.config.notify_on_recovery and not is_failed:
            return False
        
        # If notify on every error
        if self.config.notify_on_all_failures and is_failed:
            return True
        
        # Notify only on state change
        last_state = self.last_notified_state.get(api_name)
        if last_state is None or last_state != is_failed:
            self.last_notified_state[api_name] = is_failed
            return True
        
        return False
    
    def send_email(self, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """
        Sends email notification.
        
        Args:
            subject: Email subject
            body: Email text
            html_body: HTML version of email (optional)
            
        Returns:
            True if sending successful, False otherwise
        """
        if not self.config.email_enabled:
            return False
        
        if not self.config.email_to:
            logger.warning("Email notifications enabled but no recipients specified")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"{self.config.email_subject_prefix} {subject}"
            msg['From'] = self.config.email_from or self.config.email_smtp_user
            msg['To'] = ', '.join(self.config.email_to)
            
            # Text version
            text_part = MIMEText(body, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # HTML version (if available)
            if html_body:
                html_part = MIMEText(html_body, 'html', 'utf-8')
                msg.attach(html_part)
            
            # Send
            with smtplib.SMTP(self.config.email_smtp_host, self.config.email_smtp_port) as server:
                server.starttls()
                if self.config.email_smtp_user and self.config.email_smtp_password:
                    server.login(self.config.email_smtp_user, self.config.email_smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email notification sent: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def format_email_body(self, results: List[CheckResult], is_recovery: bool = False) -> Tuple[str, str]:
        """
        Formats email notification body.
        
        Args:
            results: List of check results
            is_recovery: True if this is a recovery notification
            
        Returns:
            Tuple (text version, HTML version)
        """
        failed_apis = [r for r in results if not r.success]
        successful_apis = [r for r in results if r.success]
        
        if is_recovery:
            subject = "✅ APIs Recovered"
            status_text = "recovered"
        else:
            subject = "⚠️ API Issues Detected"
            status_text = "not working"
        
        # Text version
        text_lines = [
            f"API Monitoring Status",
            f"Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]
        
        if failed_apis:
            text_lines.append(f"❌ Failed APIs ({len(failed_apis)}):")
            for api in failed_apis:
                text_lines.append(f"  - {api.name} ({api.url})")
                text_lines.append(f"    Error: {api.error or 'Unknown error'}")
                if api.status_code:
                    text_lines.append(f"    HTTP code: {api.status_code}")
                text_lines.append("")
        
        if successful_apis:
            text_lines.append(f"✅ Working APIs ({len(successful_apis)}):")
            for api in successful_apis:
                text_lines.append(f"  - {api.name} ({api.url})")
                text_lines.append(f"    Latency: {api.latency_ms:.2f} ms")
                text_lines.append("")
        
        text_body = "\n".join(text_lines)
        
        # HTML version
        html_lines = [
            "<html><body style='font-family: Arial, sans-serif;'>",
            f"<h2>{subject}</h2>",
            f"<p><strong>Check time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
        ]
        
        if failed_apis:
            html_lines.append(f"<h3 style='color: #dc3545;'>❌ Failed APIs ({len(failed_apis)}):</h3>")
            html_lines.append("<ul>")
            for api in failed_apis:
                html_lines.append(f"<li><strong>{api.name}</strong> ({api.url})<br>")
                html_lines.append(f"<span style='color: #dc3545;'>Error: {api.error or 'Unknown error'}</span>")
                if api.status_code:
                    html_lines.append(f"<br>HTTP code: {api.status_code}")
                html_lines.append("</li>")
            html_lines.append("</ul>")
        
        if successful_apis:
            html_lines.append(f"<h3 style='color: #28a745;'>✅ Working APIs ({len(successful_apis)}):</h3>")
            html_lines.append("<ul>")
            for api in successful_apis:
                html_lines.append(f"<li><strong>{api.name}</strong> ({api.url})<br>")
                html_lines.append(f"Latency: {api.latency_ms:.2f} ms</li>")
            html_lines.append("</ul>")
        
        html_lines.append("</body></html>")
        html_body = "\n".join(html_lines)
        
        return text_body, html_body
    
    def notify(self, results: List[CheckResult]) -> bool:
        """
        Sends notifications based on check results.
        
        Args:
            results: List of check results
            
        Returns:
            True if notifications sent successfully
        """
        if not self.config.email_enabled and not self.config.push_enabled:
            return False
        
        failed_apis = [r for r in results if not r.success]
        has_failures = len(failed_apis) > 0
        
        # Check if we should notify
        should_notify = False
        is_recovery = False
        
        if has_failures:
            # Check each failed API
            for api in failed_apis:
                if self.should_notify(api.name, True):
                    should_notify = True
                    break
        else:
            # Check recovery (if there were errors, now all OK)
            if any(not self.last_notified_state.get(name, False) for name in [r.name for r in results]):
                # There were error notifications, now all OK
                for api_name in self.last_notified_state:
                    if self.last_notified_state[api_name] and api_name in [r.name for r in results if r.success]:
                        should_notify = True
                        is_recovery = True
                        break
        
        if not should_notify:
            return False
        
        # Format notification
        text_body, html_body = self.format_email_body(results, is_recovery)
        
        if has_failures:
            subject = f"API Issues Detected ({len(failed_apis)})"
        else:
            subject = "APIs Recovered"
        
        # Send email
        if self.config.email_enabled:
            self.send_email(subject, text_body, html_body)
        
        # Push notifications are handled on client side (browser)
        # Here we only log
        if self.config.push_enabled:
            logger.info(f"Push notification: {subject}")
        
        return True


def create_notifier_from_config(config_data: Dict[str, Any]) -> Optional[NotificationService]:
    """
    Creates notification service from configuration.
    
    Args:
        config_data: Dictionary with notification settings
        
    Returns:
        NotificationService or None if notifications not configured
    """
    if not config_data:
        return None
    
    notification_config = NotificationConfig(
        email_enabled=config_data.get('email', {}).get('enabled', False),
        email_smtp_host=config_data.get('email', {}).get('smtp_host'),
        email_smtp_port=config_data.get('email', {}).get('smtp_port', 587),
        email_smtp_user=config_data.get('email', {}).get('smtp_user'),
        email_smtp_password=config_data.get('email', {}).get('smtp_password'),
        email_from=config_data.get('email', {}).get('from'),
        email_to=config_data.get('email', {}).get('to', []),
        email_subject_prefix=config_data.get('email', {}).get('subject_prefix', '[API Monitor]'),
        push_enabled=config_data.get('push', {}).get('enabled', False),
        notify_on_failure=config_data.get('notify_on_failure', True),
        notify_on_recovery=config_data.get('notify_on_recovery', True),
        notify_on_all_failures=config_data.get('notify_on_all_failures', False)
    )
    
    if not notification_config.email_enabled and not notification_config.push_enabled:
        return None
    
    return NotificationService(notification_config)

