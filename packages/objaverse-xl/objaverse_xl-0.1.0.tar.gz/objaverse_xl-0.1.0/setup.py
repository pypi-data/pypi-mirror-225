from setuptools import find_packages, setup

# Read the README content
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="objaverse_xl",
    version="0.1.0",
    author="Allen Institute for AI",
    author_email="mattd@allenai.org",
    description="Objaverse-XL is an open dataset of over 10 million 3D objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/objaverse_xl",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=requirements,
)
