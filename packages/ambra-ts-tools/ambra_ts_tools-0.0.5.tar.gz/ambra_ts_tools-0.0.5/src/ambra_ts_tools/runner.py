import requests
import pandas as pd
import json
import time 
import re 
import __main__ as main

if not hasattr(main, '__file__'):
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm
"""
Template CSV runner -- example here is for a study/sync api call. study_id parameter uses the uuid column of the csv file specified by the user
User input can be caputured by setting a variable = input("prompt: ")
"""
class runner:
    def __init__(self,url,sid,endpoint,csv_file,params={"uuid":"{uuid}"},delimiter=","):
        self.url = url
        self.sid = sid
        self.endpoint = endpoint
        self.csv_file = csv_file
        self.params = params
        self.failed_df = pd.DataFrame(columns=pd.read_csv(csv_file).columns)
        self.reader_data = pd.read_csv(csv_file,delimiter=delimiter)
        self.failed_df = pd.DataFrame(columns=self.reader_data.columns)
        self.responses = []
    def run(self):
        reqs = []
        
        for i, csv_row in tqdm(self.reader_data.iterrows(),total=len(self.reader_data)):
            if self.endpoint == "/bundle": 
                if isinstance(self.params,list):
                    for req in self.params:
                        r = {k : self.make_replacements(v,csv_row,re.findall('(\{[^}]+\})',v)) for k,v in req.items()}
                        r['sid'] = self.sid
                        reqs.append(r)
                    response = self.send_requests_bundle(reqs)
                    self.responses.append(response)
                else:
                    print("params must be a list of dictionaries when using the bundle endpoint")
                    raise "params must be a list of dictionaries when using the bundle endpoint"
            else:
                req = self.create_request(csv_row)
                reqs.append(
                    req
                    )
                if len(reqs)==25:
                    try:
                        response = self.send_requests_bundle(reqs)
                        self.responses += response

                    except:
                        time.sleep(30)
                        response = self.send_requests_bundle(reqs)
                        self.responses += response

                    reqs = []
        self.failed_df.to_csv("failed.csv")
        #print the number of failed studies:
        print("failed_studies ", len(self.failed_df))
        #number of successful studies: 
        print("successful_studies ", len(self.reader_data)-len(self.failed_df))
        return self.responses
    def run_sample(self):
        sample_data = self.reader_data.iloc[:5]
        
        for i, csv_row in sample_data.iterrows():
            reqs = []
            if self.endpoint == "/bundle": 
                reqs = []
                if isinstance(self.params,list):
                    for req in self.params:
                        r = {k : self.make_replacements(v,csv_row,re.findall('(\{[^}]+\})',v)) for k,v in req.items()}
                        r['sid'] = self.sid
                        reqs.append(r)
                        
                    response = self.send_requests_bundle(reqs)
                    self.responses+=response
                    
                else:
                    print("params must be a list of dictionaries when using the bundle endpoint")
                    raise "params must be a list of dictionaries when using the bundle endpoint"
            else:
                req = self.create_request(csv_row)
                reqs.append(
                    req
                    )
                response =  self.send_requests_bundle(reqs)
                self.responses+=response
            for i in range(len(response)):
                print("request: ",reqs[i])
                print("response: ", response[i],"\n")
                
    def make_replacements(self,v,csv_row,tokens_to_replace):
        for token in tokens_to_replace:
            csv_fieldname = token.replace("{","").replace("}","")
            if csv_fieldname in csv_row:
                replace_value = csv_row[csv_fieldname]
                v =  v.replace(token,replace_value)
            else:
                print(token + " not found in csv")
        return v
    def create_request(self,csv_row):
        req = {
                'URL':self.endpoint,
                "sid":self.sid,
            }
        for k in self.params:
            replace_value = None
            v = self.params[k]
            tokens_to_replace = re.findall('(\{[^}]+\})',v)
            if len(tokens_to_replace) == 0:
                req[k] = v
            else:
                req[k] = self.make_replacements(v,csv_row,tokens_to_replace)
        return req
    def send_requests_bundle(self,reqs):
        response = requests.post(self.url+"/bundle",data=json.dumps(reqs)).json()
        if isinstance(self.failed_df,pd.DataFrame):
            for r in response:
                if r['status'] != "OK":
                    index = response.index(r)
                    failed_study = reqs[index]
                    self.failed_df.append(failed_study,ignore_index=True)
        return response
    
    def summarize_responses(self):
        #print a count of each response status
        status_counts = {}
        for r in self.responses:
            if r['status'] in status_counts:
                status_counts[r['status']] += 1
            else:
                status_counts[r['status']] = 1
        print(status_counts)
