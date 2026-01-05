# Contributing Guide

Thank you for your interest in the API Health Monitor project! We welcome any contributions.

## 🚀 How to Contribute

### Reporting Bugs

If you found a bug:

1. Check if it's already registered in [Issues](https://github.com/maksim4351/api-health-monitor/issues)
2. If not, create a new Issue with description:
   - What happened
   - Expected behavior
   - Steps to reproduce
   - Python version and OS
   - Error logs (if any)

### Suggesting New Features

1. Create an Issue describing the feature
2. Discuss the idea with the community
3. After approval, create a Pull Request

### Pull Request Process

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/api-health-monitor.git
   cd api-health-monitor
   ```

2. **Create a branch for your feature**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Make changes and add tests**
   - Follow project code style
   - Add tests for new functionality
   - Ensure all tests pass: `pytest`

5. **Update documentation**
   - Update README.md if needed
   - Add docstrings to new functions

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```

7. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

8. **Create Pull Request**
   - Fill PR template
   - Describe changes
   - Reference related Issues

## 📝 Code Standards

### Code Style

- Use Python 3.8+ syntax
- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions and classes

### Testing

- All new features must have tests
- Run tests before commit: `pytest`
- Aim for code coverage >80%

### Commits

Use clear commit messages:

```
feat: add POST request support
fix: fix timeout handling
docs: update README
test: add tests for checker
refactor: improve code structure
```

## 🧪 Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=api_monitor --cov-report=html

# Specific test
pytest tests/test_checker.py::TestCheckAPI
```

## 📚 Documentation

- Update README.md when adding new features
- Add usage examples
- Update docstrings

## ❓ Questions?

If you have questions, open an [Issue](https://github.com/maksim4351/api-health-monitor/issues) or discuss in Discussions.

Thank you for your contribution! 🎉
