"""Setup file for data.understand."""

import setuptools

with open("data_understand/version.py") as f:
    code = compile(f.read(), f.name, "exec")
    exec(code)

# Fetch ReadMe
long_description = ""
with open("README.md", "r") as fh:
    long_description = fh.read()

# Use requirements.txt to set the install_requires
with open("requirements.txt") as f:
    install_requires = [line.strip() for line in f]

setuptools.setup(
    name=name,  # noqa: F821
    version=version,  # noqa: F821
    author="Gaurav Gupta",
    author_email="ggupta2005@gmail.com",
    description="Utility package for generating insights for datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ggupta2005/data.understand",
    packages=setuptools.find_packages(exclude=["tests*"]),
    python_requires=">=3.6",
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    entry_points={
        "console_scripts": ["data_understand = data_understand.main:main"]
    },
)
