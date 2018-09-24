# create miniImageNet dataset

import os, shutil
import random as rd
rd.seed(1)

data_dir = '/path/to/imagenet/train'

class_list = os.listdir(data_dir)
image_dict = {}

for cls in class_list:
    cls_path = os.path.join(data_dir, cls)
    images = os.listdir(cls_path)
    images = sorted(images)
    image_dict[cls] = images

def read_csv(file_name, img_idx_dict):
    fin = open(file_name)
    dummy = fin.readline()
    while True:
        line = fin.readline()
        if line == '':
            break
        line = line[:-1].split(',')
        img, cls = line[0:2]
        img_idx = int(img[9:-4]) - 1
        if not cls in img_idx_dict:
            img_idx_dict[cls] = []
        img_idx_dict[cls].append(img_idx)

""" read train.csv """
train_idx_dict = {}
read_csv('train.csv', train_idx_dict)
read_csv('val.csv', train_idx_dict)
val_idx_dict = {}
read_csv('test.csv', val_idx_dict)

""" data copy """
dst_dir = '/path/to/miniimagenet'
for cls in train_idx_dict:
    idx_list = train_idx_dict[cls]
    rd.shuffle(idx_list)
    try:
        os.mkdir(os.path.join(dst_dir, 'train', cls))
        os.mkdir(os.path.join(dst_dir, 'val', cls))
    except:
        pass
    for idx_idx in range(len(idx_list)):
        idx = idx_list[idx_idx]
        src = os.path.join(data_dir, cls, image_dict[cls][idx])
        if idx_idx >= 50:
            dst = os.path.join(dst_dir, 'train', cls, image_dict[cls][idx])
        else:
            dst = os.path.join(dst_dir, 'val', cls, image_dict[cls][idx])
        print src + ' -> ' + dst
        os.symlink(src,dst)
        #shutil.copyfile(src, dst)

for cls in val_idx_dict:
    idx_list = val_idx_dict[cls]
    try:
        os.mkdir(os.path.join(dst_dir, 'test', cls))
    except:
        pass
    for idx in idx_list:
        src = os.path.join(data_dir, cls, image_dict[cls][idx])
        dst = os.path.join(dst_dir, 'test', cls, image_dict[cls][idx])
        print src + ' -> ' + dst
        os.symlink(src,dst)
        #shutil.copyfile(src, dst)

