import os
import sys
from nsrr_cloud import nsrr_cloud
import argparse


# Global variables 
VERSION_MAJOR='0'
VERSION_MINOR='3'
VERSION_PATCH='0'

def main() -> None:
    desc_text="""This library provides access to Sleep resources hosted by NSRR
                example usage: nsrr_cloud -d [--dataset=cfs] [--subject=800002] [--token-file=token.txt]
                               nsrr_cloud --dataset=cfs --list-subjects
                               nsrr_cloud --list-access [--token-file=token.txt]
              """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description=desc_text)
    parser.add_argument("-v", "--version", help="shows the version of NSRR Cloud library", action="store_true")
    parser.add_argument("-d","--download",help="argument to perform download of a dataset", action="store_true")
    parser.add_argument("--subject",help="argument to input subject name for download",type=str)
    parser.add_argument("--list-subjects",help="lists all the subjects in the dataset", action="store_true")
    parser.add_argument("--dataset",help="argument to input dataset name for download",type=str)
    parser.add_argument("--list-files",help="lists all the files in the dataset", action="store_true")
    parser.add_argument("--list-directories",help="lists all the directories in the dataset", action="store_true")
    parser.add_argument("--token-file",help="argument to input User token in a file")
    parser.add_argument("--list-access",help="lists all datasets with approved DUAU of a user", action="store_true")
    parser.add_argument("--force",help="argument to force re-download of requested files/dataset", action="store_true")
    parser.add_argument("--no-md5",help="argument to use file size for file integrity check",action="store_true")
    args=parser.parse_args()
    if not len(sys.argv) < 10: 
        print("Error: Invalid run command, use --help argument to learn more")
        raise SystemExit()
    if args.version and len(sys.argv)==2:
        print("nsrr-cloud version "+VERSION_MAJOR+"."+VERSION_MINOR+"."+VERSION_PATCH)
        return
    if args.dataset and args.list_subjects and len(sys.argv)==3:
        nsrr_cloud.list_all_subjects(args.dataset)
        return
    if args.dataset and args.list_files and len(sys.argv)==3:
        nsrr_cloud.list_all_files(args.dataset)
        return
    if args.dataset and args.list_directories and len(sys.argv)==3:
        nsrr_cloud.list_all_directories(args.dataset)
        return
    if args.list_access:
        if args.token_file and len(sys.argv)==3:
            user_token=nsrr_cloud.read_token_from_file(args.token_file)
            nsrr_cloud.get_user_access(user_token)
            return
        else:
            if(len(sys.argv) ==2):
                user_token=nsrr_cloud.get_input_token()
                nsrr_cloud.get_user_access(user_token)
                return
    if args.download and args.dataset:
        user_token=''
        allowed_arguments=3
        if args.force:
            allowed_arguments+=1
        if args.no_md5:
            allowed_arguments+=1
        if args.token_file:
            allowed_arguments+=1
            user_token=nsrr_cloud.read_token_from_file(args.token_file)
        else:
            user_token=nsrr_cloud.get_input_token()
        if args.subject:
            allowed_arguments+=1
            if(len(sys.argv) == allowed_arguments):
                nsrr_cloud.download_subject_files(user_token, args.dataset, args.subject, args.force, args.no_md5)
                return
        else:
            if(len(sys.argv) == allowed_arguments):
                nsrr_cloud.download_all_files(user_token, args.dataset, args.force, args.no_md5)
                return
    print("Error: Invalid run command, use --help argument to learn more")


if __name__ == "__main__":
    main()
