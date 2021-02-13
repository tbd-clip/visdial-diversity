#!/usr/bin/env python
# coding: utf-8

# In[1]:

from glob import glob
import json
from os import path
import os
# This script assumes you are running from either of the repos
# root directory and have the coco dataset downloaded in a folder
# called coco within the same folder as the repo. The file structure
# of the dataset should be as follows:

# Please dont forget to set the global environ variable.
# export COCO_IMG_DIR='/hatti/code/nlp2021winter/datasets/coco_imgs'
# coco_imgs
# |---test2014
# |    |---000001.jpg
# |    |---000002.jpg
# |---train2014
# |---val2014


# In[7]:

jsonObject = {"images": []}
assert os.getenv('COCO_IMG_DIR') is not None, "Please set the global environ variable for COCO_IMG_DIR"
image_dir = path.join(os.getenv('COCO_IMG_DIR'))


# In[8]:


for splitPath in glob(image_dir + "*[!.zip]"):
    print(splitPath)
    for imagePath in glob(splitPath + "/*"):
        imagePath = imagePath.split("/")

        # set split var depending on folder name containing images
        split_dir_name, image_id= imagePath[-2], path.splitext(imagePath[-1])[0]
        split_tag_map = {"train2014":"train", "val2014":"val", "test2014":"test"}
        split_tag = split_tag_map[split_dir_name]

        # recreate path to image without the first "."
        filePath = '/'.join(imagePath[1:])

        # Add vars to a new JSON and append to images list
        jsonObject["images"].append({"id": image_id, "split": split_tag, "file_path": filePath})

# In[ ]:
with open('coco.json', 'w') as outfile:
    json.dump(jsonObject, outfile)

