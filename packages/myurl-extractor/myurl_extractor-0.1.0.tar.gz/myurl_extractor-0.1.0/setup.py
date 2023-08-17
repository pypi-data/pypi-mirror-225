from setuptools import setup, find_packages

setup(
    name="myurl_extractor",
    version="0.1.0",
    description="A tool to extract URLs from a domain",
    author="achu",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "myurl_extractor = myurl_extractor.__main__:main"
        ]
    },
)
