from PIL import Image
import os
import os.path
import glob
import numpy as np
from torch.utils.data import Dataset
import random


class MyDataset(Dataset):
    def __init__(self, root_path, data_folder='train', name_list='ucfTrainTestlist', version=1, transform=None, num_frames=3):
        self.root_path = root_path
        self.data_folder = data_folder
        self.num_frames = num_frames
        self.random = random
        self.split_file = os.path.join(self.root_path, name_list,
                                       str(data_folder) + 'list0' + str(version) + '.txt')
        self.label_file = os.path.join(self.root_path, name_list, 'classInd.txt')
        self.label_dict = self.get_labels()

        self.images_dict, self.flux1_dict,self.flux2_dict = self.get_images_list()
        self.verify_labels()

        self.version = version
        self.transform = transform

    def get_images_list(self):
        res = [[],[],[]]
        with open(self.split_file) as fin:
            for line in list(fin):
                line = line.replace("\n", "")
                split = line.split(" ")

                video_path = split[0].split('.')[0]
                frames_path = os.path.join(self.root_path, self.data_folder, video_path)
                allfiles = glob.glob(frames_path + '/*.jpg')
                allfiles = sorted(allfiles)
                total = int(len(allfiles)/3);
                flux1 = allfiles[:total]
                flux2 = allfiles[total:2*total]
                files = allfiles[2*total:]

                # Garder une image sur 10 = Training faster
                fi = []
                fl1 = []
                fl2 = []
                for j in range(total//10):
                    fi.append(files[10*j])
                    fl1.append(files[10*j])
                    fl2.append(files[10*j])
                files = fi
                fl1 = flux1
                fl2 = flux2
                if len(files) > 0:
                    res[0] += files
                    res[1] += flux1
                    res[2] += flux2
        return res

    # Get all labels from classInd.txt
    def get_labels(self):
        label_dict = {}
        with open(self.label_file) as fin:
            for row in list(fin):
                row = row.replace("\n", "").split(" ")
                # -1 because the index of array is start from 0
                label_dict[row[0]] = int(row[1])
        return label_dict

    def verify_labels(self):
        for index in range(len(self.images_dict)):
            image = self.images_dict[index]
            # Get Label
            root_path = os.path.join(self.root_path, self.data_folder)
            path = image.replace(root_path, '')
            label_name = path[1:]
            label_index = self.label_dict[label_name]


    def __getitem__(self, index):
        image = self.images_dict[index]
        flux1 = self.flux1_dict[index]
        flux2 = self.flux2_dict[index]
        # Open images
        img = Image.open(image)
        flu1 = Image.open(flux1)
        flu2 = Image.open(flux2)

        # Get Label
        root_path = os.path.join(self.root_path, self.data_folder)
        path = image.replace(root_path, '')
        label_name = path[1:]
        label_index = self.label_dict[label_name]

        if self.transform is not None:
           img = self.transform(img)
           flu1 = self.transform(flu1)
           flu2 = self.transform(flu2)

        return (img, label_index, flu1, flu2)

    def __len__(self):
        return len(self.images_dict)

