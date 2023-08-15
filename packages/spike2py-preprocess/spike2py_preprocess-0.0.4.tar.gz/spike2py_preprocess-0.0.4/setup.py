import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="spike2py_preprocess",
    version="0.0.4",
    description="Preprocess data with spike2py",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MartinHeroux/spike2py_preprocess",
    author="Martin Héroux",
    author_email="heroux.martin@gmail.com",
    license="GNU General Public License v3 or later (GPLv3+)",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(include=["spike2py_preprocess"], exclude=["tests", "test_*"]),
    include_package_data=False,
    install_requires=["spike2py"],
    tests_require=["pytest"]
)
