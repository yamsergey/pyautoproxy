import os
import sys

import setuptools
from setuptools.command.install import install


def version() -> str: return "0.0.15"


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != version():
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, version()
            )
            sys.exit(info)


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyautoproxy",
    version=version(),
    author="Sergey Yamshchikov",
    author_email="yamsergey@gmail.com",
    description="Light weight auto proxy server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yamsergey/pyautoproxy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    cmdclass={
        'verify': VerifyVersionCommand,
    },
    entry_points={
        'console_scripts': [
            "pyautoproxy = pyautoproxy.main:pyautoproxy"
        ]
    }
)
