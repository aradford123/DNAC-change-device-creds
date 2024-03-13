#!/usr/bin/env python
from argparse import ArgumentParser
from dnacentersdk import api
from dnacentersdk.exceptions import ApiError
import logging
import json
from  time import sleep, time, strftime, localtime
from dnac_config import DNAC, DNAC_USER, DNAC_PASSWORD
from task import Task, TaskTimeoutError, TaskError
logger = logging.getLogger(__name__)
timeout = 10

def change_device(dnac, password, snmpv2, device ):
    print(f'changing password for {device}:',end='')
    payload = {
                "cliTransport": "ssh",
                "userName": "sdn",
                "enablePassword": password,
                "ipAddress": [
                            device
                            ],
                "password": password,
                "computeDevice": False,
                "netconfPort" : 830
            }

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

    url = "api/v1/network-device"
    task = dnac.custom_caller.call_api(method="PUT", resource_path=url, data=json.dumps(payload) )
    logger.debug(task)
    try:
        t = Task(dnac, task.response.taskId)
        result = t.wait_for_task(timeout=timeout)
        logger.debug(result)
        elapsed = int((result.response.endTime - result.response.startTime)/ 1000)
        if result.response.progress == "Error":
            message = result.response.failureReason
        else:
            failure = result.response.get('failureReason','')
            if failure != '':
                failure = f' - ({failure})'
            message = f'{result.response.progress}  {failure}'
        print("Task completed:{} - elapsed time:{}sec".format(message, elapsed))
    except TaskTimeoutError as e:
        print(e)


    
def main(dnac, password, snmpv2,devices):
    for device in devices:
        change_device(dnac, password, snmpv2,device)

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    parser.add_argument('--snmpv2', action='store_true', default=False,
                        help="snmpv2")
    parser.add_argument('--password',  type=str, required=True,
                        help='new passowrd')
    parser.add_argument('--dnac',  type=str,default=DNAC,
                        help='dnac IP')
    parser.add_argument('arguments', nargs='*', help='Additional arguments as a list.')
    args = parser.parse_args()

    if args.v:
        root_logger=logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        root_logger.addHandler(ch)
        logger.debug("logging enabled")

    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    DNAC = args.dnac
    dnac = api.DNACenterAPI(base_url='https://{}:443'.format(DNAC),
                                #username=DNAC_USER,password=DNAC_PASSWORD,verify=False,debug=True)
                                username=DNAC_USER,password=DNAC_PASSWORD,verify=False)
    main(dnac, args.password, args.snmpv2,args.arguments)
