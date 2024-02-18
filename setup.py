from setuptools import setup

import setuptools

setup(
    name="akatsuki_proto",
    version="0.1.4",
    author="Akatsuki",
    description="Protobuf files & source generation for Akatsuki",
    packages=setuptools.find_packages(),
    package_data={
        package: ["*.pyi", "**/*.pyi"]
        for package in setuptools.find_packages()
    },
    install_requires=["protobuf"],
    include_package_data=True,
    python_requires=">=3.9",
)