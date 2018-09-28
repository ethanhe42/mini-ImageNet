# create miniImageNet dataset

import os, shutil
import random as rd
rd.seed(1)

data_dir = '/home/hyh/local/imagenet/train'
dst_dir = '/home/hyh/local/miniimagenet'
minitrain = open('outputs/sourcetrain.txt', 'w')
minival = open('outputs/sourceval.txt', 'w')
minitest = open('outputs/sourcetest.txt', 'w')
imagenet_train_dir = 'train.txt'

class_list = os.listdir(data_dir)
image_dict = {}

for cls in class_list:
    cls_path = os.path.join(data_dir, cls)
    images = os.listdir(cls_path)
    images = sorted(images)
    image_dict[cls] = images

def read_csv(file_name, img_idx_dict):
    with open(file_name) as fin:
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
newf2c = {}
val_idx_dict = {}
read_csv('test.csv', val_idx_dict)

""" data copy """
try:
    os.mkdir(dst_dir)
except:
    pass
try:
    os.mkdir(os.path.join(dst_dir, 'train'))
    os.mkdir(os.path.join(dst_dir, 'val'))
    os.mkdir(os.path.join(dst_dir, 'test'))
except:
    pass
cls_idx = 0
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
        if cls not in newf2c:
            newf2c[cls] = str(cls_idx)
            cls_idx += 1
        if idx_idx >= 50:
            dst = os.path.join(dst_dir, 'train', cls, image_dict[cls][idx])
            minitrain.write(src + ' ' + newf2c[cls]+'\n')
        else:
            dst = os.path.join(dst_dir, 'val', cls, image_dict[cls][idx])
            minival.write(src + ' ' + newf2c[cls]+'\n')
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
        if cls not in newf2c:
            newf2c[cls] = str(cls_idx)
            cls_idx += 1
        minitest.write(src + ' ' + newf2c[cls]+'\n')
        print src + ' -> ' + dst
        os.symlink(src,dst)
        #shutil.copyfile(src, dst)

minitest.close()
minitrain.close()
minival.close()
