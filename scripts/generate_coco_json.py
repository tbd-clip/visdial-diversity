from glob import glob
import json

# This script assumes you are running from either of the repos
# root directory and have the coco dataset downloaded in a folder
# called coco within the same folder as the repo. The file structure
# of the dataset should be as follows:

# coco
# |---images
# |    |---test2014
# |    |    |---000001.jpg
# |    |    |---000002.jpg
# |    |---train2014
# |    |---val2014

jsonObject = {"images": []}

# Only select extracted folders from zips files
for splitPath in glob("./coco/images/*[!.zip]"):  
	for imagePath in glob(splitPath + "/*"):
		imagePath = imagePath.split("/")
		# set split var depending on folder name containing images
		if imagePath[3] == "train2014":
			split = "train"
		elif imagePath[3] == "val2014":
			split = "val"
		elif imagePath[3] == "test2014":
			split = "test"
        # image ID is the same as the image name
		id = int(imagePath[4][:-4])  
        # recreate path to image without the first "."
		filePath = '/'.join(imagePath[1:]) 
        # Add vars to a new JSON and append to images list
		jsonObject["images"].append({"id": id, "split": split, "file_path": filePath}) 

with open('coco.json', 'w') as outfile:
	json.dump(jsonObject, outfile)