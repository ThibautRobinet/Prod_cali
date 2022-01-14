import cv2
import os
import time
import numpy as np
import matplotlib.pyplot as plt

"""Voici comment je prépare une vidéo de data"""


def get_video_size(video_path):
    video = cv2.VideoCapture(video_path)
    i = 0
    ret =1
    while ret:
        i+=1
        ret, frame = video.read()
    video.release()
    return i

## Load video
def process_video(video_path,dest_folder):

    #frame_number = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) not working
    frame_number = get_video_size(video_path)
    n = (frame_number // 12) # Pour les videos a 30 fps mettre 12
    video = cv2.VideoCapture(video_path)
    #fid = open(list_file_name,"a")

    # On traite des batch de 6 frames
    for i in range(n-1):# mettre n-1 pour éviter des problèmes avec les labels, ou n mais regénérer les labels
        ## Get frame
        ret, first_frame = video.read()
        ## Resize frame
        resized = cv2.resize(first_frame, (299,299), interpolation = cv2.INTER_AREA)
        ## Covert 2 Gray
        prev_gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        flows = []
        for k in range(11):# Pour les videos a 30 fps mettre 11
            ret, frame = video.read()
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
        #dest_folder = "/Users/thibaut/Desktop/Test/a/images"

        img_path = "%s/thumb-%03d_2.jpg" % (dest_folder,1+(i*6))
        flux1_path = "%s/flux1-%03d.jpg" % (dest_folder,1+(i*6))
        flux2_path = "%s/flux2-%03d.jpg" % (dest_folder,1+(i*6))
        cv2.imwrite(img_path, resized)
        cv2.imwrite(flux1_path, im1)
        cv2.imwrite(flux2_path, im2)
        #fid.write(img_path+"#"+flux1_path+"#"+flux2_path+"\n")
    #fid.close()

def get_type(subjectID):
    type = 0
    if (subjectID >= 27):
        type = 2
    elif (subjectID >= 21):
        type = 1
    return type

## Folders
root_path = "/Users/thibaut/Desktop/Prod_cali/Dataset2"
video_folder = 'Videos_MERL_Shopping_Dataset'
labels_folder = 'Labels_MERL_Shopping_Dataset'
list_folder = 'merlTrainTestList'
image_folders = ['train','validation','test']


##Files
#label_file = 'classInd.txt';
train_file = 'trainlist01.txt' # videos 1->20
validation_file = 'validationlist01.txt' # videos 21->26
test_file = 'testlist01.txt' # videos 27->41

for subjectID in range(1,42):
    for sessionID in range(1,4):
        print("Process video :",subjectID,sessionID)
        # Check type
        type =  get_type(subjectID)
        image_folder = image_folders[type]

        # Create path
        frame_path = '%s/%s' %(root_path,image_folder)
        video_name = '%d_%d_crop'% (subjectID,sessionID)
        video_full_name = '%s/%s/%s.mp4' %(root_path,video_folder,video_name)

        # Check if video exist
        try:
            os.stat(video_full_name)
            ## Folders and file processing
            # Create video thum folder
            video_crop_folder = '%s/%s' %(frame_path,video_name)
            try:
                os.stat(video_crop_folder)
            except:
                os.mkdir(video_crop_folder)
            finally:
                list_file_name = '%s/%s/%s' %(root_path, list_folder, train_file)
                if (type == 1):
                    list_file_name = '%s/%s/%s' %(root_path, list_folder, validation_file)
                elif (type == 2):
                    list_file_name = '%s/%s/%s' %(root_path, list_folder, test_file)

                fid = open(list_file_name,"a")
                fid.write(video_name+"\n")
                fid.close()
                process_video(video_full_name,video_crop_folder)
        except:
            print("video does not exist")
