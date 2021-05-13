import json
import csv

'''
This is a utility function that makes a json that is later used in the automate_selection script
Converts a csv with a head column and a lot of other columns into a json file with the head column value as the label and the other column values as an array to the json label.
'''


path_to_csv = r"C:\Users\HARSH\Downloads\classification\label_updated.csv"
path_to_json = r"C:\Users\HARSH\Downloads\classification\labels.json"


js = dict()
with open(path_to_csv, "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        categoryList = []
        for cat in row:
            if cat == '':
                continue
            categoryList.append(cat)
        categoryHeader = categoryList[0]
        categoryList.pop(0)
        js[categoryHeader] = categoryList


with open(path_to_json, "w") as outfile: 
    json.dump(js, outfile)