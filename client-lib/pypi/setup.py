import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

install_requires_list = (HERE / "requirements.txt").read_text(encoding='utf-8').split('\n')

setup(
    name="nsrr",
    version="0.1.0",
    description="Access Sleep research resources from Sleepdata.org",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/nsrr/nsrr-cloud/client-lib/pypi/nsrr",
    author="Shyamal",
    author_email="sagarwal12@bwh.harvard.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["nsrr"],
    include_package_data=True,
    install_requires=install_requires_list,
    entry_points={"console_scripts": ["nsrr=nsrr.__main__:main"]},
)