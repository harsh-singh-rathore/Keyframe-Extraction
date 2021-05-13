import os
import json
import pandas as pd


'''
For downloading files from the howto100m dataset

Takes in the count_label csv which contains the label and the number of videos in the server and then makes a txt file which contains the links to the videos of the specific files.
'''

base_dir = r"C:\Users\HARSH\Downloads\classification\videos"
class_name = 'Rabbits'
label_count_path = 'count_label.csv'
video_id_json = 'video_id_labels.json'

label_counts = pd.read_csv(label_count_path)
vid_ids = {}

with open(video_id_json, 'r') as file:
    vid_ids = json.load(file)


save_to = os.path.join(base_dir, class_name)

os.mkdir(save_to)

print(int(label_counts.loc[label_counts.Labels == class_name, 'Counts']) == len(vid_ids[class_name]))

vid_ids = vid_ids[class_name]
vid_ids = vid_ids[0:1150]
with open(save_to+'/'+class_name+'.txt', 'w') as w_file:
    for vid_id in vid_ids:
        url = 'http://howto100m.inria.fr/dataset/' + vid_id + '.mp4'
        print(url, file=w_file)