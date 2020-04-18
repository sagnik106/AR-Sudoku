import cv2
import numpy as np
import matplotlib.pyplot as plt

red=(0,0,255)

def transform(img, corners):
    rows,cols,ch = img.shape
    side=corners[3][0]-corners[0][0]
    pts1 = np.array([corners[0], corners[2],corners[1], corners[3]], dtype='float32')
    pts2 = np.array([[0, 0], [0, side-1], [side - 1, side - 1], [side-1,0]], dtype='float32')

    M = cv2.getPerspectiveTransform(pts1,pts2)

    dst = cv2.warpPerspective(img,M,(300,300))

    plt.subplot(121),plt.imshow(img),plt.title('Input')
    plt.subplot(122),plt.imshow(dst),plt.title('Output')
    plt.show()
    return dst



def filtering(coordinates):
    coordinates_new=[]
    for i in range(len(coordinates)):
        coordinates_new.append(coordinates[i][0])
    for i in range(len(coordinates_new)):
        coordinates_new[i]=np.ndarray.tolist(coordinates_new[i])
    sum_min=9999
    sum_max=0
    for i in range(len(coordinates_new)):
        sum=coordinates_new[i][0]+coordinates_new[i][1]
        if(sum_min>sum):
            sum_min=sum
            min=i
        if(sum_max<sum):
            sum_max=sum
            max=i
    lu=coordinates_new[min]
    rd=coordinates_new[max]
    #ld=[coordinates_new[min][1], coordinates_new[max][0]]
    #ru=[coordinates_new[max][1],coordinates_new[min][0]]
    max=0
    min=9999
    for i in range(len(coordinates_new)):
        if((abs(lu[1]-coordinates_new[i][1]))<=5):
            if(coordinates_new[i][0]>max):
                max=coordinates_new[i][0]
                max_ind=i
        if((abs(rd[1]-coordinates_new[i][1]))<=5):
            if(coordinates_new[i][0]<min):
                min=coordinates_new[i][0]
                min_ind=i
    ld=coordinates_new[max_ind]
    ru=coordinates_new[min_ind]
    print(lu)
    print(rd)
    print(ld)
    print(ru)
    return [lu,rd,ru,ld]
    

def get_coordinates(contours):
    
    areas=[]
    for i in range(len(contours)):
        area=cv2.contourArea(contours[i])
        areas.append(area)
    areas2=areas.copy()
    areas.sort()

    val=areas[len(areas2)-2]
    ind=areas2.index(val)

    return contours[ind]

    #return contours[1]



im = cv2.imread('scanned_im.jpg')
im=cv2.resize(im, (400,400))
im1=np.ones((len(im),len(im[1])))


imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(im1,contours,-1,0,thickness=1)

coordinates=get_coordinates(contours)
#for i in range(len(coordinates)):
#    cv2.circle(im1, (coordinates[i][0][0],coordinates[i][0][1]), 2, red, 2)
corners=filtering(coordinates)
print(corners)
for i in range(len(corners)):
    cv2.circle(im1, (corners[i][0],corners[i][1]), 2, red, 2)
img=transform(im, corners)
cv2.imshow("img",img)
cv2.waitKey(0)
img= transform(im, corners)
