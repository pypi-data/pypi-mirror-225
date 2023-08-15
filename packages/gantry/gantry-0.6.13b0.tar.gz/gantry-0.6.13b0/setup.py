from distutils.util import convert_path

import setuptools

version = {}
with open(convert_path("gantry/version.py")) as fp:
    exec(fp.read(), version)


install_requires = [
    "Jinja2~=3.1.2",
    # 1.1.1 contains a fix for a regression in a dependency
    # https://stackoverflow.com/a/71574145
    "dateparser~=1.1,>=1.1.1",
    "typeguard~=2.13",
    "backoff~=2.1.2",
    "click>=7.1.2",
    "click-aliases~=1.0",
    "requests>=2.22.0",
    "colorama>=0.4.0",
    "label-studio-sdk>=0.0.19,<0.0.22",
    "tabulate~=0.8",
    "typing-extensions>=4.6",
    "isodate~=0.6",
    "pydantic>=1.10.8",
    "python-dateutil>=2.8.1",
]


# https://packaging.python.org/tutorials/packaging-projects/
setuptools.setup(
    name="gantry",
    version=version["__version__"],
    install_requires=install_requires,
    include_package_data=True,
    author="Gantry Systems, Inc.",
    author_email="oss@gantry.io",
    description="Gantry Python Library",
    long_description="",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    license="Apache Software License v2",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": ["gantry-cli = gantry.cli.main:cli"],
    },
    package_data={"": ["dataset/templates/*.jinja"]},
)
