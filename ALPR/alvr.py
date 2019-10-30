import numpy as np
import cv2
import imutils
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Get text from a cropped image of a license plate
def getText(plate):

    return pytesseract.image_to_string(plate, config='--psm 11')
    #print("Detected Number is:",text)


# Detect a license plate in a picture
def detectPlate(imageRoute):
    img = cv2.imread(imageRoute,cv2.IMREAD_COLOR)
    img = imutils.resize(img, width=1080)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
    edged = cv2.Canny(gray, 30, 200) #Perform Edge detection

    # find contours in the edged image, keep only the largest ones, and initialize our screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None

    # loop over our contours
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        ratio = w/h 
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        # if our approximated contour has four.
        #  points, then
        # we can assume that we have found our screen
        
        if len(approx) == 4:
            #print(ratio)
            screenCnt = approx
            break

    if screenCnt is not None:
        # Masking the part other than the number plate
        mask = np.zeros(gray.shape,np.uint8)
        new_image = cv2.drawContours(mask,[screenCnt],0,255,0)
        new_image = cv2.bitwise_and(img,img,mask=mask)

        # Now crop
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]

        CroppedT = cv2.adaptiveThreshold(Cropped,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)

        text = getText(CroppedT)

        return text, Cropped, img
    
    else:
        return "No plates found", None, None
    



