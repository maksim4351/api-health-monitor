"""CLI interface for API Health Monitor."""

import sys
import argparse
import logging
from pathlib import Path
from .loader import load_config
from .checker import check_all_apis
from .reporter import print_report, get_exit_code
from .scheduler import run_monitoring, Scheduler
from .web_server import WebMonitoringServer


def setup_logging(log_file: str = None):
    """Sets up logging."""
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlers
    )


def run_command(config_path: str, output_format: str = None, output_file: str = None):
    """
    Executes API check according to configuration.
    
    Args:
        config_path: Path to configuration file
        output_format: Output format (overrides config)
        output_file: File to save report
    """
    # Setup basic logging for error handling
    setup_logging()
    
    try:
        # Load configuration
        config = load_config(config_path)
        
        # Setup logging from configuration (if log_file is specified)
        if config.log_file:
            setup_logging(config.log_file)
        
        logging.info(f"Loaded configuration: {len(config.apis)} APIs to check")
        
        # Determine output format with validation
        format_to_use = output_format or config.output_format
        valid_formats = ['table', 'json', 'csv', 'html']
        if format_to_use not in valid_formats:
            raise ValueError(f"Invalid output format: {format_to_use}. Valid: {', '.join(valid_formats)}")
        
        # Check all APIs
        logging.info("Starting API check...")
        
        # Use cache if available (optional)
        cache = None
        if hasattr(config, 'cache_enabled') and getattr(config, 'cache_enabled', False):
            from .cache import ResultCache
            cache = ResultCache(ttl=getattr(config, 'cache_ttl', 60))
        
        results = check_all_apis(config.apis, cache=cache)
        
        # Send notifications (if configured)
        if config.notifications:
            from .notifier import create_notifier_from_config
            notifier = create_notifier_from_config(config.notifications)
            if notifier:
                notifier.notify(results)
        
        # Output report
        print_report(results, format_to_use, output_file)
        
        # Determine exit code
        exit_code = get_exit_code(results)
        
        # Statistics
        total = len(results)
        successful = sum(1 for r in results if r.success)
        failed = total - successful
        
        logging.info(f"Check completed: {successful}/{total} successful, {failed} failed")
        
        return exit_code
        
    except FileNotFoundError as e:
        logging.error(f"Error: {e}")
        return 1
    except ValueError as e:
        logging.error(f"Configuration error: {e}")
        return 1
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return 1


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="API Health Monitor - fast API availability and latency monitoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  # Single check
  api-monitor run config.yaml
  api-monitor run config.yaml --format json
  
  # Continuous monitoring
  api-monitor watch config.yaml
  api-monitor watch config.yaml --interval 30
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # run command
    run_parser = subparsers.add_parser('run', help='Run API check (once or periodically)')
    run_parser.add_argument(
        'config',
        type=str,
        help='Path to configuration file (config.yaml)'
    )
    run_parser.add_argument(
        '--format', '-f',
        choices=['table', 'json', 'csv', 'html'],
        help='Output format (overrides config)'
    )
    run_parser.add_argument(
        '--output', '-o',
        type=str,
        help='File to save report'
    )
    
    # watch command
    watch_parser = subparsers.add_parser('watch', help='Start continuous monitoring')
    watch_parser.add_argument(
        'config',
        type=str,
        help='Path to configuration file (config.yaml)'
    )
    watch_parser.add_argument(
        '--interval', '-i',
        type=int,
        help='Check interval in seconds (overrides config.interval)'
    )
    watch_parser.add_argument(
        '--format', '-f',
        choices=['table', 'json', 'csv', 'html'],
        help='Output format (overrides config)'
    )
    watch_parser.add_argument(
        '--output', '-o',
        type=str,
        help='File to save reports'
    )
    watch_parser.add_argument(
        '--web', '-w',
        action='store_true',
        help='Launch web interface in browser'
    )
    watch_parser.add_argument(
        '--port', '-p',
        type=int,
        default=8080,
        help='Port for web server (default: 8080)'
    )
    
    args = parser.parse_args()
    
    if args.command == 'run':
        # Check if interval is in config
        config = load_config(args.config)
        if config.interval and config.interval > 0:
            # Periodic mode
            scheduler = Scheduler(config, args.format, args.output)
            scheduler.run(config.interval)
            sys.exit(0)
        else:
            # Single mode
            exit_code = run_command(args.config, args.format, args.output)
            sys.exit(exit_code)
    elif args.command == 'watch':
        # Forced periodic mode
        config = load_config(args.config)
        interval = args.interval or config.interval or 60  # Default 60 seconds
        
        if args.web:
            # Web interface mode
            web_server = WebMonitoringServer(config, port=args.port, interval=interval, config_path=args.config)
            web_server.start()
        else:
            # Console mode
            scheduler = Scheduler(config, args.format, args.output)
            scheduler.run(interval)
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()


