"""Module for periodic API checks."""

import time
import signal
import sys
import logging
from typing import Optional
from .loader import Config
from .checker import check_all_apis
from .reporter import print_report, get_exit_code
from .notifier import create_notifier_from_config
from .cache import ResultCache


class Scheduler:
    """Scheduler for periodic API checks."""
    
    def __init__(self, config: Config, output_format: str = None, output_file: str = None):
        """
        Initializes scheduler.
        
        Args:
            config: Monitoring configuration
            output_format: Output format
            output_file: File to save reports
        """
        self.config = config
        self.output_format = output_format or config.output_format
        self.output_file = output_file
        self.running = True
        self.check_count = 0
        
        # Initialize notification service
        self.notifier = create_notifier_from_config(config.notifications) if config.notifications else None
        
        # Initialize cache (TTL = check interval or 60 seconds)
        cache_ttl = config.interval if config.interval else 60.0
        self.cache = ResultCache(default_ttl=cache_ttl)
        
        # Signal handling for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Signal handler for graceful shutdown."""
        logging.info("\nReceived shutdown signal. Stopping monitoring...")
        self.running = False
    
    def run_once(self):
        """Performs one check of all APIs."""
        self.check_count += 1
        logging.info(f"\n{'='*60}")
        logging.info(f"Check #{self.check_count} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"{'='*60}")
        
        try:
            # Use cache for optimization
            results = check_all_apis(self.config.apis, cache=self.cache, use_async=len(self.config.apis) > 5)
            
            # Cleanup expired cache entries
            self.cache.cleanup_expired()
            
            # Send notifications
            if self.notifier:
                self.notifier.notify(results)
            
            # Output report
            print_report(results, self.output_format, self.output_file)
            
            # Statistics
            total = len(results)
            successful = sum(1 for r in results if r.success)
            failed = total - successful
            
            logging.info(f"Result: {successful}/{total} successful, {failed} failed")
            
            return get_exit_code(results)
            
        except Exception as e:
            logging.error(f"Error during check: {e}")
            return 1
    
    def run(self, interval: int):
        """
        Starts periodic checks.
        
        Args:
            interval: Interval between checks in seconds
        """
        if interval <= 0:
            raise ValueError("Interval must be a positive number")
        
        logging.info(f"Starting periodic monitoring (interval: {interval} seconds)")
        logging.info(f"Monitoring {len(self.config.apis)} APIs")
        logging.info("Press Ctrl+C to stop\n")
        
        try:
            # First check immediately
            self.run_once()
            
            # Periodic checks
            while self.running:
                time.sleep(interval)
                if self.running:
                    self.run_once()
                    
        except KeyboardInterrupt:
            logging.info("\nMonitoring stopped by user")
        except Exception as e:
            logging.error(f"Critical error: {e}")
            raise
        finally:
            logging.info(f"\nTotal checks performed: {self.check_count}")
            logging.info("Monitoring completed")


def run_monitoring(config_path: str, output_format: str = None, output_file: str = None):
    """
    Starts API monitoring (once or periodically).
    
    Args:
        config_path: Path to configuration file
        output_format: Output format
        output_file: File to save reports
    """
    from .loader import load_config
    
    config = load_config(config_path)
    
    # If interval is specified, start periodic monitoring
    if config.interval and config.interval > 0:
        scheduler = Scheduler(config, output_format, output_file)
        scheduler.run(config.interval)
    else:
        # Single check
        scheduler = Scheduler(config, output_format, output_file)
        return scheduler.run_once()

