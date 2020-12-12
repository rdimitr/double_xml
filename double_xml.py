#
# Анализ дубликатов UID в XML файлах DICOM Carl Zeiss
#

from xml.dom import minidom
import os
import collections

OUT_FILE_NAME = "uid_list.csv"
OUT_HEADER = "STUDY_UID#SERIES_UID#SOP_UID\n"
OUT_HEADER_UID = "UID#COUNT_RECORDS\n"
ERR_MESSAGE = "Error"

uids_list = [[],[],[]]

uid_files = ["uid_study_dbl.csv", "uid_series_dbl.csv", "uid_sop_dbl.csv"]

def uidcounter():
    for i in range(len(uid_files)):
        fout = open(uid_files[i], 'w')
        fout.write(OUT_HEADER_UID) 
        cnt = collections.Counter(uids_list[i])
        for key, value in cnt.items():
            if value >= 2:
               fout.write(f"{key}#{value}\n")
        fout.close()



def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) and file.endswith(".xml"):
            yield file


def main():
    csvout = open(OUT_FILE_NAME, 'w')
    csvout.write(OUT_HEADER)
    
    for file in files("."):  
        try:
           doc = minidom.parse(file)
           study_instance_uid = doc.getElementsByTagName("emr:study_instance_uid")[0].firstChild.data
           series_instance_uid = doc.getElementsByTagName("emr:series_instance_uid")[0].firstChild.data
           sop_instance_uid = doc.getElementsByTagName("emr:sop_instance_uid")[0].firstChild.data
           res = f"{study_instance_uid}#{series_instance_uid}#{sop_instance_uid}\n"
           csvout.write(res)
           
           uids_list[0].append(study_instance_uid)
           uids_list[1].append(series_instance_uid)
           uids_list[2].append(sop_instance_uid)
           
        except Exception:
           pass 

    csvout.close()
    uidcounter()

if __name__ == "__main__":
    main()