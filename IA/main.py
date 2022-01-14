from __future__ import print_function
from os import*
chdir('/Users/thibaut/Desktop/Prod_cali/IA')
import argparse
from train import Training
from test import Testing
DIR = '/Users/thibaut/Desktop/Prod_Cali/Dataset2/merlTrainTestList'
resume_ = '/Users/thibaut/Desktop/Prod_cali/IA/inceptionv4_merl/checkpoint.pth.tar'
parser = argparse.ArgumentParser(description='PyTorch Pseudo-3D fine-tuning')
parser.add_argument('--data', default='/Users/thibaut/Desktop/Prod_Cali/Dataset2', metavar='DIR', help='path to dataset')
parser.add_argument('--data-set', default='merl', const='merl', nargs='?', choices=['UCF101', 'Breakfast', 'merl'])
parser.add_argument('--workers', default=0, type=int, metavar='N', help='number of data loading workers (default: 4)')
parser.add_argument('--early-stop', default=10, type=int, metavar='N', help='number of early stopping')
parser.add_argument('--epochs', default=2, type=int, metavar='N', help='number of total epochs to run')
parser.add_argument('--start-epoch', default=0, type=int, metavar='N', help='manual epoch number (useful on restarts)')
parser.add_argument('-b', '--batch-size', default=16, type=int, metavar='N', help='mini-batch size (default: 256)')
parser.add_argument('--lr', '--learning-rate', default=1e-2, type=float, metavar='LR', help='initial learning rate')
parser.add_argument('--momentum', default=0.9, type=float, metavar='M', help='momentum')
parser.add_argument('--dropout', default=0.9, type=float, metavar='M', help='dropout')
parser.add_argument('--weight-decay', default=1e-4, type=float, metavar='W', help='weight decay')
parser.add_argument('--print-freq', default=1, type=int, metavar='N', help='print frequency')
parser.add_argument('--resume', default='', type=str, metavar='PATH', help='path to latest checkpoint')
parser.add_argument('--evaluate', dest='evaluate', action='store_true', help='evaluate model on validation set')
parser.add_argument('--test', dest='test', action='store_true', help='evaluate model on test set')
parser.add_argument('--pretrained', dest='pretrained', action='store_true', help='use pre-trained model')
parser.add_argument('--model-type', default='inceptionv4', nargs='?', choices=['inceptionv4', 'iresetv2'],
                    help="which model to run the code")
parser.add_argument('--log-visualize', default='./runs', type=str, metavar='PATH', help='tensorboard log')
parser.add_argument('--ten-crop', dest='tencrop', action='store_true', help='use ten-crop for test data')


def main():
    args = parser.parse_args()
    args = vars(args)

    print('Merl data set')
    num_classes = 6
    name_list = 'merlTrainTestList'

    Testing(name_list=name_list, num_classes=num_classes, modality='RGB', **args)
    #Training(name_list=name_list, num_classes=num_classes, modality='RGB', **args)


if __name__ == '__main__':
    main()
