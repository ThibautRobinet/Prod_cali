import cv2
import os
import time
import numpy as np


## Initialisation
f2p_path = '/mnt/Commands/file2process.txt'
f2e_path = '/mnt/Commands/file2eval.txt'
#f2p_path = '/Users/thibaut/Desktop/Test/file2process.txt'# Pour tester
#f2e_path = '/Users/thibaut/Desktop/Test/file2eval.txt'# Pour tester
sleep_time = 10

def get_video_size(video_path):
    video = cv2.VideoCapture(video_path)
    i = 0
    ret =1
    while ret:
        i+=1
        ret, _ = video.read()
    video.release()
    return i

def get_information():
    fid = open(f2p_path,"r")
    rows = []
    for row in list(fid):
        rows.append(row.replace("\n",""))
    fid.close()
    return rows

def delete_processed_lines(rows):
    fid = open(f2p_path,"w")
    for number, line in enumerate(rows):
        if number > 2:
            fid.write(line+"\n")
    fid.close()

def ask2predict(dest_folder,list_img_name,res_folder):
    print(dest_folder,list_img_name,res_folder)
    fid = open(f2e_path,"a")
    fid.write(dest_folder+"/"+list_img_name+"\n")
    fid.write(dest_folder+"\n")
    fid.write(res_folder+"\n")
    fid.close()
        
def pre_process(rows):
    print(rows)
    video_path = rows[0]# Pour trouver la vidéo
    dest_folder = rows[1]# Où sauvegarder les images pré-traitée
    res_folder = rows[2]# Le dossier où se trouvent les fichiers de commandes
    list_img_name = 'list_img.txt'
    try:
        os.stat(video_path)
    except:
        print("video does not exist")
        exit()
    try:
        os.stat(dest_folder)
    except:
        os.mkdir(dest_folder)

    frame_number = get_video_size(video_path)
    n = (frame_number // 12) # Pour les videos a 30 fps mettre 12
    print(n)
    video = cv2.VideoCapture(video_path)

    fid = open(dest_folder+"/"+list_img_name,"a")

    ## On traite des batch de 6 frames
    for i in range(n):
        _, first_frame = video.read()# Get frame
        resized = cv2.resize(first_frame, (299,299), interpolation = cv2.INTER_AREA)# Resize frame
        prev_gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)# Covert 2 Gray
        flows = []
        for k in range(11):# Pour les videos a 30 fps mettre 11
            _, frame = video.read()
            if (k %4 ==0): # Pour les videos a 30 fps mettre 4
                frame_r = cv2.resize(frame, (299,299), interpolation = cv2.INTER_AREA)
                gray = cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY)
                flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
                prev_gray = gray
                flows.append(flow)

        ## Create Images
        im1 = 128*np.ones((299, 299, 3))
        im2 = 128*np.ones((299, 299, 3))
        im1[:,:,:2] += flows[0]
        im1[:,:,2] += flows[1][:,:,0]
        im2[:,:,0] += flows[1][:,:,1]
        im2[:,:,1:] += flows[2]

        im1 = np.round(im1)
        im2 = np.round(im2)

        ## Save images
        frame_path = "%s/thumb-%03d_2.jpg" % (dest_folder,1+(i*6))
        flux1_path = "%s/flux1-%03d.jpg" % (dest_folder,1+(i*6))
        flux2_path = "%s/flux2-%03d.jpg" % (dest_folder,1+(i*6))
        cv2.imwrite(frame_path, resized)
        cv2.imwrite(flux1_path, im1)
        cv2.imwrite(flux2_path, im2)

        ## Save frames name
        fid.write(frame_path+"\n")
    fid.close()
    ask2predict(dest_folder,list_img_name,res_folder)
    delete_processed_lines(rows)
    
while True:
    try:
        os.stat(f2p_path)
    except:
        time.sleep(sleep_time)
    else :
        rows = get_information()
        if (len(rows) < 1):
            time.sleep(sleep_time)
        else:
            pre_process(rows)


