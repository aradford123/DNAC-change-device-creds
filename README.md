# DNAC-change-device-creds
This script allows you to change the inventory credentials of devices in Catalyst Center (DNA Center) via API.


## Getting stated
First (optional) step, create a vitualenv. This makes it less likely to clash with other python libraries in future.
Once the virtualenv is created, need to activate it.
```buildoutcfg
python3 -m venv env3
source env3/bin/activate
```

Next clone the code.

```buildoutcfg
git clone https://github.com/aradford123/mapsiteSSID.git
```

Then install the  requirements (after upgrading pip). 
Older versions of pip may not install the requirements correctly.
```buildoutcfg
pip install -U pip
pip install -r requirements.txt
```

Edit the dnac_vars file to add your DNAC and credential.  You can also use environment variables.

## Credentials

You can either add environment variables, or edit the  dnac_config.py file
```
import os
DNAC= os.getenv("DNAC") or "sandboxdnac.cisco.com"
DNAC_USER= os.getenv("DNAC_USER") or "devnetuser"
DNAC_PORT=os.getenv("DNAC_PORT") or 8080
DNAC_PASSWORD= os.getenv("DNAC_PASSWORD") or "Cisco123!"
```

## Edit the SNMPv2/v3 credentials.
The SNMP credentials are hardcoded in the script at present.  It is pretty easy to edit them.  I might do this a different way in future

```
    if snmpv2:
        payload["snmpVersion"]= "v2"
        payload["snmpROCommunity"] = "public"
    else:
        payload["snmpVersion"]= "v3"
        payload["snmpAuthPassphrase"] = "adam1234"
        payload["snmpAuthProtocol"] = "sha"
        #SNMPV3 mode. Supported values: noAuthnoPriv, authNoPriv, authPriv
        payload["snmpMode"] = "authPriv"
        payload["snmpPrivPassphrase"] = "adam1234"
        # only supported for assurance prior to 2.3.7.4
        payload["snmpPrivProtocol"] = "AES128"
        payload["snmpUserName"] = "adam"
```
## Running the program

The script takes a mandatory password (it is using the same password for exec and enable).  

This is specified with the --password argument.

Anything after this is considered a list of devices to update.
```
./change_device_password.py --password sdn123 10.10.21.200 
changing password for 10.10.21.200:Task completed:Inventory service updating devices - (None) - elapsed time:1sec
```

This example forces an snmpv2 credential
```
./change_device_password.py --password sdn123 10.10.21.200 --snmpv2
changing password for 10.10.21.200:Task completed:Inventory service updating devices - (None) - elapsed time:4sec
```
