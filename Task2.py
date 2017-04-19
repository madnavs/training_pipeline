import csv
import numpy as np
from PIL import Image
import parsing as par
from random import shuffle

def read_images(data,batch_size,start_indx,height=256,width=256,channels=1):
    # Initialize X and Y whixh corresponds to input and ground truth respectively
    X=np.zeros((batch_size,height,width,channels),dtype='uint8')
    Y = np.zeros((batch_size, height, width, channels),dtype='uint8')
    for i in range(0,batch_size):
        if (start_indx+i < data_size):
            X[i, :, :, 0] = np.asarray(par.parse_dicom_file(data[start_indx+i][0])['pixel_data'])
            Y[i,:,:,0]  = np.asarray(Image.open(data[start_indx+i][1]))
            print(start_indx+i)
    return X,Y

#read csv (http://stackoverflow.com/questions/24662571/python-import-csv-to-list)
with open('train.csv', 'rb') as f:
    reader = csv.reader(f)
    data = list(reader)

#Initialize Parameters
batch_size=8
epochs=6
data_size=len(data)

#Iterate at epoxh level and then batch level
for each_epoch in range(epochs):
   batch_indx = 0

   #shuffle data http://stackoverflow.com/questions/976882/shuffling-a-list-of-objects-in-python
   shuffle(data)

   for i in range(data_size/batch_size):
       X,Y=read_images(data,batch_size,batch_indx)
       # Given input to CNN Model Here
       batch_indx=batch_indx+batch_size

   # If data_size is not multiple of batch_size
   for i in range(batch_indx,batch_indx+data_size%batch_size):
       X,Y=read_images(data,batch_size,batch_indx)
       # Given input to CNN Model Here
       batch_indx=batch_indx+batch_size




