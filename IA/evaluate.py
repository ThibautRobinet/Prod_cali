import os
os.chdir('/Users/thibaut/Desktop/Projet_Cali/examples/pytorch-inception-master')
from usemodel import UseModel
import torch
import numpy as np



## Initialisation
video_path = '/Users/thibaut/Desktop/Test/a.mp4'
dest_folder = '/Users/thibaut/Desktop/Test/images'
file_path = '/Users/thibaut/Desktop/Test/images' + '/list_img.txt'
result_path = '/Users/thibaut/Desktop/Test/images' + '/results.txt'

## Load model
model = UseModel()

## Read list of images file
print("Loading Data")
fid = open(file_path,"r")
images, names = [], []
for row in list(fid):
    row  = row.replace("\n",'')
    image = model.select(row)
    image = image[None, :]
    images.append(image)
    row = row.split("/")[-1]
    names.append(row)
fid.close()

## Arrange data
I = images[0];
for k in range(1,len(images)):
    I = torch.cat((I,images[k]), 0)
print(I.size())

## Evaluate data
print("Evaluate data")
output = model.process(I)
result = output.tolist()
round_result = np.around(np.array(result),4).tolist()

## Save result
print("Save result")
fid = open(result_path,"a")
for k in range(0,len(names)):
    max_val = max(result[k])
    label = result[k].index(max_val) + 1 # + 1 Car les classes vont de 1 à 6 avec 6 aucune action
    fid.write(names[k]+" "+str(label)+"\n")
    #fid.write(names[k]+" "+str(round_result[k])+"\n")# To save all probas
fid.close()

print("Done")
