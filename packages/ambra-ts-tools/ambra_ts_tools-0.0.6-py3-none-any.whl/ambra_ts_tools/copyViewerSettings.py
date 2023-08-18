#from time import sleep
# from ambra_sdk.api import Api 
import requests
#from re import findall, match
import json
#import re
# import platformAPI as papi

# sdk = papi.create_ambra_sdk_api()
# sid = sdk.sid

#sid = '' 

"""
    
Ethan York 
September 14, 2022 at 10:06 AM

copy viewer3_config FROM a user (setting/get)
TO account
TO Role

TO another user


    Create the following custom fields in TS scripts
    user_uuid


"""


def custom_code(data):
        
        key = 'viewer3_config'

        environment = "access"
        url = "https://" + environment + ".ambrahealth.com/api/v3/"
        
        customfields = {i["name"]:i["value"] for i in data["study"]["customfields"]}
        
        api_call_data = {
            'sid': sid,
            'user_id': customfields["original_user_uuid"],
            'key': key
        }

        


        response = requests.post(url + "setting/get", data=api_call_data).json()
        response['value'] = response['value'].encode('raw_unicode_escape').decode('unicode_escape')

        pass
        
        #copy to role
        if customfields['role_uuid'] not in ["", None]:
            api_call_data['uuid'] = customfields['role_uuid']
            api_call_data["permission_viewer3_config"] = response["value"]
            role_response = requests.post(url + "role/set", data=api_call_data).json()
            
        
        #copy to account
        if customfields['account_uuid'] not in ["", None]:
            api_call_data['uuid'] = customfields['account_uuid']
            api_call_data["setting_viewer3_config"] = response["value"] 
            acct_response = requests.post(url + "account/set", data=api_call_data).json()

        if customfields['other_user_uuid'] not in ["", None]:
            api_call_data['user_id'] = customfields['other_user_uuid']
            api_call_data['value'] = response["value"]
            user_response = requests.post(url + 'setting/set', data=api_call_data)

        


#custom_code(data={"user_uuid":'94c5882d-76f5-484c-9615-6db2bf543684', 'role_uuid':'bbe9313d-884a-4cd8-b017-b25cfa8a08b6',
#'account_uuid':"7c94e43a-e890-409e-96ae-25df89b014b7", "other_user_uuid":"a74eefc2-59e4-41ed-baa6-8a15d07fc171"})