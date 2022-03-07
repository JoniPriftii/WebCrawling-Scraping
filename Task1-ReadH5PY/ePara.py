import h5py
import json


outerDict = {}

with h5py.File(r'C:\Users\User\Desktop\python\AMMICAL-Miy2 (1).h5', 'r') as grupet:
    for grup in grupet:
        innerDict = {grup:[]}

        for celesGrupi in grupet[grup]:
            innerDict[grup].append({celesGrupi : list(grupet.get(grup).get(celesGrupi)[:5])})

        outerDict.update(innerDict)

with open("jason.json" , "w") as js:
    json.dump(eval(str(outerDict)), js, indent=2)
