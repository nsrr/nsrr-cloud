import os
import sys
from nsrr import nsrr
import argparse


VERSION_MAJOR='0'
VERSION_MINOR='2'
VERSION_PATCH='0'

def main() -> None:

    desc_text="""This library provides access to Sleep research resources hosted by NSRR
    
    Usage:  nsrr --list-access --token-file token.txt
            nsrr cfs --list-files
            nsrr cfs/polysomnography/edfs --list-files
            nsrr cfs --list-directories
            nsrr cfs --list-subjects
            nsrr cfs -d --subject 800002 --decompress
            nsrr -d cfs/forms 
            nsrr -d cfs --force"""
    try:
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description=desc_text, add_help=False, usage=argparse.
    SUPPRESS)
        parser.add_argument("--list-access",help="list all datasets and access approval of a user", action="store_true")
        parser.add_argument("dataset",help="input dataset name or file/folder path", nargs='?' ,type=str)
        parser.add_argument("-l","--list-files",help="list all the files in the dataset", action="store_true")
        parser.add_argument("--list-directories",help="list all the directories in the dataset", action="store_true")
        parser.add_argument("--list-subjects",help="list all the subjects in the dataset", action="store_true")
        parser.add_argument("-d","--download",help="perform download operation", action="store_true")
        parser.add_argument("--subject",help="input subject name to download subject specific files", type=str)
        parser.add_argument("-t","--token-file",help="input user token in a file")
        parser.add_argument("--force",help="force re-download of the requested files", action="store_true")
        parser.add_argument("--no-md5",help="use file size for file download integrity check",action="store_true")
        parser.add_argument("--decompress", help="decompress and delete original compressed EDFZ file(s)", action="store_true")
        parser.add_argument("-v", "--version", help="list the current version of the library", action="store_true")
        parser.add_argument("-h", "--help", help="list all command options of the library", action="help")

        if len(sys.argv)==1:
            parser.print_help(sys.stderr)
            sys.exit(0)

        args=parser.parse_args()

        if not len(sys.argv) < 11: 
            print("Error: Invalid run command, use --help argument to learn more")
            raise SystemExit()
        if args.version and len(sys.argv)==2:
            print("nsrr version "+VERSION_MAJOR+"."+VERSION_MINOR+"."+VERSION_PATCH)
            return
        if args.dataset and args.list_subjects and len(sys.argv)==3:
            nsrr.list_all_subjects(args.dataset)
            return
        if args.dataset and args.list_files and len(sys.argv)==3:
            nsrr.list_all_files(args.dataset)
            return
        if args.dataset and args.list_directories and len(sys.argv)==3:
            nsrr.list_all_directories(args.dataset)
            return
        if args.list_access:
            if args.token_file:
                allowed_arguments=3 
                for arg in sys.argv:
                    if '-t' in arg and not '=' in arg:
                        allowed_arguments+=1
                if(len(sys.argv) == allowed_arguments):  
                    user_token=nsrr.read_token_from_file(args.token_file)
                    nsrr.get_user_access(user_token)
                    return
            else:
                if(len(sys.argv) ==2):
                    user_token=nsrr.get_input_token()
                    nsrr.get_user_access(user_token)
                    return
        if args.download and args.dataset:
            user_token=''
            allowed_arguments=3
            if args.force:
                allowed_arguments+=1
            if args.no_md5:
                allowed_arguments+=1
            if args.decompress:
                allowed_arguments+=1
            if args.token_file:
                for arg in sys.argv:
                    if '-t' in arg and not '=' in arg:
                        allowed_arguments+=1
                allowed_arguments+=1
                user_token=nsrr.read_token_from_file(args.token_file)
            else:
                user_token=nsrr.get_input_token()
            if args.subject:
                for arg in sys.argv:
                    if '--s' in arg and not '=' in arg:
                        allowed_arguments+=1
                allowed_arguments+=1
                if(len(sys.argv) == allowed_arguments):
                    nsrr.download_subject_files(user_token, args.dataset, args.subject, args.force, args.no_md5, args.decompress)
                    return
            else:
                if(len(sys.argv) == allowed_arguments):
                    nsrr.download_all_files(user_token, args.dataset, args.force, args.no_md5, args.decompress)
                    return
        print("Error: Invalid run command, use --help argument to learn more")
    except KeyboardInterrupt as e:
        print("\n")
        print('{0:<50}'.format('ERROR: User Keyboard Interrupt received, exiting now...'))
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print(' ERROR: User Keyboard Interrupt received, exiting now...')
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)
