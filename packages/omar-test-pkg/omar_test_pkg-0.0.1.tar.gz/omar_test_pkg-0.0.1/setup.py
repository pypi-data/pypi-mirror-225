from setuptools import setup, find_packages

# with open("./app/readme.md", "r") as fh:
#     long_description = fh.read()

setup(
    name="omar_test_pkg",
    version="0.0.1",
    author="Supreme Leader",
    author_email="omar@limbic.ai",
    description="Omar test package",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(where="app"),
    package_dir={"": "app"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "openai"
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
            "twine",
        ]
    },
)