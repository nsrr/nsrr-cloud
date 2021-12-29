# nsrr-cloud authentication and authorization system

Sub-component of NSRR Cloud providing authentication and authorization to access NSRR Cloud resources

## Developer guide

### Prerequisites
Following installation are necessary to start development,
- Node.js (version >=16)
- Python (version >=3.6)

### Initialization

Clone the code into the workspace and run the below command to install required node.js libraries,

`npm install`

And set up a '.env' file with following secrets,
- DB_USER
- DB_HOST
- DB_DATABASE
- DB_PASSWORD
- DB_PORT
- SIGN_KEY
- ENC_KEY
- ENC_IV
- AWS_ACCESS_KEY
- AWS_SECRET_KEY
- AWS_REGION
- S3_PUBLIC_FILES
- S3_DATASET_PREFIX


### Add authn/authz data to RDS
Use the scripts in 'auth_data_transfer' folder (specific  to MGB server, update them as needed),
- To encrypt auth data and transfer to AWS S3
- To download and decrypt and upload to AWS RDS 

### Run scripts

Run the script 'get_s3_files_list.js' to get metadata of hosted datasets from S3 buckets,

`ex: node get_s3_files_list.js cfs`

Repeat the above command per dataset. Also, you will have to run the above command everytime any new file are added or deleted from a dataset.

Run the script 'get_aws_ips.py' to get IP addresses of AWS ecosystem,

`python3 get_aws_ips.py`

### Run server

Once all the above steps are completed, you can start the auth server,

`node server.js`