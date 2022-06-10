#!/usr/bin/python
import csv  
import sys, getopt
import requests
import json

def main(argv):

    # Variables
    tenantURL = ''
    token = ''
    data = []
    header={}
    _tenantURL=''
    _token=''
    
    def getSubsequentPages(_nextPageKey):
        print(" ### Getting Subsequent Page ###")
        print("Pagination: " + _nextPageKey)
        response = requests.get(tenantURL + "/api/v2/securityProblems?nextPageKey=" +_nextPageKey, headers=header, verify=False)
        responseJson = response.json()
        securityProblems = responseJson["securityProblems"]
        for problem in securityProblems:
            data.append([
                problem["status"],
                problem["displayId"],
                problem["title"],
                problem["externalVulnerabilityId"],
                problem["cveIds"],
                problem["packageName"],
                problem["technology"],
                problem["url"]
            ])
        try: 
            nextPageKey = responseJson["nextPageKey"]
            return nextPageKey
        except:
            return False


    print("### Starting Script ###")
    # parameters
    try:
      opts, args = getopt.getopt(argv,"hu:t:",["u=","t="])
    except getopt.GetoptError:
        print('AppSecExport.py -u <tenantURL> -t <token>')
        sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
        print('AppSecExport.py -u <tenantURL> -t <token>')
        sys.exit()
      elif opt in ("-u"):
         _tenantURL = arg
      elif opt in ("-t"):
         _token = arg
    
    if _tenantURL=="" or _token == "":
        print('Missing parameters -> AppSecExport.py -u <tenantURL> -t <token>')
        sys.exit()
    else:
        tenantURL = _tenantURL
        token = _token

    # API Request Generating the first page
    header = {
        "Authorization" : "Api-Token " + token
    }
    print("### Getting First Page ###")
    response = requests.get(tenantURL + "/api/v2/securityProblems", headers=header, verify=False)
    responseJson = response.json()
    try: 
        totalCount = 0
        totalCount = responseJson["totalCount"]
        print("### Total Problems: " + str(totalCount) + " ###")

    except:
        print('Connection Failed. Check your tenant URL and API Token (Read Security Problems)')
        sys.exit()
    pageSize = responseJson["pageSize"]
    try: 
        nextPageKey = responseJson["nextPageKey"]
    except:
        nextPageKey = False
    securityProblems = responseJson["securityProblems"]
    if len(securityProblems) < 1:
        print('No problems fetched')
        sys.exit()
    for problem in securityProblems:
        data.append([
            problem["status"],
            problem["displayId"],
            problem["title"],
            problem["externalVulnerabilityId"],
            problem["cveIds"],
            problem["packageName"],
            problem["technology"],
            problem["url"]
        ])

    # loop through subsequent pages feeding data
    while nextPageKey != False:
        nextPageKey = getSubsequentPages(nextPageKey)

    
    generateCSV(data) 





def generateCSV(_data):
    print("### Generating CSV ###")

    header = ['status', 'displayId', 'title', 'externalVulnerabilityId','cveIds', 'packageName', 'technology', 'url']

    with open('appsecReport.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        # write the data
        writer.writerows(_data)

if __name__ == "__main__":
   main(sys.argv[1:])