#!/usr/bin/python3
import requests
from requests.structures import CaseInsensitiveDict
import json
import getpass
from pathlib import Path 
import hashlib

# Global variables 
#API_SERVER='https://dev-cloud.sleepdata.org/api/v1'
API_SERVER='https://cloud.sleepdata.org/api/v1'
#API_SERVER='http://localhost:9002/api/v1'

def get_input_token():
    enter_pass_text="""
    Get your token here: https://sleepdata.org/token
    Your input is hidden while entering token.
    Enter your token:
    """
    return getpass.getpass(enter_pass_text)

def read_token_from_file(file_name):
    try:
        f=open(file_name,'r')
        user_token=f.readline().strip()
        f.close()
        return user_token
    except Exception as e:
        print("ERROR: the following error occured while reading token from input file")
        print(e)

def get_user_access(user_token):
    headers = CaseInsensitiveDict()
    headers= {'token': user_token}
    try:
        resp = requests.get(API_SERVER+'/list/access', headers=headers)
        if(resp.ok and resp.status_code == 200):
            user_access_json=json.loads(resp.content)
            if(user_access_json["datasets"]):
                datasets=", ".join(list(user_access_json["datasets"]))
                print("Approved access to following dataset(s): ",datasets)
        else:
            print("ERROR: Unable to list user access, please verify input token, approved DUA and try again")
    except Exception as e:
        print("ERROR: Unable to process request at this time, try again later")

def get_auth_token(user_token, dataset_name):
    headers = CaseInsensitiveDict()
    headers={'token': user_token}
    payload = {'dataset_name': dataset_name}
    try:
        resp = requests.get(API_SERVER+'/auth-token', params=payload, headers=headers)
        if(resp.ok and resp.status_code == 200):
            auth_token=json.loads(resp.content)["auth_token"]
        else:
            auth_token=False
        return auth_token
    except Exception as e:
        return False

def get_download_url(auth_token=None, file_name=None):
    payload = {'file_name': file_name}
    try:
        if(auth_token):
            auth_headers = CaseInsensitiveDict()
            auth_headers = {'Authorization': 'Bearer %s' %auth_token}
            resp = requests.get(API_SERVER+'/download/url/controlled', params=payload, headers=auth_headers)
        else:
            resp = requests.get(API_SERVER+'/download/url/open', params=payload)
        if(resp.ok and resp.status_code == 200):
            return resp.content
        else:
            return False
    except Exception as e:
        return False


def download_file(url, download_file_name, no_md5, metadata):
    try:
        file_name_split=download_file_name.split("/")
        file_name=file_name_split[-1]
        file_download_path="/".join(file_name_split[:-1])
        path = Path(str(Path.cwd())+"/"+file_download_path)
        if not path.exists():
            path.mkdir(parents= True, exist_ok= True)
        response=requests.get(url, stream=True)
        f_download=path / file_name
        
        with f_download.open("wb+") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
            f.close()

        if no_md5:
            if not f_download.stat().st_size == metadata["size"]:
                delete_file_path=Path(str(Path.cwd())+"/"+download_file_name)
                delete_file_path.unlink()
                return False
            else:
                print("Downloaded file: ",download_file_name)   
        else:
            md5_object = hashlib.md5()
            block_size = 128 * md5_object.block_size
            md5_file = open(f_download, 'rb')
            chunk = md5_file.read(block_size)
            while chunk:
                md5_object.update(chunk)
                chunk = md5_file.read(block_size)
            md5_hash = md5_object.hexdigest()
            md5_file.close()
            if not md5_hash == metadata["md5"]:
                delete_file_path=Path(str(Path.cwd())+"/"+download_file_name)
                #delete_file_path.unlink()
                return False
            else:
                print("Downloaded file: ",download_file_name)
        return True
    except Exception as e:
        print("exception is ",e)
        return False

def get_all_files_list(dataset_name):
    payload = {'dataset_name': dataset_name}
    try:
        resp = requests.get(API_SERVER+'/list/all-files', params=payload)
        if(resp.ok and resp.status_code == 200):
            return resp.content
        else:
            return False
    except Exception as e:
        return False


def download_wrapper(all_files,user_token, dataset_name, force, no_md5):
    all_files=json.loads(all_files)
    for f in all_files["open_files"]:
        if not force:
            file_path=Path(str(Path.cwd())+"/"+f)
            if file_path.is_file():
                continue
        url=get_download_url(file_name=f)
        if(url):
            download_success=download_file(url,f,no_md5,all_files["open_files"][f])
            if not download_success:
                print("ERROR: Unable to download file {0}".format(f))
        else:
            print("ERROR: Unable to get download URL for file {0}, try again later".format(f))

 
    if(all_files["controlled_files"]):
        # get bearer token
        for f in all_files["controlled_files"]:
            f_with_dataset=dataset_name+"/"+f
            if not force:
                file_path=Path(str(Path.cwd())+"/"+f_with_dataset)
                if file_path.is_file():
                    continue
            auth_token=get_auth_token(user_token, dataset_name)
            if(auth_token):
                url=get_download_url(auth_token=auth_token,file_name=f)
                if(url):
                    download_success=download_file(url,f_with_dataset,no_md5,all_files["controlled_files"][f])
                    if not download_success:
                        print("ERROR: Unable to download file {0}".format(f))
                else:
                    print("ERROR: Unable to get download URL for file {0}, try again later".format(f))
            else:
                print("ERROR: Unable to download controlled files, try again later")


def download_all_files(user_token, dataset_name, force, no_md5):
    all_files=get_all_files_list(dataset_name)
    if(all_files):
        download_wrapper(all_files,user_token, dataset_name, force, no_md5)

    else:
        print("ERROR: Unable to retrieve files list of dataset {0}, check list of cloud hosted datasets and try again".format(dataset_name))


def get_subject_files_list(dataset_name,subject):
    payload = {'dataset_name': dataset_name, 'subject': subject}
    try:
        resp = requests.get(API_SERVER+'/list/subject-files', params=payload)
        if(resp.ok and resp.status_code == 200):
            return resp.content
        else:
            return False
    except Exception as e:
        return False

def download_subject_files(user_token,dataset_name,subject, force, no_md5):
    all_files=get_subject_files_list(dataset_name,subject)
    if(all_files):
        download_wrapper(all_files,user_token, dataset_name, force, no_md5)
    else:
        print("ERROR: Unable to retrieve files list of subject {0} of dataset {1}, check list of cloud hosted datasets and try again".format(subject,dataset_name))



def list_all_subjects(dataset_name):
    payload = {'dataset_name': dataset_name}
    try:
        resp = requests.get(API_SERVER+'/list/all-subjects', params=payload)
        if(resp.ok and resp.status_code == 200):
            all_subjects_json=json.loads(resp.content)
            if(all_subjects_json["subjects"]):
                all_subjects=", ".join(list(all_subjects_json["subjects"]))
            print("Subjects are: ",all_subjects)
        else:
            print("ERROR: Unable to list all subject of {0} dataset, check list of cloud hosted datasets and try again".format(dataset_name))
    except Exception as e:
        print("ERROR: Unable to process request at this time, try again later")

