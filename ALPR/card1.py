import cv2
import numpy as np
import imutils
from text_recognition import text_name
import pytesseract

def auto_canny(image, sigma=0.55):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
 
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
 
    # return the edged image
    return edged
'''
def id_text():
    img2 = cv2.imread("images/Name007.png", -1)
    cv2.imshow('',img2)
    text=pytesseract.image_to_string(dark, config="-l tessdata/spa --oem 1 --psm 13")
    print("Detected Number is:",text)
'''

def id_detection():
    cap = cv2.VideoCapture(1)
    while(True):
        ret, img = cap.read()

        #img = cv2.imread("card_06.jpeg", -1)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        gray = cv2.medianBlur(gray,13)

        #ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_TRIANGLE)
        thresh=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv2.THRESH_BINARY,11,2)

        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

        edged = auto_canny(opening)
        
        cv2.imshow('edge',edged)


        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
        number_plate = []

        peri = cv2.arcLength(cnts[0], True)
        approx = cv2.approxPolyDP(cnts[0], 0.018 * peri, True)
        number_plate.append(approx)

        if len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            if ar>1.4 and ar<1.6:       
                print('rectagle', str(ar))
                print('aprox', str(approx))

                cv2.drawContours(img, number_plate, -1, (0,255,0), 3)

                cv2.imshow('square',img)

                point1=approx[0][0][0]
                print('point'+str(point1))
                x1=approx[0][0][0]
                y1=approx[0][0][1]
                x2 = approx[1][0][0]
                y2=approx[1][0][1]
                x3=approx[2][0][0]
                y3= approx[2][0][1]
                x4 =approx[3][0][0]
                y4= approx[3][0][1]

                top_left_x = min(x1,x2,x3,x4)
                top_left_y = min([y1,y2,y3,y4])
                bot_right_x = max([x1,x2,x3,x4])
                bot_right_y = max([y1,y2,y3,y4])
                
                crop=img[top_left_y:bot_right_y+1, top_left_x:bot_right_x+1]
                cv2.imshow('crop',crop)

                name=crop[75:160,120:270]
                #cv2.imshow('name',name)

                dark= cv2.cvtColor(name, cv2.COLOR_BGR2GRAY)

                thresh=cv2.adaptiveThreshold(dark,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv2.THRESH_BINARY,11,2)

                kernel = np.ones((3,3),np.uint8)
                dark = cv2.morphologyEx(dark, cv2.MORPH_OPEN, kernel)

                dark = auto_canny(dark)
        
                #cv2.imshow('dark',dark)
                string_name=text_name()
                print(string_name)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    
    return string_name,crop