import json
import sys

try:
    
    d = ''
    with open(f'{sys.argv[1]}','r', encoding="utf-8") as f:
       d = json.load(f)
except:
    print(f"file {sys.argv[1]} not found")
    exit()

data = []
for index, i in enumerate(d['Items']):
    item = {f"{index}":[
                 {"timestamp":int(i['timestamp']['N'])},
                 {"Longitude":float(i['GPS']['M']['Longitude']['N'])},
                 {"Latitude":float(i['GPS']['M']['Latitude']['N'])},
                 {"Velocity":float(i['Vehicle']['M']['Velocity']['N'])}
                 ]}
    data.append(item)
with open(f'{sys.argv[2]}','w', encoding="utf-8") as f:  
    f.write(str({f"{sys.argv[2].split('.')[0]}":data}).replace("'", '"'))
print("done...")

    

    
    
