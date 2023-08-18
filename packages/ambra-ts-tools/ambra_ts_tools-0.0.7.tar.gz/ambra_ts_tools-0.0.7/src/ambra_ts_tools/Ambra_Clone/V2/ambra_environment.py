import json
import requests
from time import sleep
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
from functools import partial
import re


class ambra_environment:
    def __init__(self, sid:str,url="https://access.ambrahealth.com/api/v3"):
        """Authenticate ambra session to make api calls

        Args:
            sid (str): valid session id for cloning 
            url (str, optional): ambra api url. Defaults to "https://access.ambrahealth.com/api/v3".
        """
        self.sid = sid
        self.url = url
        self.log = []
        self.errors = []
        self.warnings = []
    def handle_ambra_request(self,endpoint:str,data:dict,throw=0,retry=0,last_error="",pg=1):
        """TODO: support pagation

        Args:
            endpoint (str): ambra api endpoint ex. /account/get
            data (dict): dictionary of parameters to pass to the endpoint
            throw (int, optional): flag to throw error. Defaults to 0.
            retry (int, optional): for recursion. Defaults to 0.
            last_error (str, optional): for recursion. Defaults to "".
            pg (int, optional): for recursion. Defaults to 1.

        Returns:
            dict: retuns the json response from the api if successful
        """
        
        if endpoint[0]!="/":
            endpoint = "/"+endpoint
        if isinstance(data,dict) and "sid" not in data:
            data["sid"] = self.sid
        # if retry>=3:
        #     if last_error not in self.errors:
        #         self.errors.append(last_error)
        #     if throw == 1:
        #         raise Exception(last_error)
        #     else:
        #         return
        try:
            response = requests.post(self.url+endpoint,data=data)
            if response.status_code == 401 and endpoint == '/account/get':
                raise Exception("sid error")
            res = response.json()
            if response.status_code == 200:
                
                if res['status'] == "OK" and "list" in endpoint and "more" in res.keys():
                    pg+=1
                    data['page'] = pg 
                    return res.append(self.handle_ambra_request(endpoint,data,pg=pg))
                elif res['status']=="OK":
                    return res
                else:
                    raise Exception(str(response.status_code)+" - " + endpoint +" - " + res.get('status')+" - " + res.get('error_type') + "-"+str(res.get('error_subtype'))+"-"+json.dumps(data))
            elif res['error_type'] in ["INVALID_SETTING","INVALID_PERMISSION","INVALID_SETTING_VALUE"] and endpoint in ['/account/set','/role/set']:
                if res['error_type'] == "INVALID_SETTING":
                    settings = json.loads(data['settings'][0])
                    del settings[res['error_subtype']]
                    data['settings'] =[json.dumps(settings)]
                    # req[i]['URL'] = re
                elif res['error_type'] == "INVALID_PERMISSION":
                    data['permissions'] = json.loads(data['permissions'])
                    del data['permissions'][res['error_subtype']]
                    data['permissions'] =json.dumps(data['permissions'])
                elif res['error_type'] == "INVALID_SETTING_VALUE":
                    settings = json.loads(data['settings'][0])
                    del settings[res['error_subtype'].split(":")[0]]
                    data['settings'] =[json.dumps(settings)]    
                self.warnings.append(res.get('error_type')+ "- "+endpoint+" Automatic error resolution attempted, "+res.get('error_subtype')+" was removed from "+data['uuid']+" "+endpoint)
                self.handle_ambra_request(endpoint,data, retry=retry+1,throw = throw)
            elif res['error_type'] == "INVALID_CUSTOMFIELD" or (res['error_type'] == "INVALID_FIELD_NAME" and 'customfield' in str(res['error_subtype'])):
                # return first group match for (?:.*)(customfield-(?:\w|\d|\-)+) if not null
                if 'user' in endpoint:
                    id = data['user_id']
                else:
                    id = data['uuid']
                field_to_remove = re.match("(?:.*)(customfield-(?:\w|\d|\-)+)",str(res['error_subtype'])).group(1)
                if field_to_remove in data:
                    del data[field_to_remove]
                    
                    self.warnings.append(res.get('error_type')+ "- "+endpoint+" Automatic error resolution attempted, "+str(res['error_subtype'])+" was removed from "+id+" "+endpoint)
                    self.handle_ambra_request(endpoint,data, retry=retry+1,throw = throw)
                elif 'defaults' in data: 
                    defaults = json.loads(data['defaults'])
                    if field_to_remove in defaults:
                        del defaults[field_to_remove]
                        data['defaults'] = json.dumps(defaults)
                        self.warnings.append(res.get('error_type')+ "- "+endpoint+" Automatic error resolution attempted, "+str(res['error_subtype'])+" was removed from "+id+" "+endpoint)
                        self.handle_ambra_request(endpoint,data, retry=retry+1,throw = throw)
                else:
                    raise Exception(str(response.status_code)+" - " + endpoint +" - " + res.get('status')+" - " + res.get('error_type') + "-"+str(res.get('error_subtype'))+"-"+json.dumps(data))
            else:
                raise Exception(str(response.status_code)+" - " + endpoint +" - " + response.text + " - "+json.dumps(data))
        except Exception as err:
            
            if 'sid error' in err.args:
                print("SID ERROR")
                raise Exception("SID ERROR")
            if retry >= 2 and err not in self.errors:
                self.errors.append(err)
                if throw == 1:
                    raise Exception(last_error)
                return 
            output = self.handle_ambra_request(endpoint,data, retry=retry+1,throw = throw,last_error=err)
            return output
        
    # method for multiprocessing handle_ambra_request with input parameters requestsm endpoint, and threads
    def multiprocess_ambra_request(self,requests,endpoint,threads=30):
        if len(requests) < threads:
            threads = len(requests)
            if threads == 0:
                return []
        func = partial(self.handle_ambra_request,endpoint)
        p = ThreadPool(threads) 
        threaded_response = p.map(func,requests)
        return threaded_response