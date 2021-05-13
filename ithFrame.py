import os
import cv2 as cv
import time
import pandas as pd
from tqdm import tqdm


className = "horses"
number_of_keyframes = 20
outPutDir = f'/content/Keyframes/'
videoDir = "/content"
analyticsDir = "/content/drive/MyDrive/Chetan Sharma sir Keyframe/Analytics"


def makeAnalyticsFile(className: str, analyticsDir: str):
    # making of the analysis csv
    df = pd.DataFrame([["Average Time for the class", 0.0, 0, 0, 0]], columns=["File Name", "Time in seconds", "i value", "Total frames", "Total Keyframes"])
    df.to_csv(os.path.join(analyticsDir, className+"iframe.csv"), index=False)

def iFrame(i : int, outPutPath: str, inPutPath: str, filename: str):
    '''
    i -> the ith frame value which needs to be extracted
    outPutPath -> the output path where the keyframe needs to be saved
    filename -> the fileName of the file whose keyframe is to be extracted
    '''
    if inPutPath.endswith(".mp4"):
        vidcap = cv.VideoCapture(inPutPath)
        count = 0
        iframe = 0

        while True:
            success, image = vidcap.read()
            if not success:
                break
            if iframe%i == 0:
                path = os.path.join(outPutPath, filename + "_{:d}.jpg".format(count))
                #print(path)
                cv.imwrite(path, image)     # save frame as JPEG file
                count += 1


            iframe += 1
        return iframe, count
    else:
        return 0

        
def findKeyframes(videoDir: str, outPutDir: str, analyticsDir: str, className: str, numberOfFrames: int):
    # defining the input and output folders
    directory_op = os.path.join(outPutDir, className, 'iframe')
    directory_ip = os.path.join(videoDir, className)

    # iterating through all the files in input directory
    for fil in tqdm(os.listdir(directory_ip)):

        start = time.time() # for calculating executing time

        videos_file_path = os.path.join(directory_ip, fil)
        keyframe_output_directory =  os.path.join(directory_op, fil)

        if not os.path.isdir(keyframe_output_directory):
            os.mkdir(keyframe_output_directory)

        try:
            total, count = iFrame(numberOfFrames, keyframe_output_directory, videos_file_path, fil.split(".")[0])
        except Exception as e:
            print(e)

        end = time.time() # end time calculation

        # collecting the analytics
        df = pd.read_csv(os.path.join(analyticsDir, className+"iframe.csv"))
        ndf = pd.DataFrame([[fil, end-start, numberOfFrames, total, count]], columns=["File Name", "Time in seconds", "i value", "Total frames", "Total Keyframes"])
        df = df.append(ndf)
        df.to_csv(os.path.join(analyticsDir, className+"iframe.csv"), index=False)


if __name__ == '__main__':
    makeAnalyticsFile(className, analyticsDir)
    findKeyframes(videoDir = videoDir, outPutDir = outPutDir, analyticsDir = analyticsDir, className = className, numberOfFrames = number_of_keyframes)
