import shutil
import argparse
import pandas as pd
from tqdm import tqdm
import os


if __name__=="__main__":
    column_name = "File Names"

    parser = argparse.ArgumentParser(description="Copy the files in the csv to the dataset folder")

    parser.add_argument("source", help='Path of the source folder', type=str)
    parser.add_argument('dest', help="Path of the destination folder", type=str)
    parser.add_argument("csv", help="Path to the csv", type=str)

    args = parser.parse_args()

    source_dir_path = args.source
    dest_dir_path = args.dest
    csv_path = args.csv


    csv_df = pd.read_csv(csv_path)
    file_names = list(csv_df[column_name])
    print("Starting Transfer...\n")

    for file in tqdm(file_names):
        if not int(csv_df[csv_df[column_name] == file]['Status']) == 1:
            continue
        source_file = os.path.join(source_dir_path, file)
        dest_file = os.path.join(dest_dir_path, file)
        
        shutil.copyfile(source_file, dest_file)
    print("\nTransfer Successful!!")
