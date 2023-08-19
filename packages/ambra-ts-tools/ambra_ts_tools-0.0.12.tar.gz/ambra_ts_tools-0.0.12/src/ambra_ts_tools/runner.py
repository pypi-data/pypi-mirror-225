import requests
import pandas as pd
import json
import time 
import re 
from .Ambra_Clone.V2.ambra_environment import ambra_environment
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
        self.env = ambra_environment(sid,url)
        self.prep_requests()

    def prep_requests(self,df=None):
        self.reqs = []
        if df == None:
            df = self.reader_data
        pbar = tqdm(df.iterrows(),total=len(df))
        pbar.set_description("loading file")
        for i, csv_row in pbar:
            if self.endpoint == "/bundle": 
                bundle_reqs = []
                if isinstance(self.params,list):
                    for req in self.params:
                        r = {}
                        for k,v in req.items():
                            if isinstance(v,str):
                                r[k] = self.make_replacements(v,csv_row,re.findall('((?<!\{)\{(?!\{){1}[^}]+\})',v))
                            else:
                                r[k] = v
                        r['sid'] = self.sid
                        bundle_reqs.append(r)
                    self.reqs.append(json.dumps(bundle_reqs))
                    # response = self.send_requests_bundle(reqs)
                    # self.responses.append(response)
                else:
                    print("params must be a list of dictionaries when using the bundle endpoint")
                    raise "params must be a list of dictionaries when using the bundle endpoint"
            else:
                req = self.create_request(csv_row)
                self.reqs.append(req)
    def preview_data(self):
        pd.DataFrame(self.reqs).head()

    def run(self):
        self.responses = self.env.multiprocess_ambra_request(self.reqs,endpoint=self.endpoint)
        self._handle_responses(self.reqs)
        # self.failed_df.to_csv("failed.csv")
        #print the number of failed studies:
        print("failed_studies ", len(self.failed_df))
        #number of successful studies: 
        print("successful_studies ", len(self.reader_data)-len(self.failed_df))
        return self.responses
    def run_sample(self):
        sample_data = self.reqs[:5]
        response = []
        for row in sample_data:
            print("request: ",row)
            response = self.env.handle_ambra_request(self.endpoint,row)
            print("response: ", response,"\n")
                
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
            tokens_to_replace = re.findall('((?<!\{)\{(?!\{){1}[^}]+\})',v)
            if len(tokens_to_replace) == 0:
                req[k] = v
            else:
                req[k] = self.make_replacements(v,csv_row,tokens_to_replace)
        return req
    def _handle_responses(self,reqs):
        for r in self.responses:
            if r['status'] != "OK":
                index = self.responses.index(r)
                failed_study = reqs[index]
                self.failed_df.append(failed_study,ignore_index=True)
        return self.responses
    
    def summarize_responses(self):
        #print a count of each response status 
        status_counts = {}
        for r in self.responses:
            if r['status'] in status_counts:
                status_counts[r['status']] += 1
            else:
                status_counts[r['status']] = 1
        print(status_counts)

    def output_responses_to_csv(self,filename):
        pd.DataFrame(self.responses).to_csv(filename)
    def output_failed_to_csv(self,filename):
        self.failed_df.to_csv(filename)
    def rerun_failed(self):
        self.prep_requests(self.failed_df)
        self.run()