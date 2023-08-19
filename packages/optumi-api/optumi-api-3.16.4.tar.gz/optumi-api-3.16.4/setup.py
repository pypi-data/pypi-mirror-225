"""
Copyright (C) Optumi Inc - All rights reserved.

You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
"""

"""
optumi-api setup
"""
import json
from pathlib import Path

import setuptools


HERE = Path(__file__).parent.resolve()
long_description = (HERE / "README.md").read_text()

# Get the version
exec(open("optumi_api/_version.py").read())
api_version = __version__

# Get the core version
exec(open("core_version.py").read())
core_version = __version__
suffix = __version__.split("-")[1] if "-" in __version__ else ""
split = core_version.split("-")[0].split(".")

if "a" in suffix.lower():
    core_dependency_string = ""
else:
    core_dependency_string = "~=" + split[0] + "." + split[1] + "." + split[2]

setup_args = dict(
    name="optumi-api",
    version=api_version,
    url="https://optumi.com",
    author="Optumi Inc Authors",
    author_email="cs@optumi.com",
    description="Optumi api library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["optumi = optumi_api.cli:main"]},
    install_requires=["optumi_core" + core_dependency_string, "phonenumbers", "pwinput", "tornado", "requests", "python-dateutil"],
    zip_safe=False,
    python_requires=">=3.7",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Optumi"],
    classifiers=[
        "License :: Other/Proprietary License",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)


if __name__ == "__main__":
    setuptools.setup(**setup_args)

    print()
    print("optumi-api version is:", api_version)
    print("optumi-core version is:", core_version)
    print("optumi-core dependency string is: 'optumi_core" + core_dependency_string + "'")
