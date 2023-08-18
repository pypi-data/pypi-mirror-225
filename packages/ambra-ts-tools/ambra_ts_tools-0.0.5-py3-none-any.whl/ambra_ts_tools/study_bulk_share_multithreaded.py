import csv
# from tqdm import tqdm
import time
import requests
import json
from tkinter import Tk
from tkinter import filedialog
from multiprocessing.pool import Pool
"""

Study thin add template -- Ensure column headers match values in the studyadd function

"""
#namespace = '09070acd-43ed-4ccc-a861-6f9eba443e99'
#node = 'd5e98b1d-c320-45c1-87a6-eb7a3591e9a9'

#accn_set = {}

csv.field_size_limit(50000<<10) #for really big csvs increase the csv python memory limit

def send_requests_bundle(reqs,retry=0):
    failed = 0
    ok = 0
    url = "https://access.ambrahealth.com/api/v3"
    try:
        response = requests.post(url+"/bundle",data=json.dumps(reqs)).json()
        for r in response:
            if r['status'] != "OK":
                failedwriter = csv.DictWriter(open('failed.csv','a',newline=""),fieldnames=['uuid','reason'])
                index = response.index(r)
                failed_study = reqs[index]
                failedwriter.writerow({"uuid":failed_study.get('study_id'),"reason":r['error_type']})
                failed+=1
            else:
                ok+=1
        return [ok,failed]
    except Exception as err:
        if retry < 3:
            time.sleep(10)
            retry+=1
            send_requests_bundle(reqs, retry)
        else:
            return


if __name__ =='__main__':
    
    sid = input("sid: ")
    share_type = input("share to type: account_id or location_id or group_id or user_id or share_code or email: ")
    share_id = input(share_type+": ")
    namespace = "09070acd-43ed-4ccc-a861-6f9eba443e99"
    node = "d5e98b1d-c320-45c1-87a6-eb7a3591e9a9"
    root = Tk()
    # root.withdraw()
    study_list_file = filedialog.askopenfilename(title="csv list of studies with uuid header")
    studies = set(l['uuid'] for l in csv.DictReader(open(study_list_file,'r')))
    print("processing data...")
    bundles = []
    reqs = []
    for uuid in studies: 
        reqs.append(
            {"URL":"/study/share",
            "uuid":uuid,
            "sid":sid,
            share_type:share_id
             }
            )
        if len(reqs)==100:
            bundles.append(reqs)
            reqs = []
            
    bundles.append(reqs)
    pool = Pool(processes=10)
    results = []
    ok = 0
    fail = 0
    print("total:"+str(len(studies)))
    for r in pool.imap_unordered(send_requests_bundle, bundles):
        ok+=r[0]
        fail+=r[1]
        print("number of OK api responses: "+str(ok)+"-- number of failed shares: " +str(fail), end="\r")
