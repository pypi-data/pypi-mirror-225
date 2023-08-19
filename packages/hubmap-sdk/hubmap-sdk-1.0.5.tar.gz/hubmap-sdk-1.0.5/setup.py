from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hubmap-sdk",
    version="1.0.5",
    author="Hubmap",
    author_email="api-developers@hubmapconsortium.org",
    description="Python Client Libary to use HuBMAP web services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['hubmap_sdk'],
    keywords=[
        "HuBMAP Sdk",
        "python"
    ],
    install_requires=[
        "certifi==2021.10.8",
        "chardet==4.0.0",
        "idna==2.10",
        "requests>=2.22.0",
        "urllib3==1.26.7"
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)

