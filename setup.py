"""
Setup configuration for Django Sybase backend.
"""
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-sybase',
    version='1.0.0',
    description='Sybase database backend for Django ORM',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Django Sybase Contributors',
    url='https://github.com/bie7u/sybase',
    packages=find_packages(),
    install_requires=[
        'Django>=3.2',
        'pyodbc>=4.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.8',
    keywords='django sybase database backend orm',
    project_urls={
        'Source': 'https://github.com/bie7u/sybase',
        'Tracker': 'https://github.com/bie7u/sybase/issues',
    },
)
