#!/usr/bin/env python
import os
import subprocess
import sys
from pathlib import Path

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def execute_command(command, error_message="Command failed"):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as error:
        print(error_message)
        print(f"Command: {command}")
        print(f"Error: {error}")
        sys.exit(1)


def check_mailpit():
    """Check if mailpit is installed and install it if not"""
    try:
        subprocess.run(["mailpit", "version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Mailpit not found. Attempting to install mailpit first...")
        execute_command(
            "brew install mailpit",
            "Failed to install mailpit. Please install it manually.",
        )
        print("Mailpit installed successfully")


def check_redis():
    """Check if redis is installed and install it if not"""
    try:
        subprocess.run(["redis-server", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Redis not found. Attempting to install redis first...")
        execute_command(
            "brew install redis",
            "Failed to install redis. Please install it manually.",
        )
        print("Redis installed successfully")


def init_git():
    """Initialize git repository"""
    execute_command("git init", "Failed to initialize git repository")
    execute_command("git add .", "Failed to add files to git repository")
    execute_command(
        'git commit -m "Initial commit"', "Failed to commit files to git repository"
    )
    print("Git repository has been initialized")


def setup_python_environment():
    """Set up Python environment with uv or virtualenv based on user choice"""
    try:
        # Check if uv is installed
        subprocess.run(["uv", "--version"], check=True, capture_output=True)

        # Create virtualenv using uv
        execute_command("uv venv", "Failed to create virtual environment with uv")

        # Install dependencies with uv
        execute_command(
            "uv pip install -r requirements/local.txt",
            "Failed to install dependencies with uv",
        )
        print("Python environment set up with uv and dependencies installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("uv not found. Attempting to install uv first...")
        try:
            execute_command("pip install uv", "Failed to install uv")
            print("uv installed successfully, now creating environment...")

            # Try again with uv now installed
            execute_command("uv venv", "Failed to create virtual environment with uv")
            execute_command(
                "uv pip install -r requirements/local.txt",
                "Failed to install dependencies with uv",
            )
            print("Python environment set up with uv and dependencies installed")
        except subprocess.CalledProcessError:
            print("Falling back to standard virtualenv")
            execute_command(
                "python -m venv .venv", "Failed to create virtual environment"
            )
            pip_cmd = ".venv/bin/pip" if os.name != "nt" else ".venv\\Scripts\\pip"
            execute_command(
                f"{pip_cmd} install -r requirements/local.txt",
                "Failed to install dependencies with pip",
            )
            print(
                "Python environment set up with virtualenv and dependencies installed"
            )


def setup_npm_packages():
    """Install npm packages for Tailwind CSS if selected"""
    os.chdir(os.path.join(PROJECT_DIRECTORY, "theme", "static_src"))
    execute_command("npm install", "Failed to install npm packages for Tailwind CSS")
    os.chdir(PROJECT_DIRECTORY)
    print("Tailwind CSS npm packages installed")


def main():
    with open(".python-version", "w") as f:
        if "{{ cookiecutter.python_version }}":
            f.write("{{ cookiecutter.python_version }}")
        else:
            python_version = (
                subprocess.check_output(
                    ["python", "--version"], stderr=subprocess.STDOUT
                )
                .decode("utf-8")
                .strip()
                .split(" ")[1]
            )

            f.write(python_version)
    print("Created .python-version file")

    # Initialize git repository
    init_git()

    # Set up Python environment based on user choices
    setup_python_environment()

    # Set up npm packages for Tailwind if selected
    setup_npm_packages()

    print("\n========================")
    print(" Project setup complete! ")
    print("========================")

    print(
        f"\nYour Django project '{Path(PROJECT_DIRECTORY).name}' has been created successfully!"
    )
    print("Checking for dependencies...")
    print("Checking for mailpit and redis...")
    check_mailpit()
    check_redis()

    print("\nNext steps:")

    print("  1. Enter your virtual environment:")
    if "{{ cookiecutter.use_uv }}" == "y":
        print("       source .venv/bin/activate  # On Unix/Linux/Mac")
        print("       .venv\\Scripts\\activate     # On Windows")
    else:
        print("       source .venv/bin/activate  # On Unix/Linux/Mac")
        print("       .venv\\Scripts\\activate     # On Windows")
    print("  2. Create a superuser: python manage.py createsuperuser")
    print("  3. Run the development server: python manage.py runserver")
    print("\nEnjoy building your project!")


if __name__ == "__main__":
    main()
