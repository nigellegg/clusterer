import os
from PIL import Image
from numpy import *
import hcluster


#create a list of images
imlist = []
for filename in os.listdir('./'):
    if os.path.splitext(filename)[1] == '.jpg':
        imlist.append(filename)
n = len(imlist)

#extract feature vector for each image
features = zeros((n, 3))
for i in range(n):
    im = array(Image.open(imlist[i]))
    print im
    R = mean(im[:, 0].flatten())
    G = mean(im[:, 1].flatten())
    B = mean(im[:, 2].flatten())
    features[i] = array([R, G, B])

tree = hcluster.hcluster(features)
