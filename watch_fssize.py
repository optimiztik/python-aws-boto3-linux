import pandas as pd
from autoextend import modify_instance_volsize 
def watch_fssize():

    data = pd.read_csv("/data/csvoutput.csv")
    if data['PercentageFree'].iloc[-1] > 60:
        modify_instance_volsize()
