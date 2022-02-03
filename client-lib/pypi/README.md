# nsrr

[nsrr](https://pypi.org/project/nsrr) - a Python-based client library is available for users to access NSSR Cloud resources. This library is compatible with Mac, Linux and Windows (tested on win10 PowerShell with admin privileges).

## Installation

```
pip install nsrr
```

If both version of Python i.e., Python2.x and Python3.x are installed in the OS then you can use the command below to call Python3 based pip using:

`pip3 install nsrr` or `python3 -m pip install nsrr`

## Usage

This section of the documentation covers usage of 'CFS' dataset as an example.


To learn about different parameters, use help argument:

```
nsrr --help
```

To list approved datasets access of a user:

```
nsrr --list-access
```

To list all the files of the dataset:

```
nsrr cfs --list-files
```

To list all the directories of the dataset:

```
nsrr cfs --list-directories
```

To download based on a folder or file path:

```
nsrr -d cfs/forms
nsrr -d cfs/dataset/cfs-data-dictionary-0.5.0-variables.csv
nsrr -d cfs/polysomnography/annotations-events-nsrr
```

To download entire dataset:

```
nsrr -d cfs
```

To list all the subjects of a specific dataset:

```
nsrr cfs --list-subjects
```

To download subject specific files from a dataset:

```
nsrr -d cfs --subject 800002
```

To provide password in non-interactive way:

```
nsrr -d cfs --token-file token.txt
```

Data Integrity check is performed via the following two options.
- (Recommended) md5 checksum value is unique to every file. This option verifies that the downloaded file is same as being served by NSRR using md5 checksum value comparison. 
- file size check to match with download size of the file hosted by NSRR.

To skip memory intensive data-integrity check:

```
nsrr cfs -d --no-md5
```

To forcefully download the whole dataset:

```
nsrr -d cfs --force
```

To list the version of the nsrr library:

```
nsrr -v
```


## Developer guide

### Prerequisites
Following installation are necessary to start development,
- Python (version >=3.6)
- Auth server is running

### Initialization

Update Auth server address in the 'nsrr.py' file

### Build and publish package

Delete any existing distributions in the dist folder:

```
rm -rf dist/*
```

Update setup.py, nsrr/__main__.py and nsrr/__init__.py to bump version number:

```
ex: vi nsrr/__init__.py
__version__ = "x.x.x"
```

Run build command:

```
python3 setup.py sdist bdist_wheel
```

Update test pypi with the latest version:

```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Upload pypi with the latest version:

```
twine upload -u <username> -p <password> dist/*
```



## Notes: 
1. It is recommended to use Python version 3.8.x
2. Compatible with Windows (tested on win10 powershell with admin privileges), Mac and Linux systems
3. Data Integrity check is performed via the following two options
    - (Recommended) md5 checksum value is unique to every file. This option verifies that the downloaded file is exactly the same as being served by NSRR using md5 checksum value comparison. Use '--no-md5' to skip this option
    - file size check to match with download size of the file hosted by NSRR 
