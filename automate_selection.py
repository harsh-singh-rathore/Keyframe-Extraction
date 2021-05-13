import os
import argparse
from os.path import basename
import pandas as pd
from pandas.core.indexes import base
from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter
from tqdm import tqdm
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16
import json

"""
Pipeline
    + take a csv list of the images with the names and  a col for checking if the file has already processed or not -1(for not visited), 0(for not selected), 1(for selected)
    + now iterate through all the files and check if the col is -1 then find the keyframes and then use the classify algo to find the object in the image if found then transfer it to another final file
    + update the files and then save them to the folder
    + now transfer the files to the new location

Note -> The name of the label is taken to be as the base name of the csv file
"""

# load the model
model = VGG16()
# path of the json file that conatins the labels for each class
path_to_json = r'/content/drive/MyDrive/Chetan Sharma sir Keyframe/Datsets/labels.json'
no_of_keyframes = 50

def findKeyframes(file_path: str, opdir: str, no_of_frames: int):
    '''
    Finds the keyframe using katna
    file_path -> path to the file whose keyframes needs to be found
    opdir -> path to the path where output needs to be delivered
    no_of_frames -> the number of frames required from the video file
    '''
    if not os.path.exists(file_path):
        raise Exception(f"File {file_path} does not exist")
    if not os.path.exists(opdir):
        raise Exception(f"Directory {opdir} does not exist")
    
    file_name = os.path.basename(file_path)
    keyframe_dir = os.path.join(opdir, file_name)

    os.mkdir(keyframe_dir)

    try:
        vd = Video()
        diskwriter = KeyFrameDiskWriter(location= keyframe_dir)


        vd.extract_video_keyframes(
        no_of_frames = no_of_frames, 
        file_path = file_path,
        writer = diskwriter
        )
    except Exception as e:
        print(e)


def classify(file: str):
    '''
    Classifies the image provided using vgg16
    file -> paht to the file that needs to be classified using the algo
    return
    label -> label of the file that it got classified into
    '''

    # example of using a pre-trained model as a classifier
    image = load_img(file, target_size=(224, 224))
    # convert the image pixels to a numpy array
    image = img_to_array(image)
    # reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # prepare the image for the VGG model
    image = preprocess_input(image)
   
    # predict the probability across all output classes
    yhat = model.predict(image)
    # convert the probabilities to class labels
    label = decode_predictions(yhat)
    # retrieve the most likely result, e.g. highest probability
    label = label[0][0]
    
    
    return label[1]




if __name__=="__main__":
    with open(path_to_json) as f:
        all_label = json.load(f)
    
    column_name = "File Names"

    parser = argparse.ArgumentParser(description='Process the images')
    
    parser.add_argument('csv', type=str, help='Path to the csv file')
    parser.add_argument('vpath', type=str, help="Path to video folder")
    parser.add_argument('-p', '--path', type=str, help="Path to save the keyframes")

    args = parser.parse_args()

    path_to_csv = args.csv
    video_path = args.vpath
    path_to_keyframes = os.path.join('/content/', os.path.basename(video_path))
    
    if not os.path.exists(path_to_csv):
        raise Exception("CSV file was not found")

    if args.path:
        path_to_keyframes = args.path
    
    class_name = os.path.basename(path_to_csv).split(".")[0]
    
    class_keyframe_dir = os.path.join(path_to_keyframes, class_name)

    if not os.path.exists(class_keyframe_dir):
        os.mkdir(class_keyframe_dir)

    label_df = pd.read_csv(path_to_csv)
    file_list = label_df[column_name]

    for file in tqdm(file_list):
        # checks if the status of the file is processed or not if it is not then the program moves ahead 
        # if the file is already processed => status is 0/1 the file is skipped
        if int(label_df[label_df[column_name]==file]['Status']) != -1:
            continue
        # now keyframe of the file is found using katna
        ipfile = os.path.join(video_path, file)

        findKeyframes(ipfile, path_to_keyframes, no_of_keyframes)

        # sets the path to the keyframes of the video file 
        keyframe_images = os.path.join(path_to_keyframes, file)
        

        # each of the keyframes is sent to classify if any of the images is classified into the required class which is the basename of the video directory then the status is set to 1 rest of the images are skipped and csv is updated.
        # otherwise is after parsing through all the files if no class is found then status is set to 0 and the csv is updated
        for keyframe in os.listdir(keyframe_images):
            label = classify(os.path.join(keyframe_images, keyframe))
            if label in all_label[class_name]:
                label_df.loc[label_df[column_name]==file, 'Status'] = 1
                break
        if int(label_df[label_df[column_name] == file]['Status']) == -1:
            label_df.loc[label_df[column_name]==file, 'Status'] = 0
        label_df.to_csv(path_to_csv, index=False)
        label_df = pd.read_csv(path_to_csv)