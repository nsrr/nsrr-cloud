# NSRR Cloud

Over the past decade, we have been experiencing a gradual increase in adoption of Cloud usage in the Healthcare, Research and IT industries. One of the main benefits of Cloud is on-demand, wide-variety of scalable IT resources that users can access at their fingertips. 

NSRR traditionally serves sleep researchers with resources using On-premises hosting services. For sleep researchers to fully realize potential of IT Cloud services, we are migrating our sleep research resources to Cloud-based hosting solution. Listed below are the potential benefits of NSRR Cloud:
- Users can skip maintaining individual copies of sleep studies; Users can access files to perform analysis and delete them as needed
- Access partial datasets to enable researchers with smaller compute and storage resources to perform analysis
- Uniform network bandwidth serving sleep studies

 Users can access NSRR Cloud hosted datasets using their existing sleepdata.org token. 
 
Currently, NSRR Cloud is available only from AWS Cloud services.

## Hosted Datasets in Cloud

As of 01 Jan 2022, we are hosting the following dataset(s) in Cloud:

- [Cleveland Family Study](https://sleepdata.org/datasets/cfs){:target="_blank"}

## Get Started with AWS 

Amazon Web Services (AWS) is a Cloud Platform offering a mix of Infrastructure as a Service, Software as a service and Platform as a service. It includes mostly paid services, although there is an AWS Free-Tier option available with limited services. To learn more, visit [AWS Free-Tier](https://aws.amazon.com/free/){:target="_blank"}.

Click [here](./aws-getting-started.md) for step-by-step documentation on getting started with AWS.

NSRR Cloud datasets are hosted in us-east-1 region. We **strongly recommend** that users create AWS EC2 (compute) resources in AWS within us-east-1 (N. Virginia) region only, as the data transfer is free within the region. 


## Access NSRR Cloud resources

One of the prerequisites for accessing NSRR Cloud resources is to have Python3 available in the OS. If you don't have Python version 3 installed, then follow the [Python3 installation](./install-python.md) guide.


[nsrr](https://pypi.org/project/nsrr){:target="_blank"} - a Python-based Client library is available for users to access NSRR Cloud resources. This library is compatible with Mac, Linux and Windows (tested on win10 PowerShell with admin privileges).

Run the command below to install nsrr library:

```
pip install nsrr
```

If both version of Python i.e., Python2.x and Python3.x are installed in the OS then you can use the command below to call Python3 based pip using:

`python3 -m pip install nsrr` or
`pip3 install nsrr`

### Usage

This section of the documentation covers usage of 'CFS' dataset as an example.

To learn about different parameters, use the help argument:

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

To download subject-specific files from a dataset:

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

## Sleep analysis workflow

Our team has documented below example workflows for sleep researchers to optimally utilize Cloud resources,

[Analysis using MATLAB](./matlab-workflow.md)

[Analysis using Luna](./luna-workflow.md)


## Contact us

If you have any question or suggestion, feel free to reach out to us at support@sleepdata.org

## About

[NSRR](https://sleepdata.org){:target="_blank"} is an NHLBI resource for the sleep research community.

