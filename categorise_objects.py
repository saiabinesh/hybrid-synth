import os
import re
from shutil import copyfile
from shutil import move
import random
import json
with open('Dict_objects.txt') as handle:
    new_dict = json.loads(handle.read())
a=os.scandir("Images")
base_dir="train"
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

counter=1
for file in a:
	# print(file.name)
	text = file
	m = re.search('e_(.*).png', text.name)
	number = int(m.group(1))
# if not number%42 in [19,20,21,12,14,16,17,32,34,35,36,38,39,40,41,42]:
	i, d = divmod((number%650)-1, 10)
	folder=new_dict[str((i+1)%65)]
	full_dir=os.path.join(base_dir,folder)
	if not os.path.exists(full_dir):
		os.makedirs(full_dir)
	move(file.path, os.path.join(full_dir,file.name))
	# print(file.name, counter)
	if counter%100==0:
		print(counter)
	counter+=1
		
a=os.scandir("train")
base_dir="val"
val_images_counter=1
for folder in a:
    print(folder.name)
    images=[x for x in os.scandir(folder.path)]
    number_of_val_images=int(len(images)/10)
    val_images_counter+=number_of_val_images
    random_image_set=[x for x in random.sample(images,number_of_val_images)]
    print(len(images))
    for file in random_image_set:
        full_dir=os.path.join(base_dir,folder.name)
        if not os.path.exists(full_dir):
            os.makedirs(full_dir)
        move(file.path, os.path.join(full_dir,file.name))
    # print("moved: ", file.name)

