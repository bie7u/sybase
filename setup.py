"""
Setup script for the Sybase Django application.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-sybase-app",
    version="1.0.0",
    author="bie7u",
    description="Django application with Sybase database connection via SQLAlchemy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bie7u/sybase",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=4.2.0,<5.0",
        "djangorestframework>=3.14.0",
        "django-filter>=23.0",
        "sqlalchemy>=2.0.0",
        "pyodbc>=5.0.0",
        "python-dotenv>=1.0.0",
    ],
)
