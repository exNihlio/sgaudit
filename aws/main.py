#!/usr/bin/env python3

import boto3
from json import loads as jload
from json import dumps as jdump

def main():
    # Create boto3 ec2 client
    ec2 = boto3.client('ec2')
    # Collect all the regions in AWS.
    regions = getRegions(ec2)

    for r in regions:
        instances = getInstances(ec2, r)

    print(jdump(instances, indent=4, sort_keys=True, default=str))
    
def getRegions(ec2):
    # Uncomment to test unit test failure (Succeed to fail)
    # return "I am a fancy teapot"
    r = ec2.describe_regions()
    # Create a list of regions
    regionList = [ i['RegionName'] for i in r['Regions'] ]
    return regionList

def getInstances(region):
    # Uncomment to test unit test failure (Succeed to fail)
    # return "I am a fancy teapot"
    # Uncomment to test/return a failing HTTP status code
    # import random
    # randomStatus = random.randint(400, 501)
    # return { "ResponseMetadata": { "HTTPStatusCode": randomStatus }}

    ec2 = boto3.client('ec2', region_name=region)
    return ec2.describe_instances()

def getSecurityGroup(ec2, region, id):
    return None

if __name__ == '__main__':
    main()
