from setuptools import find_packages
from setuptools import setup

import pathlib
import codecs
import os
import re


readme_file = pathlib.Path('README.md')
changelog_file = pathlib.Path('CHANGELOG.md')

here = os.path.abspath(os.path.dirname(__file__))


def get_long_description():
    long_description = ""

    if not readme_file.exists():
        return ""

    with readme_file.open("r") as file:
        long_description += file.read()

    long_description += "\n\n"

    if not changelog_file.exists():
        return long_description

    with changelog_file.open("r") as file:
        long_description += file.read()

    return long_description


def find_version(*file_paths):
    path = os.path.join(here, *file_paths)
    with codecs.open(path, 'r') as fp:
        version_file = fp.read()
        version_match = re.search(r"__version__ = ['\"]([^'\"]*)['\"]",
                                  version_file, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")


def find_author(*file_paths):
    path = os.path.join(here, *file_paths)
    with codecs.open(path, 'r') as fp:
        auther_file = fp.read()
        auther_match = re.search(r"__auther__ = ['\"]([^'\"]*)['\"]",
                                 auther_file, re.M)
        if auther_match:
            return auther_match.group(1)
        raise RuntimeError("Unable to find auther string.")


setup(
    name="wappstorest",
    python_requires='>=3.9.0',
    version=find_version("src", "wappstorest", "__init__.py"),
    author=find_author("src", "wappstorest", "__init__.py"),
    author_email="support@seluxit.com",
    license="Apache-2.0",
    description="Simple Wappsto Python user-interface to Wappsto Rest",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/Wappsto/python-wappsto-rest",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    # package_data={
    #     'wappstorest': ['WappstoRest.pyi'],
    #     'wappstorest/schemas': ['schemas/jsonrpc.pyi'],
    # },
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    # tests_require=[
    #     'pytest',
    #     'tox'
    # ],
    package_data={'wappstorest': ['../README.md', '../CHANGELOG.md']},
    install_requires=[
        'pydantic==1.9.2',
        'httpx>=0.23.0',
        'websocket-client>=0.59.0',
        'rich>=12.0.0'
    ],
    # entry_points={  # TODO: fix __main__.py to be optional.
    #     "console_scripts": "wappstoiot=wappstoiot:__main__"
    # },
    # extras_require={  # TODO: fix __main__.py to be optional.
    #     "cli": [
    #         'requests',
    #     ]
    # },
)
