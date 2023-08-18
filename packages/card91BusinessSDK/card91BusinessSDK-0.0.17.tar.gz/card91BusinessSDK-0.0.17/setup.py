from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="card91BusinessSDK",
    version="0.0.17",
    description="This package is used to access the bunch of Card91 fintech business services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nk2909/Python-SDK.git",
    author="Card91",
    author_email="tech.apps@card91.io",
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    keywords=["python"],
    packages=find_packages(),
)
