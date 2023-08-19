import matplotlib.pyplot as plt
import os
import zipfile
import pandas as pd
import requests
import re

class log_parser:
  def __init__(self,node_id,sid,url="https://access.ambrahealth.com/api/v3"):
    self.node = requests.post(url+"/node/get",data={"sid":sid,"uuid":node_id}).json()
    ip_regex = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    self.ip_address = re.findall(ip_regex,self.node["name"])[0]
    self.log_study = requests.post(url+"/study/list",data={"sid":sid,"filter.phi_namespace.equals":self.node["storage_namespace"],"filter.patient_name.like":"%"+self.ip_address+"%"}).json()['studies'][0]
    self.url = url
    self.sid = sid
  def pull_log(self,start,end,type):
      return requests.post(self.url+"/node/log",data={
        "sid":self.sid,
        "uuid":self.node["uuid"],
        "start":start,
        "end":end,
        "type":type
    })
  def retrieve_latest_log(self):
    url_base = self.url.replace("/api/v3","")
    storage_url = url_base+"/host/{engine_fqdn}/api/v3/storage/study/{storage_namespace}/{study_uid}/attachment/latest".format(**self.log_study)
    response = requests.get(storage_url,params={"sid":self.sid,"phi_namespace":self.log_study['phi_namespace']})
    if response.status_code == 200:
        with open('data.zip', 'wb') as file:
            file.write(response.content)
    else:
        print("Failed to download the zip file.")
        exit()

    # Step 3: Ensure the 'extracted_files' directory is empty
    if os.path.exists('extracted_files'):
        for file_name in os.listdir('extracted_files'):
            file_path = os.path.join('extracted_files', file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print("Error while clearing 'extracted_files':", e)

    # Step 4: Extract the contents of the zip file
    with zipfile.ZipFile('data.zip', 'r') as zip_ref:
        zip_ref.extractall('extracted_files')

    # Step 5: Iterate through the extracted files, read each text file as a CSV, and load it into a Pandas DataFrame
    self.data_frames = []

    self.headers  = [
    "Timestamp", "burn pending", "burn enqueued", "burn dequeued",
    "download pending", "download enqueued", "download dequeued",
    "downloadtranscode pending", "downloadtranscode enqueued", "downloadtranscode dequeued",
    "hl7client pending", "hl7client enqueued", "hl7client dequeued",
    "hl7upload pending", "hl7upload enqueued", "hl7upload dequeued",
    "move pending", "move enqueued", "move dequeued",
    "queryclient pending", "queryclient enqueued", "queryclient dequeued",
    "retrieveclient pending", "retrieveclient enqueued", "retrieveclient dequeued",
    "storagecommit pending", "storagecommit enqueued", "storagecommit dequeued",
    "upload pending", "upload enqueued", "upload dequeued",
    "uploadtranscode pending", "uploadtranscode enqueued", "uploadtranscode dequeued"
    ]

    for file_name in os.listdir('extracted_files'):
        csv_file_path = os.path.join('extracted_files', file_name)
        df = pd.read_csv(csv_file_path, delimiter=',',names=self.headers)  # You might need to adjust the delimiter
        self.data_frames.append(df)
    consolidated_df = pd.concat(self.data_frames, ignore_index=True)
    self.data_frame = consolidated_df[consolidated_df.Timestamp.str.contains("Timestamp")==False]
    for h in self.headers:
        if h != "Timestamp":
            self.data_frame[h] = self.data_frame[h].apply(pd.to_numeric)
    self.data_frame = self.data_frame.sort_values(by=["Timestamp"])


