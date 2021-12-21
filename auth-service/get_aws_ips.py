#!/usr/bin/env python3
import requests
import json

ip_range_list=[]
ip_ranges = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json').json()['prefixes']
for ip_block in ip_ranges:
    ip_range_list.append(ip_block['ip_prefix'])

with open("whitelist_ips/aws_ips.json", 'w') as f:
    json.dump(ip_range_list, f) 