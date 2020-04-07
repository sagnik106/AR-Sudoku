import cv2
from tensorflow.keras.models import load_model
import numpy as np
import math
import matplotlib.pyplot as plt

class detector:
    def __init__(self, model_name='cnn.h5'):
        self.model=load_model(model_name)
    def detect(self, img):
        if len(img.shape)==3:
            img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _,img=cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        self.h, self.w = img.shape
        self.n = list()
        for i in range(0, self.h-(self.h//9),self.h//9):
            for j in range(0, self.w-(self.w//9), self.w//9):
                self.cell=img[i:i+self.h//9, j:j+self.w//9]
                self.cell=cv2.resize(self.cell,(32,32))
                self.cell=self.cell[2:30,2:30]
                self.cell=self.cell.reshape((28*28))
                self.n.append(self.cell)
        self.n=1-(np.asarray(self.n)/255.0)
        self.l=list()
        for t in range(0,81):
            self.avg=sum(self.n[t])/(28*28)
            if (float(self.avg)*255)>15:
                self.l.append(1)
            else:
                self.l.append(0)
        return self.n, np.asarray(self.l)
    def pred(self, c, v=np.ones(81)):
        return np.argmax(self.model.predict(c), axis=-1)*v
    def disp(self, cells):
        for self.t in range(1,82):
            plt.subplot(9,9,self.t)
            plt.imshow(cells[self.t-1].reshape((28,28)))
        plt.show()
    def compiled(self, img):
        self.a, self.tru=self.detect(img)
        return self.pred(self.a, self.tru)
        

"""
d=detector()
im=cv2.imread("1.jpg",0)
import time
t=time.time()
p=d.compiled(im)
print(time.time()-t)
print(p.reshape(9,9))"""
