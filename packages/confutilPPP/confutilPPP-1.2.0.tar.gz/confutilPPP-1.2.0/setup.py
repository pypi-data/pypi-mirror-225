from setuptools import setup, find_packages

from src.confutilPPP import __version__

URL = 'https://github.com/Aurorax-own/confutilPPP'

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='confutilPPP',
    version=__version__,
    description='A simple configuration file tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    author='Aurorax-own',
    author_email='15047150695@163.com',
    packages=find_packages('src'),
    package_dir={'confutilPPP': 'src/confutilPPP'},
    include_package_data=True,
    install_requires=[
        'PyYAML==6.0.1',
        'logPPP==1.1.2'
    ],
    project_urls={
        'Source': URL,
        'Tracker': f'{URL}/issues',
    },
)
