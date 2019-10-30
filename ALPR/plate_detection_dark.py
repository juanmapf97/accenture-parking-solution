"""
First test at plate detection.
Follow this steps:
    1. Turn image greyscale
    2. Apply bilateral filter
    3. Apply Canny and find contours
    4. Get all rectangles from contours
    5. Get contours size and sort them
    6. Find contours with exactly 4 sides
    7. Crop section of image
    8. Apply tesseract OCR
"""

import cv2
import numpy as np
import imutils
import pytesseract
from PIL import Image

def auto_canny(image, sigma=0.55):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
 
	# return the edged image
	return edged

image = cv2.imread('plate_dataset/IMG_8123.png')
image = imutils.resize(image, width=1000) # Check if necessary

image = image[100:520, 250:750]

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)

blackHat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)



add = cv2.add(gray, tophat)
sub = cv2.subtract(add, blackHat)

cv2.imshow("", sub)
cv2.waitKey(0)


ret, thresh = cv2.threshold(sub,30,255,cv2.THRESH_TRIANGLE)
# ret, thresh = cv2.threshold(sub,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, rectKernel)

# perform a series of erosions and dilations to remove
# any small blobs of noise from the thresholded image
thresh = cv2.erode(thresh, None, iterations=5)
thresh = cv2.dilate(thresh, None, iterations=8)

edged = auto_canny(thresh)

cv2.imshow("thresh.png", thresh)
cv2.waitKey(0)

cv2.imshow("", edged)
cv2.waitKey(0)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
number_plate = []

peri = cv2.arcLength(cnts[0], True)
approx = cv2.approxPolyDP(cnts[0], 0.018 * peri, True)
number_plate.append(approx)

cv2.drawContours(image, number_plate, -1, (0,255,0), 3)

gray = cv2.bilateralFilter(gray,11,17,17)

# Masking the part other than the number plate
mask = np.zeros(gray.shape,np.uint8)
new_image = cv2.drawContours(mask,number_plate,0,255,0)
new_image = cv2.bitwise_and(image,image,mask=mask)

# Now crop
(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
cropped = gray[topx:bottomx+1, topy:bottomy+1]

cropped = cv2.adaptiveThreshold(cropped, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)

text = pytesseract.image_to_string(cropped, config='--psm 11')
print(text)

cv2.imshow("Number plate detection", cropped)
cv2.waitKey(0)