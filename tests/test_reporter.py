"""Tests for reporting module."""

import pytest
import json
import csv
import io
import tempfile
from pathlib import Path
from api_monitor.reporter import (
    format_table,
    format_json,
    format_csv,
    print_report,
    get_exit_code
)
from api_monitor.checker import CheckResult


class TestFormatTable:
    """Tests for format_table function."""
    
    def test_format_table_success(self):
        """Test formatting successful results."""
        results = [
            CheckResult("API 1", "https://api1.com", 200, 100.5, True),
            CheckResult("API 2", "https://api2.com", 200, 200.0, True)
        ]
        
        output = format_table(results)
        
        assert "API" in output
        assert "API 1" in output
        assert "API 2" in output
        assert "200" in output
        assert "✓ OK" in output
    
    def test_format_table_failure(self):
        """Test formatting failed results."""
        results = [
            CheckResult("API 1", "https://api1.com", 404, 100.5, False, "Not found")
        ]
        
        output = format_table(results)
        
        assert "API 1" in output
        assert "404" in output
        assert "✗ FAIL" in output
    
    def test_format_table_timeout(self):
        """Test formatting timeout."""
        results = [
            CheckResult("API 1", "https://api1.com", None, 5000.0, False, "Timeout", True)
        ]
        
        output = format_table(results)
        
        assert "TIMEOUT" in output or "Timeout" in output
    
    def test_format_table_long_url(self):
        """Test truncating long URLs."""
        long_url = "https://" + "a" * 100 + ".com"
        results = [
            CheckResult("API 1", long_url, 200, 100.0, True)
        ]
        
        output = format_table(results)
        
        # URL should be truncated
        assert len(long_url) > 50
        # Output should contain truncated URL
        assert "..." in output


class TestFormatJSON:
    """Tests for format_json function."""
    
    def test_format_json_success(self):
        """Test JSON formatting."""
        results = [
            CheckResult("API 1", "https://api1.com", 200, 100.5, True, None, False)
        ]
        
        output = format_json(results)
        data = json.loads(output)
        
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["name"] == "API 1"
        assert data[0]["url"] == "https://api1.com"
        assert data[0]["status_code"] == 200
        assert data[0]["latency_ms"] == 100.5
        assert data[0]["success"] is True
        assert data[0]["error"] is None
        assert data[0]["timeout"] is False
    
    def test_format_json_multiple(self):
        """Test formatting multiple results."""
        results = [
            CheckResult("API 1", "https://api1.com", 200, 100.0, True),
            CheckResult("API 2", "https://api2.com", 404, 200.0, False, "Not found")
        ]
        
        output = format_json(results)
        data = json.loads(output)
        
        assert len(data) == 2
        assert data[0]["name"] == "API 1"
        assert data[1]["name"] == "API 2"
        assert data[1]["error"] == "Not found"
    
    def test_format_json_empty(self):
        """Test formatting empty list."""
        output = format_json([])
        data = json.loads(output)
        
        assert isinstance(data, list)
        assert len(data) == 0


class TestFormatCSV:
    """Tests for format_csv function."""
    
    def test_format_csv_success(self):
        """Test CSV formatting."""
        results = [
            CheckResult("API 1", "https://api1.com", 200, 100.5, True, None, False)
        ]
        
        output = format_csv(results)
        
        # Check that this is valid CSV
        reader = csv.reader(io.StringIO(output))
        rows = list(reader)
        
        assert len(rows) == 2  # Header + data
        assert rows[0] == ["API", "URL", "Status Code", "Latency (ms)", "Success", "Error", "Timeout"]
        assert rows[1][0] == "API 1"
        assert rows[1][1] == "https://api1.com"
        assert rows[1][2] == "200"
        assert rows[1][3] == "100.5"
        assert rows[1][4] == "True"
    
    def test_format_csv_multiple(self):
        """Test formatting multiple results."""
        results = [
            CheckResult("API 1", "https://api1.com", 200, 100.0, True),
            CheckResult("API 2", "https://api2.com", 404, 200.0, False, "Not found", False)
        ]
        
        output = format_csv(results)
        reader = csv.reader(io.StringIO(output))
        rows = list(reader)
        
        assert len(rows) == 3  # Header + 2 data rows
        assert rows[1][0] == "API 1"
        assert rows[2][0] == "API 2"
        assert rows[2][5] == "Not found"
    
    def test_format_csv_empty_status(self):
        """Test handling empty status."""
        results = [
            CheckResult("API 1", "https://api1.com", None, 100.0, False, "Error", False)
        ]
        
        output = format_csv(results)
        reader = csv.reader(io.StringIO(output))
        rows = list(reader)
        
        assert rows[1][2] == ""  # Empty status


class TestPrintReport:
    """Tests for print_report function."""
    
    @pytest.fixture
    def sample_results(self):
        """Fixture with sample results."""
        return [
            CheckResult("API 1", "https://api1.com", 200, 100.0, True)
        ]
    
    def test_print_report_table(self, sample_results, capsys):
        """Test table output."""
        print_report(sample_results, "table")
        captured = capsys.readouterr()
        
        assert "API" in captured.out
        assert "API 1" in captured.out
    
    def test_print_report_json(self, sample_results, capsys):
        """Test JSON output."""
        print_report(sample_results, "json")
        captured = capsys.readouterr()
        
        # Check that this is valid JSON
        data = json.loads(captured.out)
        assert isinstance(data, list)
    
    def test_print_report_csv(self, sample_results, capsys):
        """Test CSV output."""
        print_report(sample_results, "csv")
        captured = capsys.readouterr()
        
        # Check that this is valid CSV
        reader = csv.reader(io.StringIO(captured.out))
        rows = list(reader)
        assert len(rows) > 0
    
    def test_print_report_to_file(self, sample_results, tmp_path):
        """Test saving to file."""
        output_file = tmp_path / "report.json"
        
        print_report(sample_results, "json", str(output_file))
        
        assert output_file.exists()
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            assert isinstance(data, list)


class TestGetExitCode:
    """Tests for get_exit_code function."""
    
    def test_get_exit_code_all_success(self):
        """Test exit code for all successful checks."""
        results = [
            CheckResult("API 1", "https://api1.com", 200, 100.0, True),
            CheckResult("API 2", "https://api2.com", 200, 200.0, True)
        ]
        
        assert get_exit_code(results) == 0
    
    def test_get_exit_code_with_failure(self):
        """Test exit code with failures."""
        results = [
            CheckResult("API 1", "https://api1.com", 200, 100.0, True),
            CheckResult("API 2", "https://api2.com", 404, 200.0, False)
        ]
        
        assert get_exit_code(results) == 1
    
    def test_get_exit_code_all_failure(self):
        """Test exit code for all failed checks."""
        results = [
            CheckResult("API 1", "https://api1.com", 500, 100.0, False),
            CheckResult("API 2", "https://api2.com", 404, 200.0, False)
        ]
        
        assert get_exit_code(results) == 1
    
    def test_get_exit_code_empty(self):
        """Test exit code for empty list."""
        assert get_exit_code([]) == 0  # Empty list is considered successful

