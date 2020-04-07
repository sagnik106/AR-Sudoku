from eyes import detector
import sudoku as s
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

img=cv2.imread("2.jpg")
d=detector()
a,tru = d.detect(img)
p=d.pred(a,tru)
sol=s.solver(p.reshape((9,9)).tolist())
sol = ((1-tru).reshape(9, 9)*(np.asarray(sol))).tolist()
scale = 0.09
fontScale = min(img.shape[1],img.shape[0])/(25/scale)
err = int((img.shape[0]//9)*0.17)

for j in range(9):
    for i in range(9):
        if sol[j][i]!=0:
            cv2.putText(img, str(sol[j][i]), ((i)*(img.shape[0]//9)+err, (j+1)*(img.shape[1]//9)-err), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0,0,0), 2)

plt.imshow(img)
plt.show()