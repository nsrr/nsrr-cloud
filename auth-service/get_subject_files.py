#!/usr/bin/env python3
import json
import sys

dataset_name=''
if not len(sys.argv) == 2:
    print("missing dataset name argument")
else:
    dataset_name=sys.argv[1]

metadata_list=[]
with open("metadata/"+dataset_name.strip()+"_metadata.json", 'r') as f:
    metadata_list=json.load(f) 

subjects_list=[]
with open("metadata/"+dataset_name.strip()+"_all_subjects.txt",'r') as f:
    subjects_list=[i.strip("\n") for i in f.readlines()]

final_list={}
for subject in subjects_list:
    final_list[subject]={}
    
    final_list[subject]["open_files"]={}
    for f in metadata_list["open_files"]:
        if subject in f:
            final_list[subject]["open_files"][f]=dict(metadata_list["open_files"][f])

    final_list[subject]["controlled_files"]={}
    for f in metadata_list["controlled_files"]:
        if subject in f:
            final_list[subject]["controlled_files"][f]=dict(metadata_list["controlled_files"][f])

with open("metadata/"+dataset_name.strip()+"_metadata_by_subject.json",'w') as f:
    json.dump(final_list,f)