from setuptools import setup, find_packages

from src.logPPP import __version__

URL = 'https://github.com/Aurorax-own/logPPP'

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='logPPP',
    version=__version__,
    description='logPPP',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    author='Aurorax-own',
    author_email='15047150695@163.com',
    packages=find_packages('src'),
    package_dir={'logPPP': 'src/logPPP'},
    include_package_data=True,
    install_requires=[
    ],
    project_urls={
        'Source': URL,
        'Tracker': f'{URL}/issues',
    }
)
