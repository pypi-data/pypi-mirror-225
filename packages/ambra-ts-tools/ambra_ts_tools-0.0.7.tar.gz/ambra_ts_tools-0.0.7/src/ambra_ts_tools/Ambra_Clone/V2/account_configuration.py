from .ambra_environment import ambra_environment

import requests
from json import loads,dump,load,dumps
import os
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import Tk
from csv import DictWriter
import __main__ as main
from csv import DictWriter
if not hasattr(main, '__file__'):
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm

class account_configuration:
    def __init__(self, ambra_environment=None,account_id:str=None,name="",clone_items:list=[]):
        self.init_config = {
        "skip_fields": {
            "account": ["name","role_name","user_account_id","vanity","saml_redirect_url","md5"],
            "customfields":["customfield_mapping"],
            "route": ["namespace_name","actions:name","actions:destination"],
            "group": ["anonymize_at_ingress","namespace_id"],
            "location":["anonymize_at_ingress","namespace_id"],
            "dictionary":["attachments:uuid"],
            "role":["permissions:viewer3_config"],
            "terminology":["vanity"],
            "account/user":["user_account_id"],
            "namespace/settings":["linked_namespace_name","location_id","group_id","status"],
            "namespace/anonymize":["dicom_tag_map"],
            "webhook":["last_error"]
            },
            "special_fields":{},
            "error_dict": {
                "DUP_SHARE_CODE":"share_code",
                "INVALID_OTHER_NAMESPACES": "other_namespaces"
                }, 
            "special_uuid": {},
            "skip_uuid": [],
            "id_map" : {},
            "never_skip_fields":["filter_field"],
            "available_api_strs": [
                    "account",
                    "customfield",
                    "customfield/mapping",
                    "role",
                    "group",
                    "location",
                    "account/user",
                    "webhook",
                    "route",
                    "group/user",
                    "location/user",
                    "namespace/settings",
                    "namespace/anonymize",
                    "namespace/study/defaults",
                    "namespace/event/defaults",
                    "terminology",
                    "hl7/template",
                    "hl7/transform",
                    "dictionary",
                    "mail/template",
                    "radreport/template",
                    "account/can/share",
                    "site",
                    "destination",
                    "node"],
            "list_api_strs": {"customfield":"customfields",
                "role":"roles",
                "group":"groups",
                "location":"locations",
                "webhook":"webhooks",
                "route":"routes",
                "hl7/template":"templates",
                "hl7/transform":"transforms",
                "dictionary":"dictionaries",
                "site":"sites",
                "radreport/template":"templates",
                "mail/template":"templates",
                "account/user":"users",
                "group/user":"users",
                "location/user":"users",
                "terminology":"tags",
                "account/can/share":"rules",
                "destination":"destinations",
                "node":"nodes"},
            "required_add_fields": {
                "customfield":["object","type"],
                "customfield/mapping":["from_customfield_id",'to_customfield_id'],
                "role":[],
                "group":[],
                "location":[],
                "account/user":["email","role_id"],
                "webhook":["url","method","event","cron"],
                "route":["conditions","actions","namespace_id"],
                "group/user":["user_id","role_id"],
                "location/user":["user_id","role_id"],
                "hl7/template":["body"],
                "hl7/transform":["conditions","replacements","order_by"],
                "dictionary":["object","lookup","replace","case_sensitive"],
                "mail/template":["type"],
                "radreport/template":["type","body"],
                "site":[],
                "destination":["node_id","aetitle","address","port"],
                "node":["type"]},
                "cast_as_string":["rules","conditions","dicom_tag_map"]
                }
        for config in self.init_config:
            setattr(self,config,self.init_config[config])
        self.config_dirname = os.path.dirname(__file__)
        filename = os.path.join(self.config_dirname, "init_config.json")
        self.namespace_properies_by_id = {}
        
        if ambra_environment==None: 
            self.load_from_file()
        else:
            self.account = {}
            self.env = ambra_environment
            if account_id in ["",None] and name != '': 
                try:
                    account_response = self.env.handle_ambra_request("/account/add",data={'sid':self.env.sid,"name":name},throw=1)
                    self.account = account_response
                    self.account_id = account_response['uuid']
                    self.account['name'] = name
                except Exception as err:
                    raise Exception("failed adding account " + name + " - " + str(err))
            else:
                self.account_id=account_id
                self.account = self.env.handle_ambra_request("account/get",data={"uuid":account_id},throw=1)
            self.permissions = self.env.handle_ambra_request("/session/permissions",data={"sid":self.env.sid,"account_id":account_id})
            self.reload_account_configuration(clone_items)
        
        
    def reload_account_configuration(self,api_strs:list=None):
        print("Loading account configuration for "+self.account.get("name")+" - uuid: "+self.account.get("uuid"))
        #api calls that have a /list endpoint
        # if api_strs in [None,"all",['all']] :
        api_strs = self.available_api_strs
        # else:
        #     api_strs = api_strs
        pbar = tqdm(api_strs,total=len(api_strs))
        for apistr in pbar:
            if apistr == "account":
                try:
                    setattr(self,"account",self.env.handle_ambra_request("/account/get",data={"sid":self.env.sid,"uuid":self.account_id},throw=1))   
                except:
                    raise Exception("Unable to get account information for "+self.account_id+ " please ensure session information is correct \n URL:"+self.env.url+"\n SID:"+self.env.sid)
            else:
                try:
                    pbar.set_description("loading "+apistr)
                    if apistr in self.list_api_strs.keys() and 'user' not in apistr:
                        data = {"sid":self.env.sid,"account_id":self.account_id}
                        tmpstr = self.list_api_strs[apistr]
                        response = self.env.handle_ambra_request("/{apistr}/list".format(url=self.env.url,apistr=apistr),data=data)
                        if response is None:
                            setattr(self,apistr,[])
                        else:
                            if apistr == "customfield":
                                setattr(self,"customfield/mapping",[])
                                for cf in response['customfields']:
                                    setattr(self,"customfield/mapping",getattr(self,"customfield/mapping")+cf['customfield_mapping'])
                            setattr(self,apistr,response[tmpstr])
                    
                    elif apistr == "account/user":
                        # try:
                            out = self.env.handle_ambra_request(apistr+"/list",data={"uuid":self.account_id})
                            out = out.get('users')
                            for user in out: 
                                user['linked_namespace_name'] = self.account.get('name')
                                user['namespace_id'] = self.account.get('namespace_id')
                                user['account_id'] = self.account.get('uuid')
                            setattr(self,apistr,out)
                        # except:
                        #     print("skipping account/user")
                            
                    elif 'namespace' in apistr or apistr in ["group/user","location/user"]:
                        threaded_requests = []
                        if apistr in ["group/user","location/user"]:
                            endpnt = apistr+"/list"
                            field = "uuid"
                            out = {}
                            namespaces = []
                            for x in getattr(self,apistr.split("/")[0]):
                                threaded_requests.append({"uuid":x[field],"sid":self.env.sid})
                                namespaces.append(x)
                            threaded_response = self.env.multiprocess_ambra_request(threaded_requests,endpnt)
                        elif 'namespace' in apistr:
                            endpnt = apistr
                            field = "namespace_id"
                            out = []
                            namespaces = [self.account]+self.group+self.location
                            for ns in namespaces:
                                threaded_requests.append({"uuid":ns['namespace_id'],"sid":self.env.sid})
                            threaded_response = self.env.multiprocess_ambra_request(threaded_requests,endpnt)
                            
                        for i in range(len(threaded_response)):
                            res = threaded_response[i]
                            x = namespaces[i]
                            if 'user' in apistr:
                                out[x[field]] = res['users']
                                for user in out[x[field]]:
                                    user['linked_namespace_name'] = x['name']
                                    user['uuid'] = x['uuid']
                            elif 'namespace' in apistr:
                                
                                if 'rules' in res:
                                    rules = loads(res['rules'])  
                                    for key in list(rules): # this loop gets rid of the other_ingress_tags all other_ingress_tags from account settings are listed but cannot be set in namespace/anonymize. Expecting OTHER_INGRESS_TAGS : ANONYMIZATION VALUE instead
                                        if '(' in key  and ',' in key:
                                            # rules['OTHER_INGRESS_TAGS'] = rules[key]
                                            del rules[key]
                                    if len(rules) > 0:
                                        res['rules'] = dumps(rules)
                                    else:
                                        del res['rules']
                                res['linked_namespace_name'] = x['name']
                                res['uuid'] =x['namespace_id']
                                res['location_id'] = x['uuid']
                                out.append(res)
                        setattr(self,apistr,out)
                except:
                    print("skipping "+apistr)
        self.reload_namespace_properties()
    def reload_namespace_properties(self):
        self.namespace_properies_by_id[self.account['namespace_id']] = {"account_id":self.account['uuid'],"name":self.account['name']}
        for g in self.group:    
            self.namespace_properies_by_id[g['namespace_id']] = {"group_id":g['uuid'],"name":g['name']}
        for l in self.location:
            self.namespace_properies_by_id[l['namespace_id']] = {"location_id":l['uuid'],"name":l['name']}
        for anon in getattr(self,"namespace/anonymize"):
            self.namespace_properies_by_id[anon['uuid']].update({"namespace/anonymize":anon})
        for default in getattr(self,"namespace/settings"):
            self.namespace_properies_by_id[default['uuid']].update({"namespace/settings":default})
    def get_account_json(self):
        return {d: self.dict_sort(self.__dict__.get(d)) for d in self.__dict__ if d in self.available_api_strs}
    def generate_account_file(self,account_file=None):
        if account_file == None:
            root = Tk()
            
            account_file = asksaveasfilename(defaultextension='.json',initialfile=self.account['name']+".json")
            root.destroy()
        dump(self.get_account_json(),open(account_file,'w',newline=""),indent=4)
    def dict_sort(self,data):
        #data can be a list or a dictionary. Return a sorted version of the data
        #sort all sub dictionaries and lists
        #sort list of dictionaries by the dictionary 'name' or 'user_name' key
        if type(data) == list:
            for i in range(len(data)):
                data[i] = self.dict_sort(data[i])
            if len(data) > 0 and type(data[0]) == dict:
                if 'name' in data[0]:
                    return sorted(data,key=lambda x: x['name'])
                elif 'user_name' in data[0]:
                    return sorted(data,key=lambda x: x['user_name'])
                elif 'linked_namespace_name' in data[0]:
                    return sorted(data,key=lambda x: x['linked_namespace_name'])
                else:
                    return sorted(data,key=lambda x: x[sorted(list(x.keys()))[0]])
            else:
                return data
        elif type(data) == dict:
            for key in data:
                data[key] = self.dict_sort(data[key])
            return dict(sorted(data.items()))
        else:
            return data
            
        
    def load_from_file(self):
        root = Tk()
        account_file = askopenfilename(title="Select account configuration json file",filetypes=[("accont_configuration",".json")])
        root.destroy()
        config = load(open(account_file,'r'))
        for k,v in config.items(): 
            setattr(self,k,v)
        self.reload_namespace_properties()
    # clone_items= [
    # "customfield",
    # "role",
    # "group",
    # "location",
    # "account/users",
    # "webhook",
    # "route",
    # "group_location_users",
    # "namespace_settings",
    # "terminology",
    # "hl7/template",
    # "hl7/transform",
    # "dictionary",
    # "mail_templates",
    # "account_settings",
    # "radreport/template",
    # "share_settings",
    # "site",
    # "destinations",
    # "nodes"]
### FOR TESTING
# calyx_uat = ambra_environment("785e516b-0861-4d5b-88ab-f5510e76538a",url = "https://mi.uat.calyx.ai/api/v3")
# act_config = account_configuration(calyx_uat,"d9084e43-6c35-4dc5-a852-caea6e618623")
# ambra_uat = ambra_environment("da891b40-3d34-49b0-ad7a-c76ef8b4b8c7",url = "https://uat.ambrahealth.com/api/v3")
# act_config = account_configuration(ambra_uat,"57ef3334-f629-4422-9406-e2bf3a8441fc")
# act_config.generate_account_file()


# local_load = account_configuration()