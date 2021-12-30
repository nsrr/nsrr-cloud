# NSRR Cloud

Over the past decade, we have been experiencing a gradual increase in adoption of Cloud usage in IT industry. One of the main benefits of Cloud is on-demand, wide-variety of scalable IT resources that users can access at their fingertips. 

NSRR has been traditionally serving Sleep reseearchers with resources using On-premise hosting services. For Sleep researhcers to fully realize potential of IT Cloud services, we are migrating Sleep research resources to Cloud based hosting solution. Below listed are the potential benefits of nsrr-cloud:
- Users can skip maintaining individual copies of Sleep studies; Users can access files to perform analysis and delete them as needed
- Access partial datasets to enable researchers with smaller compute and storage resources to perform analysis
- Uniform network bandwidth serving Sleep Studies

As of 01 Jan 2022, we have hosted CFS dataset in Cloud. Users can access CFS using their existing Sleepdata.org token. And currently NSS Cloud is available only from AWS cloud services.

## Get Started with AWS Cloud

Follow the below article to get started with AWS Cloud,

[Create and activate AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)

Once the AWS account is created, you can start EC2 (compute) instance,

[AWS EC2 getting started](https://aws.amazon.com/ec2/getting-started/)

## Access NSRR Cloud resources

Python Client library package is available at [nsrr-cloud](https://pypi.org/project/nsrr-cloud) and can be installed using following command,

`pip install nsrr-cloud`

It is recommended to use python version 3.8.x.

Compatible with Mac, Linux and Windows (tested on win10 powershell with admin privileges).

### Usage

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

Data Integrity check is performed via the following two options.
- (Recommended) md5 checksum value is unique to every file. This option verifies that the downloaded file is exactly the same as being served by NSRR using md5 checksum value comparison. 
- file size check to match with download size of the file hosted by NSRR.

To skip memory intensive data-integrity check,

`nsrr_cloud -d [--dataset=cfs]  --no-md5`

To forcefully download the whole dataset,

`nsrr_cloud -d [--dataset=cfs]  --force`


## Example sleep analysis using matlab 

If you have followed above steps to access NSRR Cloud resources, you should have the following setup completed,
- AWS account and compute instance up and running
- 'nsrr-cloud' python library installed

For this example sleep analysis workflow, we are going to use Matlab tool. You can install matlab by following link - [Install Matlab](https://www.mathworks.com/help/install/install-products.html)


