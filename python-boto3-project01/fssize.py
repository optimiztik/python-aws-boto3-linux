import shutil
import socket
import csv
from datetime import datetime,date


# Function to crete and write to a file
def writeToCsvFile(data):
    #print header to the csv file.
    csvOutputFile = open("/data/csvoutput.csv",'a',newline='')
    headerfield = ['Date','Time','Hostname','IpAddress','Path','PercentageFree']
    writer = csv.DictWriter(csvOutputFile,fieldnames=headerfield)
    if csvOutputFile.tell() == 0:
        writer.writeheader()
    writer.writerow(data)

#Script to generate data for fs usage
fsusage = {}
today = date.today()
todaydateformat = today.strftime("%d/%m/%Y")
displaytime = datetime.now().time().strftime('%H:%M:%S')
path="/"
hostname = socket.gethostname()
ipaddr = socket.gethostbyname(hostname)

stat = shutil.disk_usage(path)
pctfree = int((stat.free/stat.total)*100)

dict_fsusage = {
        "Date":todaydateformat,
        "Time":displaytime,
        "Hostname":hostname,
        "IpAddress":ipaddr,
        "Path":path,
        "PercentageFree":pctfree
        }
writeToCsvFile(dict_fsusage)
