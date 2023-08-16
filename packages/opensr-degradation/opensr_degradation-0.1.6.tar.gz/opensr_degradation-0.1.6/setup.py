#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["torch", "numpy", "sklearn", "scikit-image"]
weights = [
    "opensr_degradation/models/model_reflectance.pt",
    "opensr_degradation/models/model_noise.pt"
]

test_requirements = []

setup(
    author="Cesar Aybar",
    author_email="csaybar@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="A real-world HR degradation",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    data_files=[("opensr_degradation", weights)],
    keywords="opensr_degradation",
    name="opensr_degradation",
    packages=find_packages(include=["opensr_degradation", "opensr_degradation.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/csaybar/opensr_degradation",    
    version="0.1.6",
    zip_safe=False,
)
