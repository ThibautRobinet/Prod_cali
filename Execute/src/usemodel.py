from __future__ import print_function
import os
import os.path
import time
import torch.backends.cudnn as cudnn
import torch.nn as nn
import torch.nn.parallel
import torch.optim as optim
import torch.utils.data as data
from inceptionv4 import inceptionv4
from utils import check_gpu, accuracy
from visualize import Visualizer
from torchvision.transforms import *
from PIL import Image

class UseModel(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

        self.num_classes = 6
        self.name_list = 'merlTrainTestList'
        self.model_type  = 'inceptionv4'
        self.data_set = 'merl'
        self.pretrained = False
        self.lr = 0.01
        self.momentum = 0.9
        self.weight_decay = 1e-4
        self.normalize = Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        self.transform = Compose([
                Resize(341),
                CenterCrop(299),
                ToTensor(),
                self.normalize
            ])

        self.best_prec1 = 0
        self.start_epoch = 0
        self.checkDataFolder()
        self.loading_model()

    def checkDataFolder(self):
        try:
            os.stat('./' + self.model_type + '_' + self.data_set)
        except:
            os.mkdir('./' + self.model_type + '_' + self.data_set)
        self.data_folder = './' + self.model_type + '_' + self.data_set

    def loading_model(self):
        print('Loading %s model' % (self.model_type))
        pretrained = None
        if self.pretrained:
            pretrained = 'imagenet'
        if self.model_type == 'inceptionv4':
            self.model = inceptionv4(num_classes=1000, pretrained=pretrained)
            if self.pretrained:
                num_ftrs = self.model.last_linear.in_features
                self.model.last_linear = nn.Linear(num_ftrs, self.num_classes)
                # free all layers:
                for i, param in self.model.named_parameters():
                    param.requires_grad = False
                # unfreeze last layers:
                ct = []
                for name, child in self.model.features.named_children():
                    if "4" in ct:
                        for param in child.parameters():
                            param.requires_grad = True
                    ct.append(name)
            else:
                num_ftrs = self.model.last_linear.in_features
                self.model.last_linear = nn.Linear(num_ftrs, self.num_classes)
        else:
            print('no model')
            exit()

        # define loss function (criterion) and optimizer
        self.criterion = nn.CrossEntropyLoss()

        params = list(filter(lambda p: p.requires_grad, self.model.parameters()))
        self.optimizer = optim.SGD(params=params, lr=self.lr, momentum=self.momentum, weight_decay=self.weight_decay)

        file = os.path.join(self.data_folder, 'model_best.pth.tar')
        if os.path.isfile(file):
            print("=> loading checkpoint '{}'".format('model_best.pth.tar'))

            checkpoint = torch.load(file)
            self.start_epoch = checkpoint['epoch']
            self.best_prec1 = checkpoint['best_prec1']
            self.model.load_state_dict(checkpoint['state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer'])
            print("=> loaded best model")
        else:
            print("=> no model best found at ")
            exit()
        cudnn.benchmark = True

    def process(self, images):
        # switch to evaluate mode
        self.model.eval()

        images = torch.autograd.Variable(images)
        output_batch = self.model(images)
        return output_batch

    def select(self,path):
        img = Image.open(path)
        if self.transform is not None:
            img = self.transform(img)
        return img




