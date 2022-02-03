---
layout: default
title: Sleep analysis workflow using Luna
description: Example workflow 2
---

[Back to NSRR Cloud](./index.md)

# Sleep analysis workflow using Luna

## Luna Overview

Luna is an open-source C/C++ software package for manipulating and analyzing polysomnographic recordings, with a focus on the sleep EEG.

Luna is a very well-documented tool and it is recommend to visit [Luna Documentation](https://zzz.bwh.harvard.edu/luna){:target="_blank"} website to learn in detail about installation and different commands for sleep EEG analysis. 


## Workflow

List all the subjects of CFS dataset:

```
nsrr cfs --list-subjects
```

Now download files specific to a single subject and perform the analysis:

```
nsrr cfs -d --subject 800002
```

The above command will download file(s) specific to subject 800002. Now we will apply Luna  commands to generate a sample list and perform analysis functions:

```
luna --build cfs > s.lst
```

Generate summaries for the EDFs:

```
luna s.lst -s DESC
```

`insert your analysis code here`

Once sleep analysis processing is completed, you can delete the files of subject 800002 and save your results.

Similarly, we can loop over each subject within the CFS dataset and perform the above analysis.

If bash scripting is easier for you then you can bundle up the above commands into bash script and perform the analysis. 


## NSRR Automated Pipeline

NSRR team has also created [NAP](https://gitlab-scm.partners.org/zzz-public/nsrr){:target="_blank"} which internally utilizes the Luna tool to perform a multitude of Analysis operations in bulk manner.

For collaboration/contribution to NAP, feel free to contact us at support@sleepdata.org


## Export results

It is generally a good practice to export the sleep analysis results to keep the EC2 instance storage size in check and to safeguard against any type of accidental loss of information from the EC2 instance. Some of the export options include,

- Your local machine (Data transfer cost is applicable)
- AWS Cloud Storage (S3) (Free data transfer within the same region)

In this documentation, we are not planning to cover Data transfer between EC2 and S3 buckets. Below are couple of useful links in case you want to explore more,
- [AWS CLI prerequisites](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-prereqs.html){:target="_blank"}
- [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html){:target="_blank"}
- [AWS CLI configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html){:target="_blank"}
- [S3 reference](https://docs.aws.amazon.com/cli/latest/reference/s3/){:target="_blank"}