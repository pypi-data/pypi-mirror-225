from setuptools import setup

from confutilPPP import __version__

URL = 'https://github.com/Aurorax-own/confutilPPP'

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='confutilPPP',
    version=__version__,
    packages=['confutilPPP', 'lib.logPPP'],
    description='A simple configuration file tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    author='Aurorax-own',
    author_email='15047150695@163.com',
    include_package_data=True,
    install_requires=[
        'pyyaml==6.0.1'
    ],
    project_urls={
        'Source': URL,
        'Tracker': f'{URL}/issues',
    },
)
