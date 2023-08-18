import requests
import json 

url = input("enter url (default if blank https://access.ambrahealth.com/api/v3): ")
if url == "":
    url = "https://access.ambrahealth.com/api/v3"
account_id = input("enter account id: ")
sid = input("enter sid: ")
#
setting_to_change = input("enter setting to change (ex: allow_upload_share_code_groups_locations): ")
setting_value= input("enter setting value: ")

account = requests.post(url+"/account/get",data={"sid":sid,"uuid":account_id}).json()
ui_json = json.loads(account['settings']['ui_json'])
ui_json[setting_to_change] = setting_value

update = requests.post(url+"/account/set",data={"sid":sid,"uuid":account_id,"setting_ui_json":json.dumps(ui_json)}).json()
print(update)