from csv import DictReader, DictWriter

from tkinter import filedialog
from tkinter import Tk
import tkinter as tk


def get_filenames(root):
    
    root.geometry=("500x200")
    ambra_label = tk.Label(root,text="Ambra File")
    source_label = tk.Label(root,text="Source File")
    def set_ambra_name():
        try:
            filename =  filedialog.askopenfile().name
            ambra_label.config(text=filename)
        except:
            pass
    def set_source_name():
        try:
            filename =  filedialog.askopenfile().name
            source_label.config(text=filename)
        except:
            pass
        
        
        
    ambra_button = tk.Button(root,text='Select Ambra File ("study_uid" & "image_count" MUST BE A COLUMN)',command=set_ambra_name)   
    source_button = tk.Button(root,text='Select Source File ("study_uid" & "image_count" MUST BE A COLUMN)',command=set_source_name)
    next_button = tk.Button(root,text='ok',command=root.quit,width=30)

    ambra_button.grid(column=1,row=1)
    ambra_label.grid(column=2,row=1)
    source_button.grid(column=1,row=2)
    source_label.grid(column=2,row=2)
    next_button.grid(column=1,row=4)
    root.mainloop()
    ambra = ambra_label.cget('text')
    source = source_label.cget('text')
    root.destroy()
    return (source,ambra)
def get_reader(root):
    filenames=None
    while filenames == None:
    #     get_filenames()
    #     # file_name = input()
    #     if file_name == "":
    #         return ""
    #     if file_name[-4:] != '.csv':
    #         file_name = file_name+".csv"
            
    #     if not path.isfile(getcwd()+"/"+file_name) and not path.isfile(file_name):
    #         print("'"+file_name+"' not found in '"+getcwd()+"'")
       filenames = get_filenames(root)
    

    ambra_file_name=filenames[1]
    source_file_name = filenames[0]
    print("Loading source file: "+source_file_name)
    source_file = open(source_file_name,'r',encoding="utf-8-sig")
    source_out = {val['study_uid'].strip():val for val in DictReader(source_file)}
    print("Study Rows in Source File: "+str(len(source_out)))
    print("Loading Ambra file "+ambra_file_name)
    ambra_file = open(ambra_file_name,'r',encoding="utf-8-sig")
    ambra_out = {val['study_uid'].strip():val for val in DictReader(ambra_file)}
    print("Study Rows in Ambra File: "+str(len(ambra_out)))
    return (source_out,ambra_out)

def create_output(readers):
    # try:
    source = readers[0]
    ambra = readers[1]
    no_match_uids = list(source.keys()-ambra.keys())
    present_uids = list(source.keys()-no_match_uids)
    image_mismatches = []
    for uid in present_uids:
        if source[uid]['image_count'] != ambra[uid]['image_count']:
            a = source[uid]['image_count']
            b = ambra[uid]['image_count']
            image_mismatches.append(uid)
    print("uids missing in ambra: "+str(len(no_match_uids)))
    print("image_count mismatches: "+str(len(image_mismatches)))
    # except Exception as E:
    #     print("ERROR matching study_uids", str(E))
    #     input("")
    # try:

    output_name = filedialog.asksaveasfilename()

    if output_name == "":
        output_name ="OUTPUT.csv"
    elif '.csv'not in output_name:
        output_name=output_name+".csv"

    output_file= open(output_name,"w+",encoding="utf-8-sig",newline="",)
    output_writer  = DictWriter(output_file,fieldnames=["study_uid","status"])
    output_writer.writeheader()
    for study_uid in no_match_uids:
        output_writer.writerow({"study_uid":study_uid,"status":"missing"})
    for study_uid in image_mismatches:
        output_writer.writerow({"study_uid":study_uid,"status":'ambra image_count: {0}, source image_count: {1}'.format(ambra[study_uid]["image_count"],source[study_uid]["image_count"])})
    output_file.close()
    # except Exception in E:
    #     print("ERROR writing output file", str(E))
    #     input("")
    input(output_name+" successfully created")

# try:

root = Tk()
readers = get_reader(root)
create_output(readers)

# except Exception as E:
#     print(str(E))
#     input("")

