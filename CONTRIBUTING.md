# Contributing to Django Sybase Backend

Thank you for your interest in contributing to the Django Sybase backend! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sybase.git
   cd sybase
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

## Development Setup

### Install Development Dependencies

```bash
pip install Django>=3.2
pip install pyodbc>=4.0.0
# For testing
pip install pytest pytest-django
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_backend

# Run with verbose output
python -m unittest tests.test_backend -v
```

## Making Changes

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters (can go up to 120 for readability)
- Add docstrings to all classes and methods
- Use meaningful variable names

### Example Code Style

```python
"""
Module docstring explaining what this module does.
"""
from django.db.backends.base.operations import BaseDatabaseOperations


class DatabaseOperations(BaseDatabaseOperations):
    """
    Class docstring explaining the class purpose.
    """
    
    def quote_name(self, name):
        """
        Quote a table or column name.
        
        Args:
            name: The name to quote
            
        Returns:
            Quoted name string
        """
        if name.startswith('"') and name.endswith('"'):
            return name
        return '"%s"' % name
```

### Commit Messages

Use clear and descriptive commit messages:

```
Short (50 chars or less) summary

More detailed explanatory text, if necessary. Wrap it to about 72
characters or so. The blank line separating the summary from the body
is critical.

Further paragraphs come after blank lines.

- Bullet points are okay, too
- Use a hyphen or asterisk for the bullet
```

### Branch Naming

- `feature/` - New features (e.g., `feature/add-json-support`)
- `fix/` - Bug fixes (e.g., `fix/connection-timeout`)
- `docs/` - Documentation changes (e.g., `docs/improve-readme`)
- `test/` - Test additions/changes (e.g., `test/add-introspection-tests`)

## Types of Contributions

### Reporting Bugs

Before creating a bug report:
1. Check existing issues to avoid duplicates
2. Collect information about your environment:
   - Python version
   - Django version
   - Sybase ASE version
   - Operating system
   - pyodbc version

Create an issue with:
- Clear title
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/stack traces
- Environment information

### Suggesting Enhancements

Enhancement suggestions are welcome! Include:
- Clear description of the enhancement
- Use cases and benefits
- Potential implementation approach
- Compatibility considerations

### Pull Requests

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make your changes** with clear commits

3. **Test your changes**:
   ```bash
   python -m unittest discover tests
   ```

4. **Update documentation** if needed

5. **Push to your fork**:
   ```bash
   git push origin feature/my-feature
   ```

6. **Create a Pull Request** on GitHub

### Pull Request Checklist

- [ ] Code follows the project's style guidelines
- [ ] Tests pass locally
- [ ] New code has appropriate tests
- [ ] Documentation updated if needed
- [ ] Commit messages are clear and descriptive
- [ ] No merge conflicts with main branch

## Project Structure

```
sybase/
├── django_sybase/          # Main package
│   ├── __init__.py        # Package initialization
│   ├── base.py            # DatabaseWrapper
│   ├── features.py        # DatabaseFeatures
│   ├── operations.py      # DatabaseOperations
│   ├── client.py          # DatabaseClient
│   ├── creation.py        # DatabaseCreation
│   ├── introspection.py   # DatabaseIntrospection
│   ├── schema.py          # DatabaseSchemaEditor
│   └── compiler.py        # SQL Compiler
├── tests/                 # Test suite
│   ├── __init__.py
│   └── test_backend.py
├── examples/              # Example code
│   ├── models.py
│   └── settings.py
├── README.md
├── QUICKSTART.md
├── CONTRIBUTING.md
├── LICENSE
└── setup.py
```

## Key Components

### base.py - DatabaseWrapper
Main database connection wrapper. Handles:
- Connection management
- Transaction handling
- Cursor creation

### features.py - DatabaseFeatures
Declares what features the database supports:
- Transaction support
- Foreign key support
- Index types
- SQL features

### operations.py - DatabaseOperations
Database-specific operations:
- SQL generation
- Date/time handling
- Type conversions
- Quoting

### schema.py - DatabaseSchemaEditor
Schema manipulation:
- CREATE/DROP TABLE
- ALTER TABLE operations
- Index management
- Constraint management

### introspection.py - DatabaseIntrospection
Database schema inspection:
- List tables
- Describe tables
- Get constraints
- Get relationships

## Testing Guidelines

### Writing Tests

```python
import unittest

class TestNewFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def test_something(self):
        """Test description."""
        result = something()
        self.assertEqual(result, expected)
    
    def tearDown(self):
        """Clean up after test."""
        pass
```

### Test Coverage

Aim for high test coverage of new code:
- Unit tests for individual functions
- Integration tests for component interactions
- Edge cases and error conditions

## Documentation

### Updating Documentation

When adding features or making changes:
1. Update relevant docstrings
2. Update README.md if user-facing
3. Update QUICKSTART.md for setup changes
4. Add examples to examples/ directory

### Documentation Style

- Use Markdown for documentation files
- Include code examples
- Add comments for complex logic
- Keep examples concise and practical

## Questions?

If you have questions:
- Open an issue for discussion
- Check existing issues and pull requests
- Review Django's database backend documentation

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards others

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🙏
