# Keyframe-Extraction
A collection of different algorithms to extract keyframes from a video

## [i-th frame](ithFrame.py)
+ An algorithm that finds every i-th frame in a video and saves it in a folder
+ it also makes an analytics csv that stores the number of keyframes collected and the time taken to find those keyframes

## [Convert To JSON](convert_to_json.py)
+ This is a utility function that makes a json that is later used in the automate_selection script
+ Converts a csv with a head column and a lot of other columns into a json file with the head column value as the label and the other column values as an array to the json label.

## [Make Class](makeClassCsv.py)
+ This is a utility function (used by automate_selection) which is used to make a csv of the list of the videos in a video directory this script parses each video in file in a directory and then marks it 

+ -1 => not yet processed
+ 0 => processed required class not found
+ 1 => processed and required class found

+ To run this just provide the path of the directory that contains all the videos this script will generate the required csv file at the basename of the folder provided. 

## [Automate Selection](automate_selection.py)
+ Take a csv list of the images with the names and  a col for checking if the file has already processed or not -1(for not visited), 0(for not selected), 1(for selected)
+ now iterate through all the files and check if the col is -1 then find the keyframes and then use the classify algo to find the object in the image if found then transfer it to another final file
+ update the files and then save them to the folder
+ now transfer the files to the new location


    Note -> The name of the label is taken to be as the base name of the csv file

## [Select Files](select_files.py)
+ Select the files and copies into a new folder from the video folder that have the image of the required using the csv that is created using automate_selction script

## [Download Videos](download_videos.py)
+ This script downloads videos of the directed class from the howto100m dataset
+ This creates a text file that contains all the links associated to the files that contain the specific class
+ Then use the command below to download all the videos from the links that were added to the file
<br/>
```
    wget --user htlog23 --password fb93dc3b1950d18 -i filename.txt
```