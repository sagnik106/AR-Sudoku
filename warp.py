import cv2
import numpy as np

MAX_FEATURES=500
good_match_percent=0.15


def alignImages(im1, im2):
    im1gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    orb=cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1=orb.detectAndCompute(im1gray,None)
    keypoints2, descriptors2=orb.detectAndCompute(im2gray,None)

    matcher=cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches=matcher.match(descriptors1,descriptors2, None)

    matches.sort(key=lambda x: x.distance, reverse=False)

    numGoodMatches = int(len(matches)*good_match_percent)
    matches=matches[:numGoodMatches]

    imMatches =cv2.drawMatches(im1, keypoints1,im2,keypoints2,matches, None)
    cv2.imwrite("matches.jpg", imMatches)

    points1=np.zeros((len(matches), 2), dtype=np.float32)
    points2=np.zeros((len(matches), 2), dtype=np.float32)

    for i,match in enumerate(matches):
        points1[i,:]=keypoints1[match.queryIdx].pt
        points2[i,:]=keypoints2[match.trainIdx].pt

    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    height, width, channels=im2.shape
    im1Reg=cv2.warpPerspective(im1, h, (width,height))

    return im1Reg, h    






imReference=cv2.imread("ref_im.jpg")
imReference=imReference[90:,:]

im=cv2.imread("scanned_im1.jpeg")

imReg, h=alignImages(im, imReference)

cv2.imwrite("allined.jpg",imReg)
