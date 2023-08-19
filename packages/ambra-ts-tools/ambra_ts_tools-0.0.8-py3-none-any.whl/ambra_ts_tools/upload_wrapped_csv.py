import requests
import tempfile
import csv
import json
import os
import io

sid  = ""
url = "https://access.ambrahealth.com/api/v3"

def upload_wrapped_csv(namespace_id,report_title,data):
    """export a wrapped csv file to the namespace specified. assumes sid global variable and ambra sdk 

    Args:
        namespace_id (str): ambra namespace uuid
        report_title (str): report name to display in ambra
        output_data (list): list of dictionaries, dict keys will be the csv headers
    """
    fieldnames = list(data[0].keys())
    fqdn = requests.post(url+"/namespace/engine/fqdn",data={"namespace_id":namespace_id,"sid":sid }).json()['engine_fqdn']
    
    # create binary of csv file 
    temp = io.StringIO()
    writer = csv.DictWriter(temp,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    temp.seek(0)
    string_out = temp.read()
    binarray = str.encode(string_out)
    # use binarray to write a temporary file that can be uploaded using requests
    with  tempfile.NamedTemporaryFile('rb+') as tmp_f:
        tmp_f.name = report_title+'.csv'
        tmp_f.write(binarray)
        tmp_f.seek(0)
        file_size = os.fstat(tmp_f.fileno()).st_size
        headers = {'X-File-Size': str(file_size)}        
        wrap_url = "https://{engine_fqdn}/api/v3/storage/namespace/{namespace}/wrap".format(
            engine_fqdn = fqdn,
            namespace=namespace_id
            )
        response = requests.post(wrap_url,headers=headers,params= {
                "tags":json.dumps({"(0010,0010)":report_title}),
                "sid":sid},
            files={'file':tmp_f})
        res = response.json()


## TEST DATA  EXAMPLE## 
# TEST 1
# data = [{'column1':"column_1_value","column2":"column_2_value"},{'column1':"column_1_value_row2","column2":"column_2_value_row2"}]
# upload_wrapped_csv('3ec380b3-f241-4a8f-b9dc-ae057096b20d',"TEST^REPORT",data)
# TEST 2 
# reader = [r for r in csv.DictReader(open(r'C:\Users\17633\Documents\tech-services-scripts\Internal Scripts\audit_31515.csv','r',encoding='utf-8-sig'))]
# upload_wrapped_csv('3ec380b3-f241-4a8f-b9dc-ae057096b20d',"NEWTEST^REPORT",reader)