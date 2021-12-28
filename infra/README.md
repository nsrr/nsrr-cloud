# infra

Sub-component of NSRR Cloud for setting up AWS infrastructure using Terraform

## Developer guide

### Initialization

Terraform Initialization for AWS S3 backend:

terraform init -backend-config="access_key=<your access key>" -backend-config="secret_key=<your secret key>"

Note: For the setup of NSRR Cloud, we are using bucket nsrr-cloud-tf-backend in account xxxxxxxxxx

### Dry run

Run below command to perform dry run of the terraform files

`terraform plan`

### Deploy infrastructure

Once dry run output/changes are verified, infrastructure can be deployed using,
`terraform apply`