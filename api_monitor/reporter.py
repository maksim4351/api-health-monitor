"""Module for generating check result reports."""

import json
import csv
import io
from typing import List
from tabulate import tabulate
from .checker import CheckResult


def format_table(results: List[CheckResult]) -> str:
    """
    Formats results as a table for CLI.
    
    Args:
        results: List of check results
        
    Returns:
        Formatted table string
    """
    headers = ["API", "URL", "Status", "Latency (ms)", "Result"]
    rows = []
    
    for result in results:
        if result.timeout:
            status = "TIMEOUT"
        elif result.status_code:
            status = str(result.status_code)
        elif result.error:
            status = "ERROR"
        else:
            status = "N/A"
        
        latency = f"{result.latency_ms:.2f}"
        result_status = "✓ OK" if result.success else "✗ FAIL"
        if result.error:
            result_status += f" ({result.error})"
        
        # Truncate long URLs for readability
        url_display = result.url
        if len(url_display) > 50:
            url_display = url_display[:47] + "..."
        
        rows.append([
            result.name,
            url_display,
            status,
            latency,
            result_status
        ])
    
    return tabulate(rows, headers=headers, tablefmt="grid")


def format_json(results: List[CheckResult]) -> str:
    """
    Formats results as JSON.
    
    Args:
        results: List of check results
        
    Returns:
        JSON string
    """
    data = []
    for result in results:
        data.append({
            "name": result.name,
            "url": result.url,
            "status_code": result.status_code,
            "latency_ms": result.latency_ms,
            "success": result.success,
            "error": result.error,
            "timeout": result.timeout
        })
    
    return json.dumps(data, indent=2, ensure_ascii=False)


def format_csv(results: List[CheckResult]) -> str:
    """
    Formats results as CSV.
    
    Args:
        results: List of check results
        
    Returns:
        CSV string
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(["API", "URL", "Status Code", "Latency (ms)", "Success", "Error", "Timeout"])
    
    # Data
    for result in results:
        writer.writerow([
            result.name,
            result.url,
            result.status_code or "",
            result.latency_ms,
            result.success,
            result.error or "",
            result.timeout
        ])
    
    return output.getvalue()


def format_html(results: List[CheckResult]) -> str:
    """
    Formats results as HTML.
    
    Args:
        results: List of check results
        
    Returns:
        HTML string
    """
    from datetime import datetime
    
    total = len(results)
    successful = sum(1 for r in results if r.success)
    failed = total - successful
    success_rate = (successful / total * 100) if total > 0 else 0
    
    # Determine status color
    status_color = "#28a745" if successful == total else "#dc3545" if successful == 0 else "#ffc107"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Health Monitor - Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .header .timestamp {{
            opacity: 0.9;
            font-size: 0.9em;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #6c757d;
            font-size: 0.9em;
        }}
        .success {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .total {{ color: #007bff; }}
        .rate {{ color: {status_color}; }}
        .results {{
            padding: 30px;
        }}
        .results h2 {{
            margin-bottom: 20px;
            color: #333;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        thead {{
            background: #667eea;
            color: white;
        }}
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
        }}
        tbody tr:hover {{
            background: #f8f9fa;
        }}
        tbody tr:last-child td {{
            border-bottom: none;
        }}
        .status-badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .status-ok {{
            background: #d4edda;
            color: #155724;
        }}
        .status-fail {{
            background: #f8d7da;
            color: #721c24;
        }}
        .status-timeout {{
            background: #fff3cd;
            color: #856404;
        }}
        .status-error {{
            background: #f8d7da;
            color: #721c24;
        }}
        .url {{
            color: #007bff;
            text-decoration: none;
            word-break: break-all;
        }}
        .url:hover {{
            text-decoration: underline;
        }}
        .latency {{
            font-weight: 600;
        }}
        .latency-fast {{ color: #28a745; }}
        .latency-medium {{ color: #ffc107; }}
        .latency-slow {{ color: #dc3545; }}
        .footer {{
            padding: 20px 30px;
            background: #f8f9fa;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 API Health Monitor</h1>
            <div class="timestamp">Report created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value total">{total}</div>
                <div class="stat-label">Total APIs</div>
            </div>
            <div class="stat-card">
                <div class="stat-value success">{successful}</div>
                <div class="stat-label">Successful</div>
            </div>
            <div class="stat-card">
                <div class="stat-value failed">{failed}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value rate">{success_rate:.1f}%</div>
                <div class="stat-label">Success Rate</div>
            </div>
        </div>
        
        <div class="results">
            <h2>📊 Detailed Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>API</th>
                        <th>URL</th>
                        <th>Status</th>
                        <th>Latency</th>
                        <th>Result</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    for result in results:
        # Determine status class
        if result.timeout:
            status_class = "status-timeout"
            status_text = "TIMEOUT"
        elif result.error:
            status_class = "status-error"
            status_text = "ERROR"
        elif result.success:
            status_class = "status-ok"
            status_text = "✓ OK"
        else:
            status_class = "status-fail"
            status_text = "✗ FAIL"
        
        # Determine latency class
        if result.latency_ms < 200:
            latency_class = "latency-fast"
        elif result.latency_ms < 1000:
            latency_class = "latency-medium"
        else:
            latency_class = "latency-slow"
        
        status_code = str(result.status_code) if result.status_code else "N/A"
        error_text = f"<br><small style='color: #dc3545;'>{result.error}</small>" if result.error else ""
        
        html += f"""
                    <tr>
                        <td><strong>{result.name}</strong></td>
                        <td><a href="{result.url}" target="_blank" class="url">{result.url}</a></td>
                        <td>{status_code}</td>
                        <td><span class="latency {latency_class}">{result.latency_ms:.2f} ms</span></td>
                        <td><span class="status-badge {status_class}">{status_text}</span>{error_text}</td>
                    </tr>
"""
    
    html += """
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Generated by API Health Monitor v1.0.0</p>
            <p><a href="https://github.com/maksim4351/api-health-monitor" style="color: #667eea;">GitHub Repository</a></p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def print_report(results: List[CheckResult], output_format: str = "table", output_file: str = None):
    """
    Outputs report in specified format.
    
    Args:
        results: List of check results
        output_format: Output format (table, json, csv, html)
        output_file: Path to file for saving (optional)
    """
    if output_format == "json":
        content = format_json(results)
    elif output_format == "csv":
        content = format_csv(results)
    elif output_format == "html":
        content = format_html(results)
        # For HTML always save to file, if not specified - use default
        if not output_file:
            output_file = "api_report.html"
    else:  # table
        content = format_table(results)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Report saved to {output_file}")
        if output_format == "html":
            import os
            abs_path = os.path.abspath(output_file)
            print(f"Open in browser: file:///{abs_path.replace(os.sep, '/')}")
    else:
        print(content)


def get_exit_code(results: List[CheckResult]) -> int:
    """
    Determines exit code based on check results.
    
    Args:
        results: List of check results
        
    Returns:
        0 if all checks successful, 1 if there are errors
    """
    if all(result.success for result in results):
        return 0
    return 1


