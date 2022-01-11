#!/usr/bin/env python
# coding: utf-8

# Copyright 2022 Mihael Simonic
# The program is distributed under the terms of the GNU General Public License 

import json
import base64
from labelme.label_file import LabelFile
from labelme import utils
from labelme import __version__
from pathlib import Path
import glob



def get_points(img_name):
    f = open(img_name+'.json')
    data = json.load(f)
    all_points = list()
    for obj in data['objects']:
        assert(len(obj['mask_vertices']) == 1)
        assert(len(obj['mask_vertices'][0]) > 0)
        assert(len(obj['labels']) == 1)
        labelme_obj = { "label": obj['labels']['label'],
                    "line_color": None,
                    "fill_color": None,
                    "points": obj['mask_vertices'][0], 
                    "shape_type": "polygon",
                    "flags": {}
                  }
        all_points.append(labelme_obj)
    return all_points


def get_image_data(img_name):
    data = LabelFile.load_image_file(img_name)
    return base64.b64encode(data).decode('utf-8')

def get_image_size(img_data):
    img_arr = utils.img_b64_to_arr(img_data)
    imageWidth = img_arr.shape[1]
    imageHeight = img_arr.shape[0]
    return imageWidth, imageHeight


def make_labelme_dict(img_name):
    return {"version": __version__,
            "flags": {},
            "shapes" : get_points(img_name),
            "lineColor": [0, 255, 0, 128], 
            "fillColor": [255, 0, 0, 128],
            "imagePath": img_name,
            "imageData": get_image_data(img_name),
            "imageHeight" : get_image_size(img_data)[1],
            "imageWidth" : get_image_size(img_data)[0]
           }


#print(json.dumps(make_labelme_dict(img_name),indent=4))


jpgFilenamesList = glob.glob('/tmp/*.jpg')


for img_name in jpgFilenamesList:
    print("Processing "+Path(img_name).stem)
    out_dict = make_labelme_dict(img_name)
    with open(Path(img_name).stem+'.json', "w") as out_file:
        json.dump(out_dict, out_file)    
