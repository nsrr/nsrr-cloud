# NSRR-Cloud
To allow Sleep Researchers access NSRR cloud resources

## Folder description

Single repository for Complete NSRR Cloud system:
1. auth-service folder contains code for Auth Server primarily to perform authn/authz of NSRR (sleepdata.org) users
2. client-lib folder contains wrapper code for interaction with auth server
3. infra folder contains automated infrastructure setup scripts

## NSRR Cloud user guide

Python Client library package is available at https://pypi.org/project/nsrr_cloud and can be installed using following command,

`pip install nsrr_cloud`

### Usage

To learn about different parameters, use help argument,

`nsrr_cloud --help`

To list the version of the nsrr_cloud library,

`nsrr_cloud -v`

To download entire dataset,

`nsrr_cloud -d [--dataset=cfs]`

To list all the subjects of a specific dataset,

`nsrr_cloud --dataset=cfs --list-subjects`

To list approved datasets access of a user,

`nsrr_cloud --list-access [--token-file=token.txt]`

To list all the files of the dataset,

`nsrr_cloud --dataset=cfs --list-files`

To list all the directories of the dataset,

`nsrr_cloud --dataset=cfs --list-directories`

To download based on a folder or file path,

```
nsrr_cloud -d --dataset=cfs/forms
nsrr_cloud -d --dataset=cfs/dataset/cfs-data-dictionary-0.5.0-variables.csv
nsrr_cloud -d --dataset=cfs/polysomnography/annotations-events-nsrr
```

To download subject specific files from a dataset,

`nsrr_cloud -d [--dataset=cfs] [--subject=cfs-visit5-800002]`

To provide password during command execution instead of interactive way,

`nsrr_cloud -d [--dataset=cfs] [--token-file=token.txt]`

To skip memory intensive data-integrity (See notes) check,

`nsrr_cloud -d [--dataset=cfs]  --no-md5`

To forcefully download the whole dataset,

`nsrr_cloud -d [--dataset=cfs]  --force`

## Notes: 
1. It is recommended to use python version 3.8.x
2. Compatible with Windows (tested on win10 powershell with admin privileges), Mac and Linux systems
3. Data Integrity check is performed via the following two options
    - (Recommended) md5 checksum value is unique to every file. This option verifies that the downloaded file is exactly the same as being served by NSRR using md5 checksum value comparison. Use '--no-md5' to skip this option
    - file size check to match with download size of the file hosted by NSRR 
