from setuptools import setup

import setuptools

setup(
    name="akatsuki_proto",
    version="0.1.0",
    author="Akatsuki",
    description="Protobuf files & source generation for Akatsuki",
    packages=setuptools.find_packages(),
    package_data={
        package: ["*.pyi", "**/*.pyi"]
        for package in setuptools.find_packages()
    },
    include_package_data=True,
    python_requires=">=3.9",
)