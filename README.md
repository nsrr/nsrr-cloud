# NSRR-Cloud
To allow Sleep Researchers access NSRR cloud resources

## Folder description

Single repository for Complete NSRR Cloud system:
1. auth-service folder contains code for Auth Server primarily to perform authn/authz of NSRR (sleepdata.org) users
2. client-lib folder contains wrapper code for interaction with auth server
3. infra folder contains automated infrastructure setup scripts

## NSRR Cloud user guide

[nsrr](https://pypi.org/project/nsrr) - a python based Client library is available for users to access NSSR Cloud resources. This library is compatible with Mac, Linux and Windows (tested on win10 PowerShell with admin privileges).

Run below command to install nsrr library,

`pip install nsrr`

### Usage

To learn about different parameters, use help argument,

```
nsrr --help
```

To list approved datasets access of a user,

```
nsrr --list-access
```

To list all the files of the dataset,

```
nsrr cfs --list-files
```

To list all the directories of the dataset,

```
nsrr cfs --list-directories
```

To download based on a folder or file path,

```
nsrr -d cfs/forms
nsrr -d cfs/dataset/cfs-data-dictionary-0.5.0-variables.csv
nsrr -d cfs/polysomnography/annotations-events-nsrr
```

To download entire dataset,

```
nsrr -d cfs
```

To list all the subjects of a specific dataset,

```
nsrr cfs --list-subjects
```

To download subject specific files from a dataset,

```
nsrr -d cfs --subject 800002
```

To provide password during command execution instead of interactive way,

```
nsrr -d cfs --token-file token.txt
```

Data Integrity check is performed via the following two options.
- (Recommended) md5 checksum value is unique to every file. This option verifies that the downloaded file is same as being served by NSRR using md5 checksum value comparison. 
- file size check to match with download size of the file hosted by NSRR.

To skip memory intensive data-integrity check,

```
nsrr cfs -d --no-md5
```

To forcefully download the whole dataset,

```
nsrr -d cfs --force
```

To list the version of the nsrr-cloud library,

```
nsrr -v
```
## Notes: 
1. It is recommended to use python version 3.8.x for Windows and 3.8.x & above for mac/linux systems
2. Compatible with Windows (tested on win10 powershell with admin privileges), mac/linux systems
3. Data Integrity check is performed via the following two options
    - (Recommended) md5 checksum value is unique to every file. This option verifies that the downloaded file is exactly the same as being served by NSRR using md5 checksum value comparison. Use '--no-md5' to skip this option
    - file size check to match with download size of the file hosted by NSRR 
