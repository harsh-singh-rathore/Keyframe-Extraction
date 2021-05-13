import pandas as pd
import os
import pandas as pd
from tqdm import tqdm

'''
This is a utility function (used by automate_selection) which is used to make a csv of the list of the videos in a video directory this script parses each video in file in a directory and then marks it -1 => not yet processed

0 => processed required class not found
1 => processed and required class found


to run this just provide the path of the directory that contains all the videos this script will generate the required csv file at the basename of the folder provided. 
'''


path = "/content/rabbit"


fileNames = []

for file in tqdm(os.listdir(path)):
  fileNames.append(file)

df = pd.DataFrame()
df["File Names"] = fileNames
df["Status"] = -1
df.to_csv(os.path.basename(path)+".csv", index=False)