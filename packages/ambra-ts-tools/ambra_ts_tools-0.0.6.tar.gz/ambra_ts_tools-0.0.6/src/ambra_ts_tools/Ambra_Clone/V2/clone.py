from json import loads
from .account_configuration import account_configuration
from .ambra_environment import ambra_environment
from tkinter.filedialog import asksaveasfilename
from json import dumps,loads
from re import findall,compile
from ast import literal_eval
from os import path
import string 
import random


class clone:
    def __init__(self, sid, original_url, original_uuid,clone_items="all",copy_url=None,copy_account_uuid=None,sid_copy=None,account_name="",original_from_file = False, create_new_users=False):
        if "/api/v3" not in original_url: 
            original_url = original_url+"/api/v3"
        self.original_environment = ambra_environment(sid,original_url)
        self.clone_items = clone_items
        if copy_url is None or copy_url == original_url:
            self.copy_environment = self.original_environment
        else:
            if "/api/v3" not in copy_url: 
                copy_url = copy_url+"/api/v3"
            self.copy_environment = ambra_environment(sid_copy,copy_url)
        dirname = path.dirname(__file__)
       
        
        if original_from_file == True:
            self.original = account_configuration(account_id=original_uuid,clone_items=self.clone_items)
        else:
            self.original = account_configuration(self.original_environment,original_uuid,clone_items=self.clone_items)
        
        self.init_config = self.original.init_config
        for config in self.init_config:
            setattr(self,config,self.init_config[config])
        
        if "all" in clone_items:
            self.clone_items= self.available_api_strs
        
        self.copy = account_configuration(self.copy_environment,copy_account_uuid,account_name,clone_items=self.clone_items)
        self.uuid_pattern= compile('((?:(?:\d|\w){8}-)(?:(?:\d|\w){4}-){3}(?:(?:\d|\w){12}))')
        self.create_new_users = create_new_users
        self.uuid_map = {}
        self.errors = []
        self.mapped_records ={}
        self.records_to_update = {}
        self.whitelisted_names = {}
        self.map_all_api()
        self.records_to_add = self.get_records_to_add()

    def get_records_to_add(self):
        records_to_add = {}
        for apistr in self.clone_items:
            if apistr in ['account/can/share','account'] or 'namespace' in apistr:
                pass
            # elif apistr == "account/can/share":
            #TODO: ADD account/can/share
            else:
                if apistr in ["group/user","location/user","account/user"]:
                    key = 'user_id'
                else:
                    key = 'uuid'
                
                if apistr not in ["group/user","location/user"]:
                    for o in getattr(self.original,apistr):
                        if o[key] not in self.uuid_map.keys():
                            if apistr not in records_to_add.keys():
                                records_to_add[apistr] = []
                            records_to_add[apistr].append(dict(sorted(o.items())))
                else:
                    
                    user_json = getattr(self.original,apistr)
                    for namespace_uuid in user_json:
                        if self.uuid_map.get(namespace_uuid) in getattr(self.copy,apistr).keys():
                            ns_users = [u['user_id'] for u in getattr(self.copy,apistr)[self.uuid_map[namespace_uuid]]]
                            for original_namesapce_user in user_json[namespace_uuid]:
                                if self.uuid_map.get(original_namesapce_user['user_id']) not in ns_users:
                                    if apistr not in records_to_add.keys():
                                        records_to_add[apistr] = []
                                    records_to_add[apistr].append(dict(sorted(original_namesapce_user.items())))
                        else:
                            for o in user_json[namespace_uuid]:
                                if apistr not in records_to_add.keys():
                                        records_to_add[apistr] = []
                                records_to_add[apistr].append(dict(sorted(o.items())))
        return records_to_add
    
    def add_new_records(self):
        if self.create_new_users == True:
            self.add_users_to_instance(getattr(self.original,"account/user"))
        for apistr in self.records_to_add:
            print("adding "+apistr)
            records = self.records_to_add[apistr]
            reqs = []
            for record in records:
                if ('uuid' in record and (record['uuid'] in self.skip_uuid)) or (self.whitelisted_names.get(apistr) != None and record['name'] not in self.whitelisted_names[apistr]):
                        pass
                else:
                    req = {"account_id":self.copy.account_id,"name":record.get("name")}
                    if apistr == "group" and "site_id" in record.keys():
                        self.required_add_fields[apistr].append("site_id")
                    for field in self.required_add_fields[apistr]:
                        req[field] = self.copy_field(record.get(field),None,field,apistr,record)
                        if field in self.cast_as_string:
                            req[field] = dumps(record.get(field))
                    if 'user' in apistr:
                        req['email'] = record.get('user_email')
                        req["name"] = record.get('user_name')
                        if apistr in ["group/user","location/user"]:
                            if record.get('user_id') != None:
                                req['user_id'] = self.uuid_map.get(record.get('user_id'))
                                if req['user_id'] is None:
                                    req['user_id'] = record.get('user_id')
                                    self.errors.append("user_id not found for "+apistr+" "+record.get('user_id')+" "+record.get('user_name'))
                            req['uuid'] = self.uuid_map[record.get('uuid')]
                    if 'account' in apistr:
                        req['uuid'] = self.copy.account_id
                    reqs.append(req)        
            response = self.copy_environment.multiprocess_ambra_request(reqs,apistr+"/add")
            for r in response: 
                if r != None:
                    i = response.index(r)
                    possible_ids_to_match= ["uuid","user_id","namespace_id"]
                    if apistr == 'account/user':
                        self.update_uuid_map({self.records_to_add[apistr][i]['user_id'] : r['uuid']})
                    else:
                        for id in possible_ids_to_match:
                            if id in r.keys() and id in self.records_to_add[apistr][i].keys():
                                self.update_uuid_map({self.records_to_add[apistr][i][id] : r[id]})
        self.copy.reload_account_configuration([r for r in self.records_to_add.keys()])
        self.map_all_api()
    def map_all_api(self):
        self.uuid_map[self.original.account['uuid']] = self.copy.account['uuid']
        self.uuid_map[self.original.account['namespace_id']] = self.copy.account['namespace_id']
        for api_str in self.available_api_strs:
            
            if not 'namespace' in api_str and api_str not in ['account','group/user','location/user','terminology','account/can/share']:
                uuid_map = self.map_existing_records(api_str)
                if uuid_map != None:
                    self.update_uuid_map(uuid_map)
    def map_existing_records(self,apistr): #assumes and updates and uuid_map
        is_uuid = False
        if 'user' in apistr:
            map_by='user_email'

        elif 'mail/template'  == apistr:
            map_by='type'
        elif 'customfield/mapping' == apistr:
            map_by= 'from_customfield_id'
            is_uuid = True
        else:
            map_by='name'
    
        map = {}
        if hasattr(self.original,apistr):
            # for apistr in self.available_api_strs:
            if isinstance(getattr(self.copy,apistr),list):
                for c in getattr(self.copy,apistr):
                    for o in getattr(self.original,apistr):
                        if is_uuid == True: 
                            original_map = self.uuid_map.get(o[map_by])
                        else:
                            original_map = o[map_by]
                        if c[map_by].upper() == original_map.upper() or "MISSING INFORMATION: "+ o[map_by].upper()==c[map_by].upper() or "Missing Actions- "+ o[map_by].upper()==c[map_by].upper():
                            
                            if 'uuid' in o.keys() and 'uuid' in c.keys():
                                self.uuid_map[o['uuid']]=c['uuid']
                                self.mapped_records[o['uuid']] = [o,c]
                            if 'user_id' in o.keys():
                                self.uuid_map[o['user_id']]=c['user_id']
                                self.mapped_records[o['user_id']] = [o,c]
                            if 'user_account_id' in o.keys():
                                self.uuid_map[o['user_account_id']]=c['user_account_id']
                                self.mapped_records[o['user_account_id']] = [o,c]
                            if 'namespace_id' in o.keys() and apistr !='route': #map namespace ids
                                self.uuid_map[o['namespace_id']] = c['namespace_id']
                                self.mapped_records[o['namespace_id']] = [o,c]
                            # self.namespace_map[o['namespace_id']] = c['namespace_id']
        if map != {}:
            return map     
    
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
        'filter' not in field_key,
        len(field_key.split(':'))<2]
        if all(conditions): #skip the json field if the copy and original are the same.
            if field_key in ['lv','op','rv','search_source','order_by']:
                output = original

        elif apistr in self.skip_fields.keys() and field_key in self.skip_fields[apistr] and apistr+":"+field_key not in self.special_fields.keys():
            pass
        elif apistr+":"+field_key in self.special_fields.keys():
            if "REPLACE" not in self.special_fields.get(apistr+":"+field_key):
                output = self.special_fields.get(apistr+":"+field_key)
            else:
                output = original
                for r in self.special_fields.get(apistr+":"+field_key).split("|"):
                    replace_array = r.split("^")
                    output = output.replace(replace_array[1],replace_array[2])
        elif isinstance(original,dict):
            if 'uuid' in original and original['uuid'] in self.skip_uuid:
                pass
            elif field_key in ['parameters','settings','options'] and apistr not in ["radreport/template"]:
                value = self._parse_dictionary_field(original,copy,field_key=field_key,return_type='list',apistr=apistr,original_object=original_object)
            elif field_key in ['defaults','share_settings','settings:viewer3_config','options', 'customfields:options','customfields:value','linked_study_accounts','settings:upload_settings','settings:ui_json',"settings:study_status_tags_attributes","permissions:ui_json","permissions","study_field_flags","settings:login_json"] or (apistr =='node' and 'configuration' in field_key):
                value = self._parse_dictionary_field(original,copy,field_key=field_key,return_type='json',apistr=apistr,original_object=original_object)
            else:
                value = self._parse_dictionary_field(original,copy,field_key=field_key,apistr=apistr,original_object=original_object)
            if value is not None:
                output = value
        elif isinstance(original,int) or isinstance(original,float):

            if original == 0 and copy is None and apistr not in ['dictionary','group','location','radreport/template','site_qualified',"namespace/study/defaults","account/user"]:
                pass
            elif (apistr == "radreport/template" and field_key=="active"):
                output = str(original)
            else:
                output = original
        elif isinstance(original,str):
            if original == copy and len(field_key.split(':'))<2 and  'filter' not in field_key :
                pass
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
                if apistr in ['route','hl7/transform','role','account/user','account'] and field_key in ['actions','conditions','replacements','customfields']:
                    output = dumps(output)
        elif original is None:
            output = None
        else:
            print("COPY_FIELD TYPE ERROR DOUBLECHECK ",original)
        if 'output' in locals() and output is not None:
            return output
    
    def _update_records_to_match(self,original,apistr,read_only=False):
        """update records in the copy account to match records in the original account

        Args:
            original (list): list of oringal records that will serve as the master copy updating their mappings in the uuid_map variable.
            apistr (string): apistr (string): string that cooresponds to the ambra api object
        """
        if read_only == True:
            print("gathering data for update "+apistr)
        else:
            print("updating "+apistr)
        reqs =[]
        if apistr in self.list_api_strs or apistr == 'account':
            set_endpoint = apistr+'/set'
        else:
            set_endpoint = apistr

        if isinstance(original,list):
            for o in original:
                

                ldict = {}
                if 'user' in apistr:
                    id = "user_id"
                else:
                    id = "uuid"
                req = {'uuid':self.uuid_map.get(o[id])}
                if read_only:
                    if 'name' in o.keys():
                        req['name'] = o['name']
                    if 'user_email' in o.keys():
                        req['email'] = o['user_email']
                    if 'user_name' in o.keys():
                        req['user_name'] = o['user_name']
                if o[id] in self.mapped_records:
                    if 'user' in apistr: 
                        req["user_id"] = self.uuid_map.get(o['user_id'])
                    if 'account' in apistr:
                        req['uuid'] = self.copy.account['uuid']
                    if 'namespace' in apistr: 
                        set_endpoint = apistr
                        c = self.copy.namespace_properies_by_id[self.uuid_map[o['uuid']]].get(apistr)
                    else:
                        c = self.mapped_records.get(o[id])[1]
                    
                    
                    if o[id] in self.special_uuid.keys():
                        for field_key in self.special_uuid[o[id]]:
                            self.add_special_field(field_key=field_key,apistr=apistr,value=self.special_uuid[o['uuid']][field_key])
                    if ('uuid' in o and o[id] in self.skip_uuid) or (self.whitelisted_names.get(apistr) != None and o['name'] in self.whitelisted_names[apistr]):
                        pass
                    else:
                        for field in o.keys():
                            field_uuids = findall(self.uuid_pattern,field)

                            if field == 'uuid':
                                pass
                            elif field == "attachments" and apistr == "dictionary":
                                for attachment in o['attachments']:
                                    if attachment['uuid'] in self.uuid_map:
                                        req['attachments'].append({"uuid":self.uuid_map[attachment['uuid']]})
                            elif field == "customfields":
                                for cf in o["customfields"]:
                                    if cf['uuid'] in self.uuid_map:
                                        req['customfield-'+self.uuid_map[cf['uuid']]] = cf['value']
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
                                if field in self.cast_as_string:
                                    value = dumps(value)
                                req[field] = value
                                del value
                    # if apistr=='route' and 'actions' in req.keys() and "MISSING INFORMATION" in str(req['actions']):
                    #         del req['actions']
                    #         if c['name'] != "Missing Actions- "+ o['name']:
                    #             req['name'] = "Missing Actions- "+ o['name']
                    if len(req.keys())>1:
                        reqs.append(req)
                        #api_audit_log.write("\n"+str(req))
                    if o[id] in self.special_uuid.keys():
                            for field_key in self.special_uuid[o[id]]:
                                self._delete_special_field(field_key,apistr)
                else:
                    self.errors.append(apistr+" "+o[id]+"is not in the mapped records")     
        elif apistr in ['group/user',"location/user"]:
            for ns in original:
                for o in original[ns]:
                    req = {}
                    for field in o: 
                        value = self.copy_field(o[field],copy=None,field_key=field,apistr=apistr,original_object=o)     
                        if value is not None:
                            req[field] = value
                    if len(req.keys())>1:
                        reqs.append(req)
        else:
            o = original
            req = {'uuid':self.uuid_map[o['uuid']]}
            if apistr=='account':
                c = self.copy.account
            if 'account' in apistr:
                req['uuid'] = self.copy.account['uuid']
            
            for field in o.keys():
                field_uuids = findall(self.uuid_pattern,field)

                if field == 'uuid':
                    pass
                elif field == "customfields":
                    for cf in o["customfields"]:
                        if cf['uuid'] in self.uuid_map:
                            req['customfield-'+self.uuid_map[cf['uuid']]] = cf['value']
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
            if len(req.keys())>1:
                reqs.append(req)
        if len(reqs)>0:
            if 'order_by' in reqs[0].keys():
                reqs = sorted(reqs, key=lambda d: d['order_by'], reverse=True)
                for r in reqs:
                    r['order_by']+=len(reqs)
                    if read_only == True:
                        if apistr not in self.records_to_update.keys():
                            self.records_to_update[apistr] = []
                        self.records_to_update[apistr].append(dict(sorted(r.items())))
                    else:
                        self.copy_environment.handle_ambra_request(set_endpoint,data=r)
            else:
                if read_only == True:
                    if apistr not in self.records_to_update.keys():
                        self.records_to_update[apistr] = []
                    self.records_to_update[apistr]+=[dict(sorted(req.items())) for req in reqs]
                else:
                    self.copy_environment.multiprocess_ambra_request(reqs,set_endpoint)
        return reqs
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
        original_uuids = findall(self.uuid_pattern,original)
        if original==copy and len(original_uuids)==0 and len(key.split(":"))<2 and 'filter' not in key: # skip if original same as copy
            pass
        elif original in ['','{}','[]',""]:
            if copy is not None and copy in ['','{}','[]',""]:
                    pass
            else:
                if key == 'ui_json':
                    output = dumps({})
                else:
                    output = original
        elif original[0]=='{' and original[-1]=="}" and  original[-2]!="}": #If json string. convert to json object- rerun copy_field function.
            modified_original = original.replace('\n',"").replace('\t',"")
            if modified_original[-2] == ",":
                modified_original = modified_original[:-2]+modified_original[-1]
            if copy is not None and copy not in ['{}',''] and isinstance(copy, str) and copy[0]=="{" and copy[-1]=="}" and apistr not in ['hl7/transform']:
                value= self.copy_field(loads(modified_original),loads(copy),field_key=key,apistr=apistr,original_object=original_object)
            elif len(modified_original.split(":"))==1 or apistr in ['hl7/transform']: #Not true json object.
                value = modified_original
            else:
                
                value= self.copy_field(loads(modified_original),field_key=key,apistr=apistr,original_object=original_object)
        
            output = value
            if key=='ui_json' and output != None:
                output = dumps(value)
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
                    # self.uuid_not_found.append(uuid)
                    self.errors.append("uuid match not found for {apistr}, Item:{key}, Name:{name}, uuid:{uuid}".format(apistr=apistr.upper(),key=key,uuid=uuid,name=name))
                    # if 'output' in locals():
                    #     del output
        elif original!='' and original[0]=="[" and key not in ['share_settings:setTextElements:selector','settings:study_status_tags_attributes','settings:study_status_tags_attributes:study-listLoaded:all:selector',"settings:passwd_regexp",'options:hint']:
                original = literal_eval(original)
                output = self.copy_field(original,copy,field_key=key,apistr=apistr,original_object=original_object)
                if len(output)>0:
                    output= dumps(output)
        # elif original == "0" and (copy is None or copy =='[]'):
        #     pass
        elif original is None:
            output = ''
        else:
            output= original
        if 'output' in locals() and output is not None:
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
                    copy = loads(copy)
                else:
                    copy = None
            for field in original.keys():

                field_uuids = findall(self.uuid_pattern,field)

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
            return dumps(output)
        elif return_type =='list':
            return [dumps(output)]
        else:
            return output
    def add_users_to_instance(self,users):
        """add users to new instance where they do not already exist

        Args:
            users (list): user list as returned by the account/user/list api call
        """
        for user in users:
            if user['user_id'] in self.uuid_map:
                pass
            else:
                character_list = string.ascii_letters + string.digits + "!@#$%"
                password = random.choice(string.ascii_lowercase)+ random.choice(string.ascii_uppercase)+random.choice(string.digits)+random.choice(string.digits)+random.choice("!@#$%")
                while len(password)<10:
                    password+=random.choice(character_list)
                name_list = user['user_name'].split(" ")
                first = " ".join(name_list[0:-1])
                last = name_list[-1]
                data = {
                    "account_id":self.copy.account['uuid'],
                    "first":first,
                    'last':last,
                    'password':password,
                    'email':user['user_email'],
                }
                if 'mobile_phone' in user.keys():
                    data['mobile_phone'] = user['mobile_phone']
                self.copy_environment.handle_ambra_request("user/add",data=data)
        # and viewer config 
            user_viewer_settings = self.original_environment.handle_ambra_request("setting/get",data={"key":"viewer3_config","user_id":user['user_id']})       
            if user_viewer_settings not in ["",None]:
                self.copy_environment.handle_ambra_request("setting/set",data={"key":"viewer3_config","user_id":user['user_id'],"value":user_viewer_settings['value']})            
    
    def get_records_to_update(self):
        for apistr in self.clone_items:
            if len(getattr(self.original,apistr))!=0 and apistr not in ['location/user','group/user','account/can/share']:
                self._update_records_to_match(getattr(self.original,apistr),apistr,read_only=True)
            # elif apistr == "account/can/share":
    def update_to_match(self):
        """update copy to match original
        """
        for apistr in self.clone_items:
            if len(getattr(self.original,apistr))>0 and apistr not in ['location/user','group/user','account/can/share']:
                self._update_records_to_match(getattr(self.original,apistr),apistr)  
    def output_errors_to_file(self,output_file_path=None):
        """prompt user for output file path and write errors to file

        Args:
            output_file_path (str, optional): if None will prompt user with dialog box. Defaults to None.
        """
        if output_file_path in [None,""]:
            output_file_path = asksaveasfilename(initialfile="errors.txt",title="Save Errors to File",filetypes=(("Text File","*.txt"),("All Files","*.*")))
        output_file = open(output_file_path,'w')
        output_file.write("Read Errors:")
        read_err = 0
        read_warn = 0
        write_err = 0
        write_warn = 0
        clone_err = 0
        for err in self.original_environment.errors:
            read_err+=1
            output_file.write("\n\t"+str(read_err)+" - "+str(err))
        output_file.write("\nRead Warnings:")     
        for warn in self.original_environment.warnings:
            read_warn+=1
            output_file.write("\n\t"+str(read_warn)+" - "+str(warn))
        output_file.write("\n")
        output_file.write("\nWrite Errors:")    
        for err in self.copy_environment.errors:
            write_err+=1
            output_file.write("\n\t"+str(write_err)+" - "+str(err))
        output_file.write("\nWrite Warnings:")
        for warn in self.copy_environment.warnings:
            write_warn+=1
            output_file.write("\n\t"+str(write_warn)+" - "+str(warn))
        output_file.write("\nClone Errors:")
        for err in self.errors:
            clone_err+=1
            output_file.write("\n\t"+str(clone_err)+" - "+str(err))
    def output_script_plan(self, output_file_path=None):
        self.get_records_to_update()
        #prompt for save file- output json file of records_to_add and records_to_update
        #format json file

        if output_file_path in [None,""]:
            output_file_path = asksaveasfilename(initialfile="script_plan.csv",title="Save Script Plan to File",filetypes=(("csv","*.csv"),("All Files","*.*")))
        output_file = open(output_file_path,'w',newline="")
        output_writer = DictWriter(output_file,fieldnames=['endpoint','name','data'])
        output_writer.writeheader()
        actions = {"add":self.records_to_add,"set":self.records_to_update}
        for action in actions:
            for apistr in actions[action]:
                records = actions[action][apistr]
                for record in records:
                    name = ""
                    if 'name' in record.keys():
                        name = record['name']
                    elif 'user_name' in record.keys():
                        name = record['user_name']
                    elif 'user_email' in record.keys():
                        name = record['user_email']
                    if apistr in self.list_api_strs:
                        endpt = apistr+"/"+action
                    else:
                        endpt = apistr
                    output_writer.writerow({'endpoint':endpt,'name':name,'data':record})



## add a function that copies a dictionary 
