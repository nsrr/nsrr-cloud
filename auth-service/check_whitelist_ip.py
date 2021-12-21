#!/usr/bin/env python3
import ipaddress
import sys
import json

def check_ip(ip):
    ip_range_list=[]
    with open("whitelist_ips/aws_ips.json", 'r') as f:
        ip_range_list = json.load(f)
    check_value=False
    for ip_range in ip_range_list:
        if(ipaddress.ip_address(ip) in ipaddress.ip_network(ip_range,strict=False)):
            check_value=True
    print(check_value)

if __name__ == "__main__":
    ip=sys.argv[1]
    check_ip(ip)