import os
#os.chdir('/Users/thibaut/Desktop/Projet_Cali/CALIA/IA/Execute/src')# Pour tester
from usemodel import UseModel
import torch
import numpy as np
import time

## Load model
model = UseModel()
batch_size = 16
sleep_time = 10

## Initialisation
f2e_path = '/mnt/Commands/file2eval.txt'
#f2e_path = '/Users/thibaut/Desktop/Test/file2eval.txt'# Pour tester
def get_information():
    fid = open(f2e_path,"r")
    rows = []
    for row in list(fid):
        rows.append(row.replace("\n",""))
    fid.close()
    return rows

def delete_processed_lines(rows):
    fid = open(f2e_path,"w")
    for number, line in enumerate(rows):
        if number > 2:
            fid.write(line+"\n")
    fid.close()


def eval(rows):
    ## Init paths
    file_path = rows[0]
    dest_folder = rows[1]
    dest_result_folder = rows[2]
    result_path = dest_result_folder + '.json'
    #try:
    #    os.stat(dest_result_folder)
    #except:
    #    os.mkdir(dest_result_folder)

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

    start = 0
    ## Arrange data
    if (len(images)>0):
        fid = open(result_path,"a")
        fid.write('{"result":{"frames":[')
        for l in range(((len(images)-1)//batch_size)+1):
            print('New batch ', start,len(images) )
            I = images[start]
            for k in range(1,batch_size):
                if (start+k < len(images)):
                    I = torch.cat((I,images[start+k]), 0)
            print(I.size())

            ## Evaluate data
            print("Evaluate data")
            output = model.process(I)
            result = output.tolist()
            round_result = np.around(np.array(result),4).tolist()

            ## Save result
            print("Save result")
            for k in range(0,batch_size):
                if (start+k < len(images)):
                    if k+start > 0 :
                        fid.write(',')
                    max_val = max(result[k])
                    label = result[k].index(max_val) + 1 # + 1 Car les classes vont de 1 à 6 avec 6 aucune action
                    #fid.write(names[start+k]+" "+str(label)+"\n")
                    #fid.write(names[k]+" "+str(round_result[k])+" "+str(label)+"\n")# To save all probas
                    fid.write('{"frameID":'+str(k+start)+',"label":'+str(label)+',"probas":{')
                    for i in range(5):
                        fid.write('"'+str(i+1)+'":'+str(round_result[k][i])+",")
                    fid.write('"'+str(0)+'":'+str(round_result[k][5])+"}}")
            start += batch_size
        fid.write(']}}')
        fid.close()
        ## delete 3 first lines
        delete_processed_lines(rows)
        print("Done")

while True:
    try:
        os.stat(f2e_path)
    except:
        time.sleep(sleep_time)
    else :
        rows = get_information()
        if (len(rows) < 1):
            time.sleep(sleep_time)
        else:
            eval(rows)
