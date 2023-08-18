import time
import requests
import boto3

pingURLSuffix= "/ping"

def get_regions_by_latency(includeRegions=[]):
    ec2_client = boto3.client('ec2')
    regions = ec2_client.describe_regions()['Regions']

    results = []

    for region in regions:
        if len(includeRegions) > 0 and region['RegionName'] not in includeRegions:
            continue
        response, latency = time_http_request("https://"+region['Endpoint']+pingURLSuffix)
        if response.status_code == 200:
            results.append({"region_name": region['RegionName'], "latency": latency})


    results.sort(key=lambda x: x['latency'])

    return results

def time_http_request(url):
    start_time = time.time()
    
    response = requests.get(url)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return response, elapsed_time*1000
