import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)

def auto_canny(image, sigma=0.55):
        # compute the median of the single channel pixel intensities
        v = np.median(image)
     
        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)
     
        # return the edged image
        return edged

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

            cv2.drawContours(img, number_plate, -1, (0,255,0), 3)

            cv2.imshow('square',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()