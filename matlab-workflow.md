---
layout: default
title: Sleep analysis workflow using MATLAB
description: sample workflow
---

[Back to NSRR Cloud](./index.md)

# Sleep analysis workflow using MATLAB


## Prerequisite:
 
[Install MATLAB](https://www.mathworks.com/help/install/install-products.html){:target="_blank"}


### Loading MATLAB

In Windows machine for loading MATLAB, type `matlab` within the command prompt or click on MATLAB desktop icon (if available). This will open the MATLAB interactive software where you can type in the MATLAB functions given in the examples below (EDF data and Annotations).


For Linux terminal use:

```
$ matlab
```

For loading specific version of MATLAB, for e.g 2020b use: 

```
$ module load matlab/R2020b
```
 
Alternatively, you can call the MATLAB software without the interactive terminal using:
```
$ matlab -nodisplay
```

### EDF Data

Once you have the MATLAB software installed and loaded (we recommend MATLAB R2020b since it has a in-built function for reading European Data Format (EDF) or EDF+ files, the common format for raw signals file in NSRR), use the command below to import the data:

```	
data = edfread('example.edf');
```

For more help, please refer to [MATLAB edfread](https://www.mathworks.com/help/signal/ref/edfread.html){:target="_blank"}.
 
*data* will be a MATLAB table with each column corresponding to different signals. For example, if a raw data file had EEG and SpO2 in the EDF file, data will have "Record Time", "EEG","SpO2" as column variables.
 

### Annotations

 For importing annotation (XML) files to MATLAB you can use the in-built function `xmlread` which gives you a Document Object Model node representing the document (a little bit harder to use - for more help please refer to https://www.mathworks.com/help/matlab/ref/xmlread.html):
	
	DOMnode =  xmlread('example.xml')
	
 Alternatively, you can use `xml2struct` which is available to download using this [link](https://www.mathworks.com/matlabcentral/fileexchange/28518-xml2struct) (you may need to have a Mathworks/MATLAB account)

```
S=xml2struct('example.xml');
```
 This will give you a structure array which will be easier to handle for further processing.

###  Execute MATLAB Functions Non-interactively

 If you want to execute the above functions in a non-interactive way:
 
```
matlab -nodisplay -batch  "edfread($example.edf,$data)" -sd folder -logfile output.log
```

where,
 *-sd folder* is used to set the initial working folder (where MATLAB software is located)
 *-logfile output.log* will create a log file which can be useful for troubleshooting any errors, if present.


## Workflow

This section of the documentation covers usage of 'CFS' dataset as an example.


List all subjects of CFS dataset:

```
nsrr cfs --list-subjects
```

Now download files specific to a single subject and perform the analysis:

```
nsrr cfs -d --subject 800002
```

The command above will download file specific to subject 800002. Now we will apply our  MATLAB functions (as documented above) to read the files:

```
matlab -nodisplay -batch  "edfread($cfs/polysomnography/edfs/cfs-visit5-800002.edf,$data)" -sd folder -logfile output.log
```

`insert your analysis code here`

Once your sleep analysis processing is completed, you can delete the files of subject 800002 and save your results.

Similarly, we can loop over each subject within the CFS dataset and perform the above analysis.

If bash scripting is easier for you then you can bundle up the above commands into bash script and perform the analysis. 



## Export results

It is generally a good practice to export the sleep analysis results to keep the EC2 instance storage size in limit and to safeguard against any type of accidental loss of information from the EC2 instance. Some of the export options include:

- Your local machine (Data transfer cost is applicable)
- AWS Cloud Storage (S3) (Free data transfer within the same region)

In this documentation, we are not planning to cover Data transfer between EC2 and S3 buckets. Here are couple of useful links in case you want to explore more,

- [AWS CLI prerequisites](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-prereqs.html){:target="_blank"}
- [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html){:target="_blank"}
- [AWS CLI configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html){:target="_blank"}
- [S3 reference](https://docs.aws.amazon.com/cli/latest/reference/s3/){:target="_blank"}
