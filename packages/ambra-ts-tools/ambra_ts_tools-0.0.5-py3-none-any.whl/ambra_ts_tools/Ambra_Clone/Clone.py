from os import name, remove
from ambra_sdk.service.entrypoints import account
import requests as requests
import json
from ambra_sdk.api import Api
import ast
import re
from time import sleep
from csv import DictWriter
class Clone:
    def __init__(self, sid, original_url, original_account_uuid,clone_items="all",copy_url_base=None,copy_account_uuid=None,sid_copy=None,account_name=""):
        """initialize cloning objecy
        Args:
            sid (str): session id for original_url
            original_url (str): the original url with "api/v3" included. ie. https://access.ambrahealth.com/api/v3
            original_account_uuid (str): original account uuid
            clone_items (str/list, optional): list of items to clone. Defaults to "all".
            copy_url_base (str, optional): [description]. Defaults to None.
            copy_account_uuid (str, optional): If unspecified a new account will be created. The uuid of the duplicate account if it already exists. Defaults to None.
            sid_copy (str, optional): If unspecified, same as original session id. The session id for the duplicate account. Defaults to None.
            account_name (str,optional): Account Name. If unspecified or "", Account name will be be "Copy of <original account Name>"
        """
        # handle user input parameters
        self.sid = sid
        self.original_url = original_url
        self.sdk = Api.with_sid(original_url,self.sid)
        self.original_account_uuid = original_account_uuid
        self.clone_items = clone_items
        self.copy_url_base = copy_url_base
        self.copy_account_uuid = copy_account_uuid
        self.sid_copy = sid_copy
        if self.sid_copy in ["",None]:
            self.sid_copy=self.sid
            self.copy_url_base = original_url
            self.sdk_copy=self.sdk
        else:
            self.sdk_copy = Api.with_sid(self.copy_url_base,self.sid_copy)
        self.special_fields = {} #ui json should not be null or things do not display correctly in the ui
        self.skip_fields = {
        "account": ['name','role_name','user_account_id','vanity','saml_redirect_url','md5','role_name'],
        "route": ['namespace_name','actions:name','actions:destination'],
        "group": ["anonymize_at_ingress","namespace_id"], # set in namespace settings
        "location":["anonymize_at_ingress","namespace_id"],
        "dictionary":["attachments:uuid"],
        "role":[],
        "terminology":["vanity"],
        "node":["configuration:os_version","last_ping"],
        "account/user":["user_account_id"],
        "site":["trials"]
        }
        self.error_dict = {
            "DUP_SHARE_CODE":"share_code",
            "INVALID_OTHER_NAMESPACES": "other_namespaces",
            "SID_USER_NOT_IN_ACCOUNT":"sid_user_id",
            "NOT_FOUND:OTHER_CUSTOMFIELD":"other_customfield_id"
            }
        self.special_uuid = {}
        self.skip_uuid = []
        self.url = original_url+'/bundle'
        self.copy_bundle_url = self.copy_url_base+'/bundle'
        self.uuid_map ={} # uuid_original : uuid_copy
        self.namespace_map = {}
        self.namespace_group_uuid_map ={}
        self.namespace_location_uuid_map={}
        self.errors = []
        self.uuid_pattern= re.compile('((?:(?:\d|\w){8}-)(?:(?:\d|\w){4}-){3}(?:(?:\d|\w){12}))')
        self.api_calls = []
        self.missing_users =set()

        if self.clone_items  in [[],"all",None,""] or "all" in self.clone_items:
            self.clone_items = ["customfield","role","group","location","account/user","webhook","route","group_location_users","namespace_settings","terminology","hl7/template","hl7/transform","dictionary","mail_templates","account_settings","radreport/template","share_settings","site","destinations","nodes"]
        try:
            self.o_account = self.sdk.Account.get(uuid = self.original_account_uuid).get()
        except Exception as err:
            raise Exception("An error occured getting the account information. Please verify sid, url, and account uuid")
        if self.copy_account_uuid in ["",None]:
            if account_name in ["",None]:
                account_name = "copy of "+self.o_account['name']
            try:

                res = requests.post(self.copy_url_base+"/account/add", data = {
                    "sid":self.sdk_copy.sid,
                    "name": account_name
                })
                self.add_api_call("POST",self.copy_url_base+"/account/add",{
                    "sid":self.sdk_copy.sid,
                    "name": account_name
                })
                res = res.json()
                self.copy_account_uuid = res['uuid']
            except Exception as E:
                raise Exception("Account Name in use- please get uuid of existing account and plug it into the 'copy_account_uuid' Optional field")
            #Map Account UUIDs
        self.uuid_map[self.original_account_uuid] = self.copy_account_uuid
        # o_users = self.sdk.Account.user_list(self.original_account_uuid).get()['users']
        # c_users = self.sdk_copy.Account.user_list(self.copy_account_uuid).get()['users']
        # self._map_existing_records(c_users,o_users,'user',map_by='user_email',uuidMap="user_id")
        # add_users_to_instance(o_users,self.copy_account_uuid,self.copy_url_base)
        # Map Account namespaces
        try:
            self.c_account = self.sdk_copy.Account.get(self.copy_account_uuid).get()
        except Exception as E:
            raise Exception("An error occured getting copy account information. Please try again.")

        self.uuid_map[self.o_account['namespace_id']]=self.c_account['namespace_id']
        print("new account uuid: "+self.copy_account_uuid)
    def overwrite_user_role(self,original_role_name):
        c_roles = self.sdk_copy.Role.list(account_id=self.copy_account_uuid).get()['roles']
        o_roles = self.sdk.Role.list(account_id=self.original_account_uuid).get()['roles']

        c_user_role = [r['uuid'] for r in c_roles if r['name']=="User"][0]
        o_user_role = [r['uuid'] for r in o_roles if r['name']==original_role_name][0]
        self.update_uuid_map({o_user_role:c_user_role})
    def add_api_call(self,method,url,data):
        self.api_calls.append({"Method":method,"URL":url,"Data":data})
        #api_audit_log = open("api_audit_log"+self.copy_account_uuid+".txt","w+",encoding="utf-8")
    def add_special_field(self,field_key,apistr,value,lookup_and_replace=None, lookup_value=""):
        """Instead of copying the value for the specified field and apistr. Default a preset value. For example if you wanted to suspend all webhooks in the newly cloned account - apistr='webhook',field_key='suspended',value=1

        Args:
            field_key (str): field key for specified value. Use : to separate fields in a seeded json.
            apistr (str): api endpoint string ie. webhook, route, customfield, ect.
            value (any): value to default for the api endpoint value
        """
        if lookup_and_replace != 1:
            self.special_fields[apistr+":"+field_key]=value
        else:
            if apistr+":"+field_key in self.special_fields:
                self.special_fields[apistr+":"+field_key] = self.special_fields[apistr+":"+field_key]+"|"+"REPLACE^"+lookup_value+"^"+value
            else:   
                self.special_fields[apistr+":"+field_key]="REPLACE^"+lookup_value+"^"+value
    def _delete_special_field(self,field_key,apistr):
        del self.special_fields[apistr+":"+field_key]
    def add_special_uuid(self,uuid,field_key,value):
        """For a specific uuid. Instead of copying the original field data use the specified value

        Args:
            uuid (str): uuid of the original item with a special field
            field_key (str): field key for the special value. separate seeded json fields by a :
            value (any): value of the uuid field.
        """
        if uuid in self.special_uuid:
            self.special_uuid[uuid][field_key] = value
        else:
            self.special_uuid[uuid] = {field_key:value}
    #def clone_specific_uuid():

    def update_uuid_map(self,dict):
        """Ambra items are generally mapped to their new uuid by the name of the record. However you can manually map records with this parameter instead.

        Args:
            dict (dictionary): map of uuids {original_uuid : new_uuid}
        """
        self.uuid_map.update(dict)
    def copy_field(self,original,copy=None,field_key='',apistr="",original_object={}):
        """copy the original field based on it's data type. Identical fields will be skipped.

        Args:
            original (any): original field to copy
            copy (any, optional): copy field if exists. Defaults to None.
            field_key (any, optional): = The field key for special exceptions. Defaults to None.
            apistr (string, optional): api string to tell what type of object is being copied. Defaults to None.
            original_object (dict, optional): the original object to print out more useful infomration during error handling
        Returns:
            [any]: copy of the original with updated uuids ect.
        """

        output = None
        ### Validation
        conditions = [original == copy or str(original)== str(copy) or (original in ['',None] and copy in [None,'']), 
        apistr+":"+field_key not in self.special_fields,
        len(field_key.split(':'))<2,
        field_key!="name"]
        if all(conditions): #skip the json field if the copy and original are the same.
            pass

        elif apistr in self.skip_fields.keys() and field_key in self.skip_fields[apistr] and apistr+":"+field_key not in self.special_fields.keys():
            pass
        elif apistr+":"+field_key in self.special_fields.keys():
            if "REPLACE" not in self.special_fields.get(apistr+":"+field_key):
                output = self.special_fields.get(apistr+":"+field_key)
            else:
                output = original
                for r in self.special_fields.get(apistr+":"+field_key).split("|"):
                    replace_arraya = r.split("^")
                    output = output.replace(replace_array[1],replace_array[2])
        elif isinstance(original,dict):
            if 'uuid' in original and original['uuid'] in self.skip_uuid:
                pass
            if field_key in ['parameters','settings'] and apistr not in ["radreport/template"]:
                value = self._parse_dictionary_field(original,copy,field_key=field_key,return_type='list',apistr=apistr,original_object=original_object)
            elif field_key in ['share_settings','settings:viewer3_config','options','linked_study_accounts','settings:upload_settings','settings:ui_json',"settings:study_status_tags_attributes","permissions:ui_json","permissions","study_field_flags","permissions:viewer_config","permissions:viewer3_config"] or (apistr =='node' and 'configuration' in field_key):
                value = self._parse_dictionary_field(original,copy,field_key=field_key,return_type='json',apistr=apistr,original_object=original_object)
            else:
                value = self._parse_dictionary_field(original,copy,field_key=field_key,apistr=apistr,original_object=original_object)
            if value not in [None,{},"{}"]:
                output = value
        elif isinstance(original,int) or isinstance(original,float):

            if original == 0 and copy is None and apistr not in ['dictionary','group','location','radreport/template','site_qualified'] and len(field_key.split(':'))<2 :
                pass
            elif (apistr == "radreport/template" and field_key=="active"):
                output = str(original)
            else:
                output = original
        elif isinstance(original,str):
            if original == copy and len(field_key.split(':'))<2:
                if field_key in ['lv','op','rv','search_source','order_by']:
                    output = original
                else:
                    pass
            # elif field_key == '' and len(original.split("-"))<5:
            #     output = original
            else:
                value = self._parse_string_field(original,copy,field_key,apistr=apistr,original_object=original_object)
                if value is not None:
                    output = value
        elif isinstance(original,list):
            if original == [] and copy is None:
                pass
            else:
                output = []
                for item in original:
                    ind = original.index(item)
                    if copy is not None and ind <= len(copy)-1:
                        value = self.copy_field(item,copy=copy[ind],field_key=field_key,apistr=apistr,original_object=original_object)
                    else:
                        value = self.copy_field(item,field_key=field_key,apistr=apistr,original_object=original_object)
                    if value is not None:
                        output.append(value)
                if apistr in ['route','hl7/transform','role'] and field_key in ['actions','conditions','replacements']:
                    if output != []:
                        output = json.dumps(output)
                    else:
                        output = None
        elif original is None:
            output = None
        else:
            print("COPY_FIELD TYPE ERROR DOUBLECHECK ",original)
        if 'output' in locals() and output is not None:
            if field_key== "settings:study_status_tags_attributes":
                print("PAUSE")
            return output
    def _parse_string_field(self,original,copy,key,apistr="",original_object = {}):
        """copy a field of data type string

        Args:
            original (string): original string
            copy (string): string in copy account- if exists
            key (str): field name (for exceptions)
            apistr (string, optional): String to represent the ambra api calls associated with object. Defaults to None.

        Returns:
            (string): copy of original string
        """
        if original == "f83df896-29ce-4c0f-952b-54faf5d5a365":
            print("PAUSE")
        original_uuids = re.findall(self.uuid_pattern,original)
        if original==copy and len(original_uuids)==0 and len(key.split(":"))<2: # skip if original same as copy
            pass
        elif original in ['','{}','[]',""]:
            if copy is not None and copy in ['','{}','[]',""]:
                    pass
            else:
                if key == 'ui_json':
                    output = json.dumps({})
                else:
                    output = original
        elif original[0]=='{' and original[-1]=="}": #If json string. convert to json object- rerun copy_field function.
            if copy is not None and copy not in ['{}',''] and copy[0]=="{" and copy[-1]=="}" and copy[1]!="{" and apistr not in ['hl7/transform']:
                value= self.copy_field(json.loads(original),json.loads(copy),field_key=key,apistr=apistr,original_object=original_object)
            elif len(original.split(":"))==1: #Not true json object.
                value = original
            else:
                value= self.copy_field(json.loads(original),field_key=key,apistr=apistr,original_object=original_object)
        
            output = value
            if key=='ui_json' and output != None:
                output = json.dumps(value)
        elif len(original_uuids)>0:
            output = original
            for uuid in original_uuids:
                if uuid in self.uuid_map:
                    output = output.replace(uuid,self.uuid_map[uuid])
                else:
                    if 'name' in original_object.keys():
                        name = original_object['name']
                    else:
                        name= ''
                    self.errors.append("uuid match not found for {apistr}, Item:{key}, Name:{name}, uuid:{uuid}".format(apistr=apistr.upper(),key=key,uuid=uuid,name=name))
                    # if 'output' in locals():
                    #     del output
        elif original!='' and original[0]=="[" and key not in ['share_settings:setTextElements:selector','settings:study_status_tags_attributes','settings:study_status_tags_attributes:study-listLoaded:all:selector',"settings:passwd_regexp",'options:hint']:
                original = ast.literal_eval(original)
                output = self.copy_field(original,copy,field_key=key,apistr=apistr,original_object=original_object)
                if len(output)>0:
                    output= json.dumps(output)
        elif original == "0" and (copy is None or copy =='[]'):
            pass
        elif original is None:
            output = ''
        else:
            output= original
        if 'output' in locals() and output is not None and (output != copy or 'study_status_tags' in key):
            return output
    def _parse_dictionary_field(self,original,copy,field_key,return_type=None,apistr="",original_object={}):
        value = None
        if original=={}:
            if copy!= None:
                output={}
        else:
            output = {}
            if isinstance(copy,str):
                if copy[0]=="{" and copy[-1]=="}":
                    copy = json.loads(copy)
                else:
                    copy = None
            for field in original.keys():

                field_uuids = re.findall(self.uuid_pattern,field)

                # if field =='ui_json' and original[field] == '':
                #     if copy is not None and copy[field]!='':
                #         value = json.dumps({})
                if copy is not None and field in copy.keys():
                    value = self.copy_field(original[field],copy[field],field_key=str(field_key)+":"+field,apistr=apistr,original_object=original_object)
                else:
                    value = self.copy_field(original[field],field_key=str(field_key)+":"+field,apistr=apistr,original_object=original_object)
                if len(field_uuids)>0:
                    for uuid in field_uuids:
                        if uuid in self.uuid_map:
                            field=field.replace(uuid,self.uuid_map[uuid])
                        else:
                            self.errors.append("uuid match not found for {apistr} {uuid}".format(apistr=apistr,uuid=uuid))
                    output[field]=value
                elif value is not None:
                    output[field]=value
        if 'output' not in locals():
            return
        elif output == {}:
            return
        elif return_type == 'json':
            return json.dumps(output)
        elif return_type =='list':
            return [json.dumps(output)]
        else:
            return output
    def _handle_res(self,res,req,apistr,url,original):

        if not isinstance(res,list):
            res = [res]
        if not isinstance(original,list):
            original = [original]
            req = [req]
        i = 0
        retry = []
        for r in res:
            if r['status'] == 'OK':
                if 'add' in url:
                    if "uuid" in r and 'uuid' in original[i]:
                        self.uuid_map[original[i]['uuid']] = r['uuid']
                    elif "uuid" in r and 'user_id' in original[i]:
                        self.uuid_map[original[i]['user_id']] = r['uuid']
                    if 'namespace_id' in r.keys() and apistr !='route': #map namespace ids
                        self.namespace_map[original[i]['namespace_id']] = r['namespace_id']
                        self.uuid_map[original[i]['namespace_id']] = r['namespace_id']
            else:

                if r.get('error_type') in self.error_dict or r.get('error_type')+":"+str(r.get('error_subtype')) in self.error_dict:
                    try:
                        remove_field = self.error_dict[r.get('error_type')]
                    except:
                        remove_field = self.error_dict[r.get('error_type')+":"+str(r.get('error_subtype'))]
                    del req[i][remove_field]
                    retry.append(req[i])
                    self.errors.append("Automatic error resolution attempted, "+remove_field+" was removed from the copy of "+apistr+ " "+original[i]['name'])
                # elif r.get('error_type') == "NOT_FOUND":
                #     if isinstance(r.get('error_subtype'),list):
                #         for f in r.get('error_subtype'):
                #             del req[i][f]
                #             retry.append(req[i])
                #             self.errors.append("Automatic error resolution attempted, "+remove_field+" was removed from the copy of "+apistr+ " "+original[i]['name'])
                #     retry.append(req[i])
                #     self.errors.append("Automatic error resolution attempted, "+remove_field+" was removed from the copy of "+apistr+ " "+original[i]['name'])
                elif r['error_type'] in ["INVALID_SETTING","INVALID_PERMISSION","INVALID_SETTING_VALUE"] and apistr in ['account_settings','role']:
                        if r['error_type'] == "INVALID_SETTING":
                            settings = json.loads(req[i]['settings'][0])
                            del settings[r['error_subtype']]
                            req[i]['settings'] =[json.dumps(settings)]
                            # req[i]['URL'] = re
                        elif r['error_type'] == "INVALID_PERMISSION":
                            req[i]['permissions'] = json.loads(req[i]['permissions'])
                            del req[i]['permissions'][r['error_subtype']]
                            req[i]['permissions'] =json.dumps(req[i]['permissions'])
                        elif r['error_type'] == "INVALID_SETTING_VALUE":
                            settings = json.loads(req[i]['settings'][0])
                            del settings[r['error_subtype'].split(":")[0]]
                            req[i]['settings'] =[json.dumps(settings)]
                            
                        retry.append(req[i])
                        self.errors.append(r.get('error_type')+ "- "+apistr+" Automatic error resolution attempted, "+r.get('error_subtype')+" was removed from the copy of "+apistr+ " "+original[i]['name'])
                elif r.get('error_type') == "ALREADY_EXISTS":
                    pass
                elif r.get('error_type') == "USER_NOT_FOUND":
                    self.missing_users.add(req[i]['email'])
                else:
                    if apistr not in ['group/user','location/user','dictionary/entry/add','/account/can/share'] and original is not None:
                        if 'name' in req[i]:
                            name = req[i]['name']
                        elif 'site_name' in req[i]:
                            name = req[i]['site_name']
                        else:
                            name = ''
                        message = " {error_type}, {apistr} - {name}".format(error_type=r.get('error_type'),apistr=apistr,name= name)
                        print(message)
                        self.errors.append(message)

            i+=1
        if len(retry)>0:
            if url == self.copy_bundle_url:
                res = requests.post(url,data=json.dumps(retry))
                self.add_api_call("POST",url,json.dumps(retry))
            else:
                data = retry[0]
                res = requests.post(url,data=data)
                self.add_api_call("POST",url,retry[0])
            res = res.json()
            self._handle_res(res,retry,apistr,url,original)
    def _map_existing_records(self,copy,original,apistr,uuidMap='uuid',map_by='name',return_map=False): #assumes and updates and uuid_map
        """map records in the original account to records that exist in the copy account.

        Args:
            copy (list): List of json objects returned from an ambra 'list' call
            original (list): List of json objects returned from an ambra 'list' call
            apistr (str): string that cooresponds to the ambra api object
            uuidMap (str, optional): The field in the copy/original json objects to map inside of the uuid_map global variable (only exists because user/list returns the user uuid as user_id). Defaults to 'uuid'.
            map_by (str, optional): The json field that allows you to identify if an object already exists in the copy account. Defaults to 'name'.
            return_map (bool, optional): Boolean to determine if the function will return a dictionary where {"original account object uuid": "copy account object uuid"}. Defaults to False.

        Returns:
            Dict: a dictionary where {"original account object uuid": "copy account object uuid"} for each object that there is a match
        """
        map = {}
        for c in copy:
            for o in original:
                if c[map_by] == o[map_by] or "MISSING INFORMATION: "+ o[map_by]==c[map_by] or "Missing Actions- "+ o[map_by]==c[map_by]:
                    self.uuid_map[o[uuidMap]]=c[uuidMap]
                    if return_map==True:
                        map[o[uuidMap]]=c[uuidMap]
                    if 'namespace_id' in o.keys() and apistr !='route': #map namespace ids
                        self.uuid_map[o['namespace_id']] = c['namespace_id']
                        self.namespace_map[o['namespace_id']] = c['namespace_id']
                        # if apistr == 'group':
                        #     self.namespace_group_uuid_map[o['namespace_id']] = c['uuid']
                        # elif apistr == 'location':
                        #     self.namespace_location_uuid_map[o['namespace_id']] = c['uuid']

        if map != {}:
            return map
    def _add_new_records(self,original,apistr,info_req_for_add=None,id='uuid',act_id="account_id",name=True,namespace_users={}):
        """[summary]

        Args:
            original (list): list of original json objects from ambra 'list' call
            self.copy_account_uuid (string): uuid of the copy account
            apistr (string): string that cooresponds to the ambra api object
            info_req_for_add (list, optional): bare miniumum list of fields that are required to add an object, the object is updated to match later. Defaults to None.
            id (str, optional): field cooresponding to the uuid of the object. Defaults to 'uuid'.
            act_id (str, optional): field cooresponding to the account uuid. Defaults to "account_id".
            name (bool, optional): is "name" a field on the object. Defaults to True.
            namespace_users (dict, optional): dictionary mapping namespace uuids between Users in the original account to the copy account . Defaults to {}.
        """
        add_req = []
        reqs = []
        for o in original:
            if (o[id] not in self.uuid_map.keys() or (apistr in ['group/user','location/user'] and namespace_users != None and o[id] not in namespace_users.keys())) and o[id] not in self.skip_uuid:
                req = {"URL":"/"+apistr+"/add","sid":self.sid_copy}
                if apistr != "route":
                    req[act_id] = self.copy_account_uuid
                if name:
                    if o[id] in self.special_uuid.keys() and 'name' in self.special_uuid[o[id]]:
                        req["name"] = self.special_uuid[o[id]]['name']
                    else:
                        req['name'] = o['name']
                if apistr =='customfield' and o['type']=='search':
                    info_req_for_add.append('options')
                if info_req_for_add is not None:
                    for info in info_req_for_add:
                        if o[id] in self.special_uuid.keys() and info in self.special_uuid[o[id]]:
                            req[info] = self.special_uuid[o[id]][info]
                        # if apistr=='route' and info=='namespace_id':
                        #     if o[info] in self.namespace_group_uuid_map.keys():
                        #         req['group_id']= self.namespace_group_uuid_map[o[info]]
                        #     elif o[info] in self.namespace_location_uuid_map.keys():
                        #         req['location_id'] = self.namespace_location_uuid_map[o[info]]
                        #     elif o[info] in self.uuid_map:
                        #         req['namespace_id'] = self.uuid_map[o[info]]
                        #     else:
                        #         req[act_id]=self.copy_account_uuid
                        elif info =="email" and apistr in ["account/user",'group/user','location/user']:
                            req[info] = o["user_email"]
                        else:

                            value = self.copy_field(o.get(info),copy=None,field_key=info,apistr=apistr,original_object=o)
                            if value is not None:
                                req[info] = value
                            elif info in ['actions','conditions','replacements']:
                                req[info]=json.dumps([])
                if apistr=='route':
                    if len(json.loads(req['actions']))>0 and "MISSING INFORMATION" in json.loads(req['actions'])[0].values():
                        req['actions'] = '[]'
                        req['name'] = "Missing Actions- "+ req['name']
                #api_audit_log.write("\n"+str(req))
                reqs.append(req)
        if len(reqs)>0:
            res = requests.post(self.copy_bundle_url,data =json.dumps(reqs))
            self.add_api_call("POST",self.copy_bundle_url,json.dumps(reqs))
            res = res.json()
            self._handle_res(res,reqs,apistr,self.copy_bundle_url,original)
    def _update_records_to_match(self,original,apistr):
        """update records in the copy account to match records in the original account

        Args:
            original (list): list of oringal records that will serve as the master copy updating their mappings in the uuid_map variable.
            apistr (string): apistr (string): string that cooresponds to the ambra api object
        """
        reqs =[]
        for o in original:
            ldict = {}
            if o['uuid'] in self.uuid_map:
                res = requests.post(self.copy_url_base+"/"+apistr+"/get",data={"uuid":self.uuid_map[o['uuid']],"sid":self.sid_copy})
                self.add_api_call("POST",self.copy_url_base+"/"+apistr+"/get",{"uuid":self.uuid_map[o['uuid']],"sid":self.sid_copy})
                c = res.json()
                req = {'URL':'/'+apistr+'/set','sid':self.sid_copy, 'uuid':self.uuid_map[o['uuid']]}
                if o['uuid'] in self.special_uuid.keys():
                        for field_key in self.special_uuid[o['uuid']]:
                            self.add_special_field(field_key=field_key,apistr=apistr,value=self.special_uuid[o['uuid']][field_key])
                for field in o.keys():
                    field_uuids = re.findall(self.uuid_pattern,field)

                    if field == 'uuid':
                        pass
                    elif len(field_uuids)>0:
                        for uuid in field_uuids:
                            if uuid in self.uuid_map:
                                field = field.replace(uuid,self.uuid_map[uuid])
                            else:
                                self.errors.append('uuid not found - ',uuid,' ',apistr)
                    elif c is not None and c !=[] and field in c.keys():
                        value = self.copy_field(o[field],copy=c[field],field_key=field,apistr=apistr,original_object=o)
                    else:
                        value = self.copy_field(o[field],copy=None,field_key=field,apistr=apistr,original_object=o)
                    if 'value' in locals() and value is not None:
                        req[field] = value
                        del value
                if apistr=='route' and 'actions' in req.keys() and "MISSING INFORMATION" in str(req['actions']):
                        del req['actions']
                        if c['name'] != "Missing Actions- "+ o['name']:
                            req['name'] = "Missing Actions- "+ o['name']
                if len(req.keys())>3:
                    reqs.append(req)
                    #api_audit_log.write("\n"+str(req))
                if o['uuid'] in self.special_uuid.keys():
                        for field_key in self.special_uuid[o['uuid']]:
                            self._delete_special_field(field_key,apistr)
        if len(reqs)>0:
            if 'order_by' in reqs[0].keys():
                reqs = sorted(reqs, key=lambda d: d['order_by'], reverse=True)
                for r in reqs:
                    r['order_by']+=len(reqs)
                reqs_str = json.dumps(reqs)
            else:

                reqs_str = json.dumps(reqs)
            res = requests.post(self.copy_bundle_url,data=reqs_str)
            self.add_api_call("POST",self.copy_bundle_url,reqs_str)
            res = res.json()
            self._handle_res(res,reqs,apistr=apistr,url=self.copy_bundle_url,original=original)
    def _update_settings(self,o_settings,c_settings,req,endpoint,apistr='account'):
        """update settings to match. Send the bundle request

        Args:
            o_settings (dict): original json settings
            c_settings (dict): copy json settings
            req (dict): started request that includes the URL of the api call and sid and any other hardcoded settings
        """
        if 'sid' not in req.keys():
            req['sid'] = self.sid_copy
        expected_length=len(req)
        for field in o_settings.keys():
            value = None
            if field in ['name'] or field in req.keys():
                pass
            elif c_settings is not None and c_settings !=[] and field in c_settings.keys():
                value = self.copy_field(o_settings[field],copy=c_settings[field],field_key=field,apistr=apistr)
            else:
                value = self.copy_field(o_settings[field],copy=None,field_key=field,apistr=apistr)
            if 'value' in locals() and value is not None:
                req[field] = value
        if len(req)>expected_length:
            res = requests.post(self.copy_url_base+endpoint,data=req)
            res = res.json()
            self.add_api_call("POST",self.copy_url_base+endpoint,req)
            #api_audit_log.write("\n"+str(req))
            
            self._handle_res(res,req,apistr=apistr,url=self.copy_url_base+endpoint,original=o_settings)
    def _get_map_init(self,api_strs=None):
        if api_strs == None:
            api_strs = ['customfield','role','group','location','webhook','route','hl7/template','hl7/transform','dictionary','site','radreport/template','mail/template']
            # api_strs = ['customfield','dictionary']
        else:
            api_strs = api_strs
        for apistr in api_strs:
            try:
                if apistr == "dictionary":
                    tmpstr = ["dictionarie"]
                elif apistr in ["radreport/template",'mail/template']:
                    tmpstr = ["template"]
                else:
                    tmpstr = apistr.split("/")
                o_post_url = "{url}/{apistr}/list".format(url=self.original_url,apistr=apistr)
                o_res = requests.post(o_post_url,data={"account_id":self.original_account_uuid,"sid":self.sid})
                #self.add_api_call("POST",o_post_url,{"account_id":self.original_account_uuid,"sid":self.sid})
                o = o_res.json()
                setattr(self,"o_"+apistr,o[tmpstr[-1]+"s"])
                c_res = requests.post("{url}/{apistr}/list".format(url=self.copy_url_base,apistr=apistr),data={"account_id":self.copy_account_uuid,"sid":self.sid_copy})
                #self.add_api_call("POST","{url}/{apistr}/list".format(url=self.copy_url_base,apistr=apistr),{"account_id":self.copy_account_uuid,"sid":self.sid_copy})
                c = c_res.json()
                setattr(self,"c_"+apistr,c[tmpstr[-1]+"s"])
                self._map_existing_records(c[tmpstr[-1]+"s"],o[tmpstr[-1]+"s"],apistr)
                # if o['status'] == "OK":
                    #     setattr(self,apistr,c[tmpstr[-1]+"s"])
                    # else:
                    #     self.errors.append("Script is skipping "+apistr+ "please double check permissions in clone account")
            except Exception as E:
                if apistr in self.clone_items:
                    self.errors.append("Script is skipping "+apistr+ " please double check permissions")
                    self.clone_items.pop(self.clone_items.index(apistr))
        try:
            self.o_users = self.sdk.Account.user_list(self.original_account_uuid).get()['users']
            self.c_users = self.sdk_copy.Account.user_list(self.copy_account_uuid).get()['users']
            self._map_existing_records(self.c_users,self.o_users,'user',map_by='user_email',uuidMap="user_id")
        except:
            if apistr in self.clone_items:
                self.errors.append("Script is skipping account users please double check permissions")
                self.clone_items.pop(self.clone_items.index("account/user"))

            # except:
            #     print("unable to get ")
    def _clone_customfields(self):
        #CUSTOMFIELDS
        print("updating custom fields...")
        try:
            self.o_customfield = self.sdk.Customfield.list(self.original_account_uuid).get()['customfields']
            self.c_customfield = self.sdk_copy.Customfield.list(self.copy_account_uuid).get()['customfields']
            self._map_existing_records(self.c_customfield,self.o_customfield,"customfield")
            self._add_new_records(self.o_customfield,'customfield',['object','type'])
            self.c_customfield = self.sdk_copy.Customfield.list(self.copy_account_uuid).get()['customfields']
            self._map_existing_records(self.c_customfield,self.o_customfield,"customfield")
            self._update_records_to_match(self.o_customfield,'customfield')
        except Exception as E:
            message = "customfield error skipping remaining customfields; "+str(E)
            print(message)
            self.errors.append(message)
    def _clone_roles(self):
        if not hasattr(self,"o_customfield"):
            self.o_customfield = self.sdk.Customfield.list(self.original_account_uuid).get()['customfields']
            self.c_customfield = self.sdk_copy.Customfield.list(self.copy_account_uuid).get()['customfields']
            self._map_existing_records(self.c_customfield,self.o_customfield,"customfield")
        # #ROLES

        try:
            print("Updating Roles...")
            self.o_role = self.sdk.Role.list(self.original_account_uuid).get()['roles']
            self.c_role = self.sdk_copy.Role.list(self.copy_account_uuid).get()['roles']
            self._map_existing_records(self.c_role,self.o_role,"role")
            self._add_new_records(self.o_role,'role')
            self.c_role = self.sdk_copy.Role.list(self.copy_account_uuid).get()['roles']
            self._map_existing_records(self.c_role,self.o_role,"role")
            self._update_records_to_match(self.o_role,'role')
        except Exception as E:
            message = "Role error; skipping remaining "+str(E)
            print(message)
            self.errors.append(message)
    def _clone_nodes(self):
        print("updating gateway nodes...")
        self.o_nodes = self.sdk.Node.list(self.o_account['uuid']).get()['nodes']
        self.c_nodes = self.sdk_copy.Node.list(self.c_account['uuid']).get()['nodes']
        self._map_existing_records(self.c_nodes,self.o_nodes,'node')
        self._add_new_records(self.o_nodes,'node',info_req_for_add=['type'])
        self.o_nodes = self.sdk_copy.Node.list(self.c_account['uuid']).get()['nodes']
        self._map_existing_records(self.c_nodes,self.o_nodes,'node')
        self._update_records_to_match(self.o_nodes,'node')


    def _clone_destinations(self):
        print("updating destinations...")
        self.o_dest = self.sdk.Destination.list(account_id =self.o_account['uuid']).get()['destinations']
        self.c_dest = self.sdk_copy.Destination.list(account_id =self.c_account['uuid']).get()['destinations']
        self._map_existing_records(self.c_dest,self.o_dest,'destination')
        self._add_new_records(self.o_dest,'destination',info_req_for_add=['node_id','aetitle','address','port'])
        self.c_dest = self.sdk_copy.Destination.list(account_id =self.c_account['uuid']).get()['destinations']
        self._map_existing_records(self.c_dest,self.o_dest,'destination')
        self._update_records_to_match(self.o_dest,'destination')
    def _clone_groups(self):
        #Groups
        print("updating Groups...")
        try:
            if len(self.o_group)>1 and 'site_id' in self.o_group[0].keys():
                self._add_new_records(self.o_group,'group',info_req_for_add=["site_id"])
            else:
                self._add_new_records(self.o_group,'group')
            self._update_records_to_match(self.o_group,'group')
            self._map_existing_records(self.c_group,self.o_group,'group')
        except Exception as E:
            message = "Group error; skipping remaining "+str(E)
            print(message)
            self.errors.append(message)
    def _clone_location(self):
        #Locations
        print("updating Locations...")
        try:

            self._add_new_records(self.o_location,'location')
            self._update_records_to_match(self.o_location,'location')
            self._map_existing_records(self.c_location,self.o_location,'location')
        except Exception as E:
            message = "Location error; skipping remaining "+str(E)
            print(message)
            self.errors.append(message)
    def _clone_account_users(self):
        try:
            #Copy Account Users
            print("updating Account Users...")

            self._add_new_records(self.o_users,'account/user',['email','role_id'],id='user_id',act_id='uuid',name=False)
            self.c_users = self.sdk_copy.Account.user_list(self.copy_account_uuid).get()['users']
            self._map_existing_records(self.c_users,self.o_users,'user',map_by='user_email',uuidMap="user_id")

            c_dict = {}
            for c in self.c_users:
                c_dict[c['user_email']] = c
            for o in self.o_users:
                if o['user_email'] in c_dict:
                    req = {"user_id":c_dict[o['user_email']]['user_id'],"uuid":self.copy_account_uuid}
                    self._update_settings(o,c_dict[o['user_email']],req,"/account/user/set","account/user")
        except Exception as E:
            message = "Account User error; skipping remaining "+str(E)
            self.errors.append(message)
    def _clone_webhooks(self):
        #Copy Webhooks Breaks when destination linked. Destinations cannot be copied because of linked gateway..
        try:
            
            
            print("Updating Webhooks")
            self._add_new_records(self.o_webhook,'webhook',['url','method','event','cron'])
            self._get_map_init(['webhook'])
            if 'route' in self.clone_items:
                self._add_new_records(self.o_route,'route',['conditions','actions','namespace_id'])
            o_routes = self.sdk.Route.list(self.original_account_uuid).get()['routes']
            c_routes = self.sdk_copy.Route.list(self.copy_account_uuid).get()['routes']
            self._map_existing_records(c_routes,o_routes,'route')
            self._map_existing_records(self.c_webhook,self.o_webhook,'webhook')
            self._update_records_to_match(self.o_webhook,'webhook')
            self._map_existing_records(self.c_webhook,self.o_webhook,'webhook')
        except Exception as E:
            message = "webhook error; skipping remaining "+str(E)
            print(message)
            self.errors.append(message)
    def _clone_routing_rules(self):
        try:
            #Routing Rules
            print("updating routing rules...")

            self._add_new_records(self.o_route,'route',['conditions','actions','namespace_id'])
            self._update_records_to_match(self.o_route,'route')
        except Exception as E:
            message = "Route error; skipping remaining "+str(E)
            print(message)
            self.errors.append(message)
    def _clone_group_location_users(self):
        try:
            #group and location users
            print("Updating Group Users...")

            for group in self.o_group:
                o_group_users = self.sdk.Group.user_list(group['uuid']).get()['users']
                c_group_users = self.sdk_copy.Group.user_list(self.uuid_map[group['uuid']]).get()['users']
                group_user_map = self._map_existing_records(c_group_users,o_group_users,'group/user',map_by='user_id',uuidMap="user_id",return_map=True)
                self._add_new_records([o for o in o_group_users if o['user_id'] in self.uuid_map],'group/user',['user_id','role_id'],id='user_id',act_id='uuid',name=False,namespace_users=group_user_map)
            print("Updating Location Users...")
            self.o_location = self.sdk.Location.list(self.original_account_uuid).get()['locations']
            self.c_location = self.sdk_copy.Location.list(self.copy_account_uuid).get()['locations']
            self._map_existing_records(self.c_location, self.o_location, "location")
            for location in self.o_location:
                o_location_users = self.sdk.Location.user_list(location['uuid']).get()['users']
                c_location_users = self.sdk_copy.Location.user_list(self.uuid_map[location['uuid']]).get()['users']
                location_user_map = self._map_existing_records(c_location_users,o_location_users,'location/user',map_by='user_id',uuidMap="user_id",return_map=True)
                self._add_new_records([o for o in o_location_users if o['user_id'] in self.uuid_map],'location/user',['user_id','role_id'],id='user_id',act_id='uuid',name=False,namespace_users=location_user_map)
        except Exception as E:
            message = "Group or Location User error; skipping remaining "+str(E)
            print(message)
            self.errors.append(message)
    def _clone_namespace_settings(self):

        print("Updating Namespace - Anonymize Fields/Default Fields...")
        #anonymize namespace fields
        o_account_settings = self.sdk.Account.get(self.original_account_uuid).get()

        for namespace in self.namespace_map.keys():
            ingress_tags = False
            try:
                cnamespace = self.namespace_map[namespace]
                o_settings = self.sdk.Namespace.anonymize(namespace).get()

                copy_rules = self.copy_field(o_settings['rules'],apistr="namespace/anonymize")
                if copy_rules=='{}':
                    copy_rules={}
                original_rules = json.loads(o_settings['rules'])
                copy_rules_keys = copy_rules.keys()
                # original_rule_keys = original_rules.keys()
                for key in list(copy_rules_keys): # this loop gets rid of the other_ingress_tags all other_ingress_tags from account settings are listed but cannot be set in namespace/anonymize. Expecting OTHER_INGRESS_TAGS : ANONYMIZATION VALUE instead
                    if '(' in key  and ',' in key:
                        del copy_rules[key]
                if copy_rules != {}:
                    req = {"URL":"/namespace/anonymize","sid":self.sid_copy,"rules":json.dumps(copy_rules),"uuid":cnamespace}
                    if "anonymize_at_ingress" in o_settings:
                        req['anonymize_at_ingress']=o_settings['anonymize_at_ingress']
                    res = requests.post(self.copy_bundle_url,json.dumps([req]))
                    self.add_api_call("POST",self.copy_bundle_url,json.dumps([req]))
                    res = res.json()
                    self._handle_res(res,req,apistr='/namespace/anonymize',url=self.copy_bundle_url,original=o_account_settings)
                        #api_audit_log.write("\n"+str(req))
                        #res = self.sdk.Namespace.anonymize(self.namespace_map[namespace],rules=json.dumps(copy_rules)).get()
            except Exception as E:
                message = "namespace anonymization error; skipping remaining "+str(E)
                print(message)
                self.errors.append(message)

            o_namespace_defaults = self.sdk.Namespace.study_defaults(uuid=namespace).get()['defaults']
            new_defaults = self.copy_field(o_namespace_defaults,apistr="/namespace/anonymize")

            if new_defaults is not None:
                req = {"URL":"/namespace/study/defaults","uuid":cnamespace,"sid":self.sid_copy, "defaults":json.dumps(new_defaults)}
                res = requests.post(self.copy_bundle_url,json.dumps([req]))
                self.add_api_call("POST",self.copy_bundle_url,json.dumps([req]))
                res = res.json()
                self._handle_res(res,req,apistr='/namespace/study/defaults',url=self.copy_bundle_url,original=o_namespace_defaults)
                #api_audit_log.write("\n"+str(req))
                #res = self.sdk.Namespace.study_defaults(cnamespace,defaults=json.dumps(new_defaults)).get()

            o_namespace_settings = requests.post(self.original_url+"/namespace/settings",data={"sid":self.sid,"uuid":namespace}).json()
            c_namespace_settings = requests.post(self.copy_url_base+"/namespace/settings",data={"sid":self.sid_copy,"uuid":self.namespace_map[namespace]}).json()
            self._update_settings(o_namespace_settings,c_namespace_settings,req={"uuid":self.namespace_map[namespace]},endpoint="/namespace/settings",apistr='namespace/settings')

            # self._update_settings(o_namespace_settings,c_namespace_settings,req)
    def _clone_terminology(self,vanity=""):
        try:
            #Copy Terminology:
            print("Updating Terminology...")
            terms = self.sdk.Terminology.account_overrides(account_id=self.original_account_uuid).get()['tags']
            for term in terms:
                try:
                    req = {
                        "sid":self.sid_copy,
                        "account_id":self.copy_account_uuid,
                        "language":"en",
                        'tag':term.get('tag'),
                        'value':term.get('val'),
                        'language':term['language']}
                    # if term.get('vanity') not in ['',None]:
                    #     del req['account_id']
                    #     req['vanity'] = term.get('vanity')
                    if vanity != '':
                        req['vanity'] = vanity
                    res = requests.post(self.copy_url_base+"/terminology/set",data=req)
                    self.add_api_call("POST",self.copy_url_base+"/terminology/set",req)
                    res = res.json()
                    self._handle_res(res,req,apistr='terminology',url=self.copy_bundle_url,original=terms)
                    #api_audit_log.write("\n"+str(req))
                except Exception as err:
                    message = "terminology error;"+ str(err)
        except Exception as E:
            message = "terminology error; skipping remaining "+str(E)
            print(message)
            self.errors.append(message)
    def _clone_account_settings(self):
        # try:
        print("Updating account settings...")
        #Copy account settings
        o_account_settings = self.sdk.Account.get(self.original_account_uuid).get()
        c_account_settings = self.sdk_copy.Account.get(self.copy_account_uuid).get()
        req = {"uuid":self.copy_account_uuid}
        endpoint = "/account/set"
        self._update_settings(o_account_settings,c_account_settings,req,endpoint,"account_settings")
        # except Exception as E:
        #     message = "Account Settings error; skipping remaining "+str(E)
        #     print(message)
        #     self.errors.append(message)
        # try:
        # o_template_assign = requests.post(self.original_url+"/template/assign/list",data={"account_id":self.original_account_uuid,"sid":self.sid}).json()['templates']
        # c_template_assign= requests.post(self.copy_url_base+"/template/assign/list",data={"account_id":self.copy_account_uuid,"sid":self.sid_copy}).json()['templates']
        # if len(c_template_assign)>0:
        #     c_template_assign = c_template_assign[0]
        # if len(o_template_assign)>0:
        #     o_template_assign = o_template_assign[0]
        # req = {"account_id":self.copy_account_uuid}
        # if 'name' in o_template_assign:
        #     req['name'] = o_template_assign['name']
        # for template in o_template_assign:
        #     self._update_settings(o_template_assign,c_template_assign,req,"/template/assign")
        # except Exception as E:
        #     message = "account setting - template/assign for study list error"+str(E)
        #     print(message)
        #     self.errors.append(message)
    def _clone_hl7_templates(self):
        try:
            print("updating hl7 templates...")

            self._add_new_records(getattr(self,'o_hl7/template'),'hl7/template',info_req_for_add=['body'])
            c_hl7 = self.sdk_copy.Hl7.template_list(account_id = self.copy_account_uuid).get()['templates']
            self._map_existing_records(c_hl7,self.o_hl7,"hl7/template")
            self._update_records_to_match(self['o_hl7/template'],'hl7/template')
        except Exception as E:
            message = "Hl7 Templates error; skipping remaining "+str(E)
            print(message)
            self.errors.append(message)
    def _clone_hl7_transforms(self):
        try:
            #HL7 Transformations
            print("Updating HL7 Transforms...")
            self._add_new_records(getattr(self,'o_hl7/transform'),'hl7/transform',info_req_for_add=["conditions","replacements","order_by"])
            setattr(self,'c_hl7/transform',self.sdk_copy.Hl7.transform_list(account_id=self.copy_account_uuid).get()['transforms'])
            self._map_existing_records(getattr(self,'c_hl7/transform'),getattr(self,'o_hl7/transform'),'hl7/transform')
            self._update_records_to_match(getattr(self,'o_hl7/transform'),'hl7/transform')
        except Exception as E:
            message = "Hl7 Transforms error; skipping remaining "+str(E)
            print(message)
            self.errors.append(message)
        #Dictionaries
    def _clone_rad_reports(self):
        try:
            print("Updating Rad Reports")
            c_radreports = self.sdk_copy.Radreport.template_list(self.copy_account_uuid).get()['templates']
            o_radreports = self.sdk.Radreport.template_list(self.original_account_uuid).get()['templates']
            if len(o_radreports) != 0:
                self._map_existing_records(c_radreports,o_radreports,'radreport/template')
                self._add_new_records(o_radreports,'radreport/template',info_req_for_add=['type','body'])
                c_radreports = self.sdk_copy.Radreport.template_list(self.copy_account_uuid).get()['templates']
                self._map_existing_records(c_radreports,o_radreports,'radreport/template')
                self._update_records_to_match(o_radreports,'radreport/template')
                for crad in c_radreports:
                    self.sdk_copy.Radreport.template_activate(crad['uuid']).get()
        except Exception as E:
            message = "Rad Report error; skipping remaining "+str(E)
            print(message)
            self.errors.append(message)
    def _clone_dict(self):
        try:
            print("Updating Dictionaries")

            self._add_new_records(self.o_dictionary,'dictionary',info_req_for_add=["object","lookup","replace","case_sensitive"])
            self.c_dictionary = self.sdk_copy.Dictionary.list(account_id=self.copy_account_uuid).get()['dictionaries']
            self._map_existing_records(self.c_dictionary,self.o_dictionary,'dictionary')
            self._update_records_to_match(self.o_dictionary,'dictionary')
            self.c_dictionary = self.sdk_copy.Dictionary.list(account_id=self.copy_account_uuid).get()['dictionaries']
            existing_attachments = {}
            for dict in self.c_dictionary:
                if len(dict['attachments'])>0:
                    for attachment in dict['attachments']:
                        if 'namespace_id' in attachment.keys() and attachment['namespace_id'] in self.uuid_map.values():
                            existing_attachments[dict['uuid']] = attachment['namespace_id']
                        elif  'account_id' in attachment.keys() and  attachment['account_id'] in self.uuid_map.values():
                            existing_attachments[dict['uuid']] = attachment['account_id']

            for dictionary in self.o_dictionary:
                if dictionary['attachments']!= []:
                    try:
                        req = {"sid":self.sid_copy,"uuid": self.uuid_map[dictionary['uuid']]}
                        for attachment in dictionary['attachments']:
                            if self.uuid_map[dictionary['uuid']] in existing_attachments.keys() and (('namespace_id' in attachment.keys() and attachment['namespace_id'] in self.uuid_map and self.uuid_map[attachment['namespace_id']] in existing_attachments.values()) or ('account_id' in attachment.keys() and self.uuid_map[attachment['account_id']] in existing_attachments.values())):
                                pass
                            else:
                                if 'namespace_id' in attachment.keys() and attachment['namespace_id'] in self.uuid_map.keys():
                                    req['namespace_id'] = self.uuid_map[attachment['namespace_id']]
                                elif  'account_id' in attachment.keys() and  attachment['account_id'] in self.uuid_map.keys():
                                    req['account_id'] = self.uuid_map[attachment['account_id']]
                                
                                    res = requests.post(self.copy_url_base+"/dictionary/attach",data = req)
                                    self.add_api_call("POST",self.copy_url_base+"/dictionary/attach",req)
                                    res = res.json()
                    except:
                        self.errors.append("Unable to attach dictionary "+dictionary['uuid']+" to "+str(req))
                            #api_audit_log.write("\n"+str(req))
            for dictionary in self.o_dictionary:
                try:
                    res = requests.post(self.original_url+"/dictionary/entries",data = {"sid":self.sid,"uuid":dictionary['uuid']})
                    self.add_api_call("POST",self.original_url+"/dictionary/entries",{"sid":self.sid,"uuid":dictionary['uuid']})
                    o_entries = res.json()
                    o_entries = o_entries['entries']
                    res = requests.post(self.copy_url_base+"/dictionary/entries",data = {"sid":self.sid_copy,"uuid":self.uuid_map[dictionary['uuid']]})
                    self.add_api_call("POST",self.copy_url_base+"/dictionary/entries",{"sid":self.sid_copy,"uuid":self.uuid_map[dictionary['uuid']]})
                    c_entries = res.json()
                    c_entries = c_entries['entries']
                    add_entries = o_entries
                    data = {"sid":self.sid_copy,"uuid":self.uuid_map[dictionary['uuid']]}
                    i=0
                    for entry in add_entries:
                        for c_entry in c_entries:
                            if entry['replace']==c_entry['replace'] and entry['lookup']==c_entry['lookup']:
                                add_entries.pop(i)
                        i+=1

                    for entry in add_entries:
                        for field in entry.keys():
                            value = self.copy_field(entry[field])
                            if value != None:
                                data[field]=value
                        if len(data.keys())>2:
                            res = requests.post(self.copy_url_base+"/dictionary/entry/add",data=data)
                            self.add_api_call("POST",self.copy_url_base+"/dictionary/entry/add",data)
                            res = res.json()
                            self._handle_res(res,data,apistr='dictionary/entry/add',url=self.copy_url_base+"/dictionary/entry/add",original=self.o_dictionary)
                except:
                    self.errors.append("Unable to add entries to dictionary "+dictionary['uuid']+" to "+str(data))
        except Exception as E:
            message = "Dictionary error; skipping remaining "+str(E)
            print(message)
            self.errors.append(message)
    def _clone_mail_templates(self):
        try:
            print("copying mail templates")
            o_mail_res = requests.post(self.original_url+"/mail/template/list",data={"sid":self.sid,"account_id":self.original_account_uuid})
            self.add_api_call("POST",self.original_url+"/mail/template/list",{"sid":self.sid,"account_id":self.original_account_uuid})
            o_mail_res = o_mail_res.json()
            o_mail = o_mail_res['templates']
            # for o in o_mail:
            #     if 'from_email_address' in o.keys():
            #         o['from_email_address'] = emailAddress
            #     if 'bcc' in o.keys():
            #         o['bcc'] = emailAddress
            c_mail_res = requests.post(self.copy_url_base+"/mail/template/list",data={"sid":self.sid_copy,"account_id":self.copy_account_uuid})
            self.add_api_call("POST",self.copy_url_base+"/mail/template/list",{"sid":self.sid_copy,"account_id":self.copy_account_uuid})
            c_mail_res = c_mail_res.json()
            c_mail = c_mail_res['templates']
            self._map_existing_records(c_mail,o_mail,'mail/template',map_by='type')
            self._add_new_records(o_mail,'mail/template',info_req_for_add=["type"],name = False)
            c_mail_res = requests.post(self.copy_url_base+"/mail/template/list",data={"sid":self.sid_copy,"account_id":self.copy_account_uuid})
            self.add_api_call("POST",self.copy_url_base+"/mail/template/list",{"sid":self.sid_copy,"account_id":self.copy_account_uuid})
            c_mail_res = c_mail_res.json()
            c_mail = c_mail_res['templates']
            self._map_existing_records(c_mail,o_mail,'mail/template',map_by='type')
            self._update_records_to_match(o_mail,'mail/template')
        except Exception as E:
            message = "mail/template error; skipping remaining "+str(E)
            print(message)
            self.errors.append(message)
    def _clone_sites(self):
        print("cloning sites")
        try:
            
            o_sites = self.page_list_call(self.original_url+"/site/list",{"sid":self.sid,"account_id":self.original_account_uuid},"sites")

            # o_sites = o_sites_res.json()['sites']
            # self.add_api_call("POST",self.original_url+"/site/list",{"sid":self.sid,"account_id":self.original_account_uuid})
            c_sites = self.page_list_call(self.copy_url_base+"/site/list",{"sid":self.sid_copy,"account_id":self.copy_account_uuid},"sites")
            # c_sites = c_sites_res.json()['sites']
            # self.add_api_call("POST",self.copy_url_base+"/site/list",{"sid":self.sid_copy,"account_id":self.copy_account_uuid})
            self._map_existing_records(c_sites,o_sites,'site')
            self._add_new_records(o_sites,apistr='site')
            c_sites = self.page_list_call(self.copy_url_base+"/site/list",{"sid":self.sid_copy,"account_id":self.copy_account_uuid},"sites")
            # self.add_api_call("POST",self.copy_url_base+"/site/list",{"sid":self.sid_copy,"account_id":self.copy_account_uuid})
            # c_sites = c_sites_res.json()['sites']
            self.sites = self._map_existing_records(c_sites,o_sites,'site',return_map=True)
            self._update_records_to_match(o_sites,'site')
            # self._map_existing_records(c_sites,o_sites,'site')
        except Exception as E:
            message = "Sites error; skipping remaining "+str(E)
            print(message)
            self.errors.append(message)
    def _clone_share_settings(self):
        print("updating share_settings")
        try:
            o_shares = self.sdk.Account.can_share_list(account_id=self.original_account_uuid).get()['rules']
            c_shares = self.sdk_copy.Account.can_share_list(account_id = self.copy_account_uuid).get()['rules']
            shares_to_add = o_shares
            for o in o_shares:
                if o['by_type'] == "account":
                        if self.copy_url_base == self.original_url:
                            self.uuid_map[o['by_id']] = o['by_id']
                            self.uuid_map[o['with_id']] = o['with_id']
                        elif o['by_id'] not in self.uuid_map:
                            print("please use the 'set_uuid_map' to map account uuids in share_settings prior to running the Clone script.")
                for c in c_shares:
                    if o['with_id'] in self.uuid_map and c['with_id']==self.uuid_map[o['with_id']] and o['by_id'] in self.uuid_map and c['by_id']==self.uuid_map[o['by_id']]:
                        shares_to_add.pop(shares_to_add.index(o))

            reqs = []
            for o in shares_to_add:
                req = {"URL":"/account/can/share","sid":self.sid_copy,"account_id":self.copy_account_uuid}
                for info in o:
                    req[info] = self.copy_field(o[info],apistr="/account/can/share")
                reqs.append(req)
            res = requests.post(self.copy_bundle_url,json.dumps(reqs))
            self.add_api_call("POST",self.copy_bundle_url,json.dumps(reqs))
            res = res.json()

            self._handle_res(res,reqs,'/account/can/share',self.copy_bundle_url,shares_to_add)
        except Exception as E:
            raise Exception("share settings error; skipping remaining "+str(E))
    ##### Primary Function #####
    def run(self):
        """main clone function

        Args:
            self.original_account_uuid (string): uuid of the original account
            self.copy_account_uuid (str, optional): uuid of the copy account. if '' a new account will be created. Defaults to ''.
            clone_items (list, optional): items to clone from original to copy. Options include: "all" "customfields" "roles","groups","locations","account_users","webhooks","routing_rules","group_location_users","namespace_settings","terminology","hl7_templates","hl7_transforms","dictionaries","mail_templates","account_settings. Defaults to "all".
        """

        print("Cloning {o_act_name} ({o_uuid}) to {c_account_name}({c_uuid})\n Attempting to clone {clone_items}".format(
            o_act_name=self.o_account['name'],o_uuid=self.original_account_uuid,c_account_name=self.c_account['name'],
            c_uuid=self.copy_account_uuid,clone_items=self.clone_items))

        if "customfield" in self.clone_items:
            self._clone_customfields()
        if "role" in self.clone_items:
            self._clone_roles()
        #Do customfields and roles first to get propper permissions for gathering the rest of the data.

        self._get_map_init()
        if "account_settings" in self.clone_items:
            self._clone_account_settings()
        if "group" in self.clone_items:
            self._clone_groups()
        if "location" in self.clone_items:
            self._clone_location()
        if "account/user" in self.clone_items:
            self._clone_account_users()
        if "share_settings" in self.clone_items:
            self._clone_share_settings()
        if "webhook" in self.clone_items:
            self._clone_webhooks()
        if "route" in self.clone_items:
            self._clone_routing_rules()
        if "group_location_users" in self.clone_items:
            self._clone_group_location_users()
        if "namespace_settings" in self.clone_items:
            self._clone_namespace_settings()
        if "terminology" in self.clone_items:
            self._clone_terminology()
        if "hl7/template" in self.clone_items:
            self._clone_hl7_templates()
        if "hl7/transform" in self.clone_items:
            self._clone_hl7_transforms()
        if "dictionary" in self.clone_items:
            self._clone_dict()
        if "mail_templates" in self.clone_items:
            self._clone_mail_templates()
        ### RAD REPORTS NEED FIX ###
        # if "radreport/template" in self.clone_items:
        #     self._clone_rad_reports()
        if "site" in self.clone_items:
            self._clone_sites()
        if "nodes" in self.clone_items:
            self._clone_nodes()
        if "destinations" in self.clone_items:
            self._clone_destinations()

        #Map Account UUIDs
        self.uuid_map[self.original_account_uuid] = self.copy_account_uuid

        #Map Account namespaces
        self.uuid_map[self.sdk.Account.get(self.original_account_uuid).get()['namespace_id']]=self.sdk_copy.Account.get(self.copy_account_uuid).get()['namespace_id']



        print("Errors:")

        i = 0
        for error in self.errors:
            print(str(i)+"- "+error)
            i=i+1
        if len(self.missing_users)>0:
            print(str(i)+"- Missing Users:")
            for email in self.missing_users:
                print("\t "+email)
        i = 0
    def output_api_calls(self):
        file = open(self.c_account['name']+" api calls.csv", 'w', encoding="utf-8-sig",newline="")
        output_writer = DictWriter(file,fieldnames=["Method","URL","Data"])
        for call in self.api_calls:
            output_writer.writerow(call)
        file.close()
    def output_errors(self):
        file = open(self.c_account['name']+" errors.txt", 'w', encoding="utf-8-sig",newline="")
        file.write("errors")
        i=0
        for err in self.errors:
            file.write("\n"+str(i)+"-"+err)
            i+=1
        if len(self.missing_users)>0:
            file.write("\n"+str(i)+"- Missing Users:")
            for email in self.missing_users:
                file.write("\n\t "+email)
        file.close()
    def page_list_call(self,url,data,keyword):
        all_data = []
        response = {"page":{"more":1}}
        pg_no = 1
        while response.get("page").get("more") == 1:
            data.update({"page.number":str(pg_no)}) 
            r = requests.post(url,data)
            response= r.json()
            for obj in response.get(keyword):
                all_data.append(obj)
            pg_no += 1 
        return all_data
