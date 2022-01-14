import torch
import torch.nn as nn

# get accuracy from y pred
def accuracy(y_pred, y_actual, topk=(1,)):
    """Computes the precision@k for the specified values of k"""
    maxk = max(topk)
    batch_size = y_actual.size(0)

    _, pred = y_pred.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(y_actual.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[k-1].view(-1).float().sum()
        res.append(correct_k.mul_(100.0 / batch_size))

    return res


def check_gpu():
    num_gpus = 0
    if torch.cuda.is_available():
        num_gpus = torch.cuda.device_count()
    return num_gpus

def get_learning_rate(optimizer):
    lr = []
    for param_group in optimizer.param_groups:
        lr += [param_group['lr']]
    return lr

