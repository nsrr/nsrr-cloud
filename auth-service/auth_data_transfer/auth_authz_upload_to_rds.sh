#!/bin/bash

# Pre-requisite's to run the above file
#  1. Encrypted nsrr auth data is available in s3 bucket 
#  2. AWS RDS is setup and table is created
#  3. AWS profile with a name confgiured to access the associated s3 bucket
#  4. Files are available -> nsrr_cloud_decryp_secret.txt, nsrr_auth_data.txt.enc, post_data.sql 
#  5. Install openssl version 1.0.2 for decryption (compatibility with MGB server openssl) 
# PSQL file to uload data from s3 to RDS
# cat post_data.sql 
# \copy (select * from public.nsrr_cloud_view) to nsrr_auth_data.txt
#
# Daily Crontab 
# 0 0 * * * source  /root/update_authn_authz_rds/authn_authz_upload_to_rds.sh > /var/log/cron_logs/`date +\%Y-\%m-\%d`update_authn_authz.log 2>&1

today_date=$(date +%Y-%m-%d)
aws s3 --profile xxxxxxxxxx cp s3://test-nsrr-authn-authz-data/${today_date}/nsrr_auth_data.txt.enc /root/update_authn_authz_rds/
download_status=$?
echo "download status is ${download_status}"
if [[ ${download_status} -eq 0 ]]; then
    # decrypt 
    rm -rf /root/update_authn_authz_rds/nsrr_auth_data.txt
    /old-openssl-version-1.0.2k/bin/openssl enc -aes-256-cbc -d -in /root/update_authn_authz_rds/nsrr_auth_data.txt.enc -out /root/update_authn_authz_rds/nsrr_auth_data.txt -pass file:"/root/update_authn_authz_rds/nsrr_cloud_decryp_secret.txt"
    decryp_status=$?
    if [[ ${decryp_status} -eq 0 ]]; then
        # upload to rds
        PGPASSWORD=xxxxxxxxxx  psql --host=xxxxxxxxxx.rds.amazonaws.com  --username=xxxxxxxxxx --port=5432 --dbname=test_nsrr_cloud -f /root/update_authn_authz_rds/post_data.sql
	upload_status=$?
	if [[ ${upload_status} -eq 0 ]]; then
	    echo "Authn/Authz data uploaded to s3 successfully"
	else
	    echo "RDS upload failed, try again"
	    exit 1
        fi
    else
	echo "Decryption failed, try again"
	exit 1
    fi
else
    echo "PSQL command failed, try again"
    exit 1
fi