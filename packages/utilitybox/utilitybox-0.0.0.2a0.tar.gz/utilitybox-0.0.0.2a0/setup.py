from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.0.2-alpha'
DESCRIPTION = 'Utility Box - A collection of useful Python utilities.'
PACKAGE_NAME = 'utilitybox'
AUTHOR = 'Jose Angel Colin Najera'
EMAIL = 'josecolin99@gmail.com'
GITHUB_URL = 'https://github.com/Josecolin99/utilitybox'

setup(
    name=PACKAGE_NAME,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "utilitycmd=utilitybox.__main__:main"
        ]
    },
    version=VERSION,
    license='MIT',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=GITHUB_URL,
    keywords=[
        'utilities', 'tools', 'python', 'utilitybox'
    ],
    install_requires=[ 
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
