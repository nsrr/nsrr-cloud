# nsrr-cloud

nsrr-cloud is a Python library to access NSRR Cloud resources.

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

Update setup.py and nsrr_cloud/__init__.py to bump version number,
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




