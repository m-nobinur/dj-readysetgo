# Djago Starter Template

A fully-featured Django starter template with all batteries included, featuring pre-configured authentication, REST API support, admin enhancements, static/media file handling, testing setup, and best-practice project structure.

## Features

- Modern Django structure based on industry best practices
- Pre-configured settings for development, testing, and production
- Complete user authentication flow with Django-allauth
- DRF API with JWT authentication and Swagger documentation
- Enhanced admin interface with Unfold
- Tailwind CSS with daisyUI components
- HTMX integration for modern interactive UIs
- Celery task queue for background processing
- Multi-environment configurations
- Docker support for development and production
- Comprehensive testing setup with pytest
- Type checking with mypy
- Code quality tools: ruff, djlint, pre-commit
- uv integration for faster Python package management

## Requirements

- Python 3.8 or higher
- Cookiecutter 2.5.0 or higher

## Usage

### Using Cookiecutter Directly

```bash
cookiecutter gh:m-nobinur/dj-readysetgo
```

### Using uv (Optional)

If you want to use uv for package management (recommended for speed):

```bash
pip install uv
cookiecutter gh:m-nobinur/dj-readysetgo
# Select 'y' for use_uv when prompted
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| project_name | Name of the project | {{ cookiecutter.project_name }} Project |
| project_slug | Python module name for the project | dj_readysetgo |
| project_description | Brief description of the project | A fully-featured Django starter template with all batteries included |
| author_name | Your name | Your Name |
| author_email | Your email address | you@example.com |
| domain_name | Domain name for the project | example.com |
| python_version | Python version to use | {{ cookiecutter.python_version }} |

## Development

To set up this cookiecutter template for development:

```bash
git clone https://github.com/m-nobinur/dj-readysetgo
cd dj-readysetgo
cookiecutter . --no-input  # Test the template with default values
```

## License

This project is licensed under the terms of the Apache Software License 2.0.