---
layout: default
title: Sleep analysis workflow using MATLAB
description: sample workflow
---

[Back to NSRR Cloud](./index.md)

# Sleep analysis workflow using MATLAB


## MATLAB overview
 
Follow the MATLAB official documentation to [Install MATLAB](https://www.mathworks.com/help/install/install-products.html){:target="_blank"}.

To load MATLAB,
-  In Windows machine, type `matlab` within the command prompt or click on MATLAB desktop icon (if available).
- In Linux/Mac, type `matlab` in terminal


## Workflow

This section of the documentation covers usage of 'CFS' dataset as an example.


List all subjects of CFS dataset:

```
nsrr cfs --list-subjects
```

Now, download files specific to a single subject and perform the analysis:

```
nsrr cfs -d --subject 800002
```

The command above will download file specific to subject 800002. Now, apply MATLAB (R2020b) function to read the EDF file:

```
matlab -nodisplay -r "edfread('cfs/polysomnography/annotations-events-nsrr/cfs-visit5-800002.edf');exit"
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
