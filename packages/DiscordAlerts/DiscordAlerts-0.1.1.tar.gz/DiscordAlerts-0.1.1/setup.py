# setup.py
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="DiscordAlerts",
    version="0.1.1",
    author="gabrielchboff",
    description="Package for Alerts on Discord",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gabrielchboff/DiscordAlerts",
    packages=find_packages(),
    install_requires=[
        "discord-webhook",  # Add any other dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
