# Tests for API Health Monitor

## Running Tests

### Installing Test Dependencies

```bash
pip install -r requirements.txt
```

### Running All Tests

```bash
pytest
```

### Running with Code Coverage

```bash
pytest --cov=api_monitor --cov-report=html
```

After execution, open `htmlcov/index.html` in browser to view coverage report.

### Running Specific Test

```bash
pytest tests/test_loader.py
pytest tests/test_checker.py::TestCheckAPI::test_check_api_success
```

### Running with Verbose Output

```bash
pytest -v
```

### Running Only Fast Tests

```bash
pytest -m "not slow"
```

## Test Structure

- `test_loader.py` - tests for configuration loading
- `test_checker.py` - tests for API checking (with mocks)
- `test_reporter.py` - tests for report formatting
- `test_cli.py` - tests for CLI interface
- `test_cache.py` - tests for result caching
- `test_notifier.py` - tests for notifications

## Notes

- Tests for `checker.py` use mocks to avoid making real HTTP requests
- Tests for `loader.py` create temporary YAML files
- All tests should pass without internet connection
