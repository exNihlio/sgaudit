#!/usr/bin/env python3

## Unit tests to validate main.py

import boto3
import json
import os
import sys

class TextColors():
    def __init__(self):
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARN = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

c = TextColors()

def main():
    # Exit code
    e = 0
    path = os.path.dirname(os.path.realpath(__file__))
    # Need to pass in the path so this function can always open regions.json
    getRegionsRC = testGetRegions(path)
    if getRegionsRC == 0:
        print(f"{c.OKGREEN}getRegions() passed{c.ENDC}") 
    else:
        if type(getRegionsRC) is int:
            print(f"{c.FAIL}getRegions() failed: {getRegionsRC} regions not found{c.ENDC}")
            e = 1
        else:
            print(f"{c.FAIL}getRegions() failed: {getRegionsRC}{c.ENDC}")
            e = 1

    # Test getInstances() function
    getInstancesRC = testGetInstances()
    if getInstancesRC == 0:
        print(f"{c.OKGREEN}getInstances() passed{c.ENDC}")
    else:
        print(f"{c.FAIL}getInstances() failed: {getInstancesRC}{c.ENDC}")
        e = 1

    sys.exit(e)

## Test the getRegions function
def testGetRegions(path):
    # Import from main.py, only a single function at a time
    from main import getRegions
    # Default return code
    rc = 0
    # Default list of valid AWS regions, to act as a master to compare our
    # received data from inspecting regions.
    validRegions = json.loads(open(f'{path}/data/regions.json').read())
    ec2 = boto3.client('ec2')
    # Check if our getRegions function returns correctly
    try:
        testRegions = getRegions(ec2)
    except:
        return "Err: Could not extract regions. Malformed data?"
    # Iterate through the regions JSON dict, if any of these are not in
    # the list of regions returned by getRegions(), something went wrong.
    for i in validRegions['regions']:
        if i not in testRegions:
            rc += 1
    return rc

def testGetInstances():
    from main import getInstances
    rc = 0
    regions = ['us-west-1', 'us-west-2', 'us-east-1', 'us-east-2']
    for r in regions:
        #ec2 = boto3.client('ec2')
        try:
            instances = getInstances(r)
        except:
            return "Err: Could not retrieve instances."

        try:
            statusCode = instances['ResponseMetadata']['HTTPStatusCode']
        except:
            return "Err: Could not extract status code. Malformed data?"

        if statusCode != 200:
            return f"Err: HTTP: {statusCode}"
    
    return rc
        
if __name__ == '__main__':
    main()
