from setuptools import setup, find_packages

setup(
    name="aiogitignore",
    version="1.1",
    description="A simple command line tool to generate .gitignore files",
    author="Aiglon Doré",
    author_email='aiglondore@outlook.com',
    long_description="A simple command line tool to generate .gitignore files",
    long_description_content_type="text/markdown",
    install_requires=["aiohttp", "async-lru"],
    packages=find_packages(),
)
