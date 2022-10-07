from setuptools import setup, find_packages

setup(
    name='PyNotionClient',
    version='0.0.1',
    description='Python client for Notion.so',
    package_dir={'': 'notion'},
    py_modules=['notion']
)