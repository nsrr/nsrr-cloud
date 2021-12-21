#!/bin/bash

# Pre-requisite's to run the above file
#  1. pg view 'nsrr_cloud_view' is configured in pg db 
#  2. Files are available -> get_nsrr_cloud_data.sql, nsrr_auth_data.txt, nsrr_cloud_enc_secret.txt
#  3. AWS profile with a name confgiured to access the associated s3 bucket
# PSQL file to dump auth view from MGB PG server
# cat get_nsrr_cloud_data.sql 
# \copy (select * from public.nsrr_cloud_view) to nsrr_auth_data.txt
#
# Daily Crontab 
# 5 0 * * * source /home/sx409/authn_authz_upload_to_s3.sh > /home/sx409/cron_logs/`date +\%Y-\%m-\%d`update_authn_authz_data.log 2>&1; mailx -s "Authn and Authz update log" sagarwal12@bwh.harvard.edu < /home/sx409/cron_logs/`date +\%Y-\%m-\%d`update_authn_authz_data.log

PGPASSWORD=xxxxxxxxxx psql --host=pgsql2.research.partners.org --username=sleepdata_read_staging --port=5432 --dbname=sleepdata_staging -f /home/sx409/get_nsrr_cloud_data.sql 
psql_status=$?
if [[ ${psql_status} -eq 0 ]]; then
    openssl enc -aes-256-cbc -salt -in /home/sx409/nsrr_auth_data.txt -out /home/sx409/nsrr_auth_data.txt.enc -pass file:"/home/sx409/nsrr_cloud_enc_secret.txt"
    enc_status=$?
    if [[ ${enc_status} -eq 0 ]]; then
        # tomorrow's date
         tomorrow_date=$(date -d '+1 day' +%Y-%m-%d)
        # copy to aws s3 bucket
        /usr/local/bin/aws s3 --profile xxxxxxxxxxx cp /home/sx409/nsrr_auth_data.txt.enc s3://test-nsrr-authn-authz-data/${tomorrow_date}/nsrr_auth_data.txt.enc
        upload_status=$?
        if [[ ${upload_status} -eq 0 ]]; then
            echo "Authn/Authz data uploaded to S3 succesfully"
        else
            echo "AWS upload failed, try again"
            exit 1
        fi
    else
        echo "Encryption failed, try again"
        exit 1
    fi
else
    echo "PSQL command failed, try again"
    exit 1
fi