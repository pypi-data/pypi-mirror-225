from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="tablipy",
    version="0.1.5",
    author="Miro Laukka",
    author_email="mjlaukka@gmail.com",
    description="A library for working with tabular data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mirolaukka/tablipy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
