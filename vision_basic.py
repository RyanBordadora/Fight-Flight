import cv2
import numpy as np

class Vision:
    def __init__(self,rval,vc,frame,height,width):
        self.frame = frame
        self.height = height
        self.width = width
        self.detected = False
        self.vc = vc
        self.rval = rval

    def see(self):
        #define frame
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        
        #define color range (high and low)
        #lower_pink = np.array([140, 50, 50])
        lower_pink = np.array([120, 50, 50])
        upper_pink = np.array([180, 255, 255])

        #lower_pink = np.array([140, 50, 150], dtype = "uint8")
        #upper_pink = np.array([50, 255, 255], dtype = "uint8")

        #draw frame with only color, black and white
        mask = cv2.inRange(hsv, lower_pink, upper_pink)
        res = cv2.bitwise_and(self.frame,self.frame, mask= mask)

        #find color in original frame
        colorcnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        #check if drone is in center of screen (fire range)
        if len(colorcnts) > 0:
            color_area = max(colorcnts, key=cv2.contourArea)
            (xg,yg,wg,hg) = cv2.boundingRect(color_area)
            #print((xg,yg,wg,hg))
            #print(colorcnts)
            cv2.rectangle(self.frame,(xg,yg),(xg+wg, yg+hg),(0,255,0),2)
            width_threshold = self.width * 0.6
            height_threshold = self.height * 0.6
            #if xg <= self.width and yg <= self.height and yg + hg >= self.height and xg + wg >= self.width:
            #if xg <= (self.width - width_threshold) / 2 and xg + wg >= (self.width + width_threshold) / 2 and yg <= (self.height - height_threshold) / 2 and yg + hg >= (self.height + height_threshold) / 2:
            #if xg <= self.width/2 and xg + wg >= self.width/2 and yg <= self.height/2 and yg + hg >= self.height/2:
            self.detected = True
                #print("detected")
            #else:
                #self.detected = False
                #print("not detected")

        #display colors
       # if self.frame is not None:
           # cv2.imshow("preview", self.frame)
            #cv2.imshow('mask',mask)
            #cv2.imshow('res',res)

        self.rval,self.frame = self.vc.read()

    def is_detected(self):
        return self.detected