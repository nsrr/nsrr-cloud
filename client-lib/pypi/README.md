# nsrr-cloud

nsrr-cloud is a Python library to access NSRR Cloud resources.

## Installation

`pip install nsrr-cloud`

## Usage

To learn about different parameters, use help argument,

`nsrr_cloud --help`

To list the version of the nsrr-cloud library,

`nsrr_cloud -v`

To download entire dataset,

`nsrr_cloud -d [--dataset=cfs]`

To list all the subjects of a specific dataset,

`nsrr_cloud --dataset=cfs --list-subjects`

To list approved datasets access of a user,

`nsrr_cloud --list-access [--token-file=token.txt]`

To download subject specific files from a dataset,

`nsrr_cloud -d [--dataset=cfs] [--subject=cfs-visit5-800002]`

To provide password during command execution instead of interactive way,

`nsrr_cloud -d [--dataset=cfs] [--token-file=token.txt]`

To skip memory intensive data-integrity (See notes) check,

`nsrr_cloud -d [--dataset=cfs]  --no-md5`

To forcefully download the whole dataset,

`nsrr_cloud -d [--dataset=cfs]  --force`


## Developer guide

### Prerequisites
Following installation are necessary to start development,
- Python (version >=3.6)
- Auth server is running

### Initialization

Update Auth server address in the 'nsrr_cloud.py' file

### Build and publish package

Delete any existing distributions in the dist folder,

`rm -rf dist/*`

Update setup.py, nsrr_cloud/__main__.py and nsrr_cloud/__init__.py to bump version number,
```
ex: vi nsrr_cloud/__init__.py
__version__ = "x.x.x"
```
Run build command,

`python3 setup.py sdist bdist_wheel`

Update test pypi with the latest version, 

`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`

Upload pypi with the latest version,

`twine upload -u <username> -p <password> dist/*`



## Notes: 
1. It is recommended to use python version 3.8.x
2. Compatible with Windows (tested on win10 powershell with admin privileges), Mac and Linux systems
3. Data Integrity check is performed via the following two options
    - (Recommended) md5 checksum value is unique to every file. This option verifies that the downloaded file is exactly the same as being served by NSRR using md5 checksum value comparison. Use '--no-md5' to skip this option
    - file size check to match with download size of the file hosted by NSRR 
