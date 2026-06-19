# Contributing to SentimentIQ

Thank you for your interest in contributing to SentimentIQ! We welcome contributions from everyone.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. Install development dependencies: `pip install -r requirements-dev.txt`

## Development Workflow

1. Create a new branch for your feature/fix: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `pytest`
4. Run code quality checks:
   ```bash
   black .
   isort .
   flake8 app tests
   mypy app
   ```
5. Commit your changes: `git commit -m "Description of changes"`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Open a pull request

## Code Standards

- Follow PEP 8 style guide
- Use type hints for all functions
- Add docstrings to all functions and modules
- Write tests for new functionality
- Maintain or improve code coverage

## Testing

Run the test suite:
```bash
pytest                    # Run all tests
pytest --cov=app         # Run with coverage
pytest -v                # Verbose output
pytest -k test_auth      # Run specific tests
```

## Pull Request Process

1. Update README.md with any new features or changes
2. Ensure all tests pass: `pytest`
3. Ensure code quality checks pass
4. Update docstrings as needed
5. Request review from maintainers

## Issues

When reporting issues, please include:
- Python version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error traceback if applicable

## Feature Requests

Feature requests are welcome! Please describe:
- The use case
- Why it would be valuable
- How it should work

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Report inappropriate behavior to maintainers

Thank you for contributing to SentimentIQ!
