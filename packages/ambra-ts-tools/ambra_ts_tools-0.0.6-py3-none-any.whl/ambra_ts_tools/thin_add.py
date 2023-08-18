import csv
from dataclasses import field
from threading import local
from venv import create 
from tqdm import tqdm
import re
import time
import requests
from datetime import datetime
from ambra_sdk.api import Api
import json
from tkinter import Tk
from tkinter import filedialog

"""

Study thin add template -- Ensure column headers match values in the studyadd function

"""

def studyadd(study):
    global adds
    if 'namespace' in globals() and namespace not in ['',None]:
        study['storage_namespace'] = namespace
        study['phi_namespace'] = namespace
    if 'node' in globals() and node not in ['',None]:
        study['node_id'] = node
    try:
    
        request = {
            "URL":"/study/add",
            "sid":sid,
            "storage_namespace":study.get("storage_namespace"),
            "phi_namespace":study.get("phi_namespace"),
            "accession_number":study.get("accession_number"),
            "modality":study.get('modality'),
            "patient_birth_date":study.get("patient_birth_date"),
            "patient_name":study.get("patient_name"),
            "patient_sex":study.get("patient_sex"),
            "patientid":study.get("patientid"),
            "referring_physician":study.get("referring_physician"),
            "study_description":study.get("study_description"),
            "study_date":study.get("study_date"),
            "study_uid":study.get("study_uid"),
            "node_id":study.get("node_id"),
            'thin':1
        }
        return request
    except Exception as err:
        print(err)



    

# csv.field_size_limit(50000<<10) for really big csvs increase the csv python memory limit


if __name__ =='__main__':
    sid = input("sid: ")
    api = Api.with_sid('https://access.ambrahealth.com/api/v3', sid)
    namespace = input("namespace: ")
    node = input("node: ")
    Tk()

    thin_data_filename = filedialog.askopenfile(title="select thin add csv file").name
    existing_uid_filename = filedialog.askopenfile(title="existing uid csv file").name
    lines = csv.DictReader(open(thin_data_filename,"r+",encoding="utf-8-sig"))
    uids = set(l['study_uid'] for l in csv.DictReader(open(existing_uid_filename,'r')))
    #Get the length of the file
    length=0
    for l in open(thin_data_filename,"r+"): 
        length+=1

    #if historic_data gets too big add counter to reset after size gets to 
    historic_data = {}
    studies_to_add=0
    print("processing data...")
    for row in tqdm(lines): 
        historic_data[row['study_uid']] = row

    
    historic_uid = set(historic_data.keys())
    new_uid = list(historic_uid-uids)

    chunk = []
    print("adding studies...")
    for uid in tqdm(new_uid,total =len(new_uid)):
        study = historic_data[uid]
        print(uid)
        if len(chunk) < 25:
            req = studyadd(study)
            if req != None:
                chunk.append(req)
        else:
            chunk.append(req)
            try:
                res = requests.post("https://access.ambrahealth.com/api/v3/bundle",data = json.dumps(chunk))
                response = res.json()
            except:
                time.sleep(30)          
                res = requests.post("https://access.ambrahealth.com/api/v3/bundle",data = json.dumps(chunk))
                response = res.json()         
            chunk = []
    if len(chunk)>0:
        res = requests.post("https://access.ambrahealth.com/api/v3/bundle",data = json.dumps(chunk))
        response = res.json()
        chunk = []
