import json
import os
from tqdm import tqdm

def clean_bbox(train_folder_path):
    # Iterate over each file in the train folder
    for filename in tqdm(os.listdir(train_folder_path)):
        if filename.endswith('.json'):
            file_path = os.path.join(train_folder_path, filename)
            
            # Read and load JSON data from the file
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Filter out shapes with a shape_type of 'rectangle' or label 'latSacrum'
            data['shapes'] = [shape for shape in data['shapes'] if shape['shape_type'] != 'rectangle' and shape['label'] != "latSacrum"]

            # Write the modified data back to the file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

    print("All JSON files in the train folder have been updated.")

if __name__ == '__main__':
    clean_bbox('../dataset/train')
    clean_bbox('../dataset/test')