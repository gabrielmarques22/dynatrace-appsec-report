
# Dynatrace AppSec CSV Exporter

This script generates a CSV file with all application security problems Dynatrace has detected in your environment.




## Requirements

- Python 3.x
- requests package 
    - pip install requests
- API Token with Read Security Problems permission
- Dynatrace Tenant (with Appsec enable) URL
    - SaaS: https://<TenantID>.live.dynatrace.com
    - Managed: https://<ManagedURL OR ClusterActiveGate IP>:443/e/<EnvironmentID>


## Running script

- cd to script folder
- ./AppSecExport.py -u <tenantURL> -t <token>