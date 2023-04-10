import cv2
import numpy as np
def transform(image):
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    canny = cv2.Canny(blur,50,150)
    return canny

def set_roi(image):
    height = image.shape[0]
    corners = np.array([
        [(200,height),
         (1100,height),
         (550,250)]
        ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask,corners,255)
    masked_image = cv2.bitwise_and(image,mask)
    return masked_image
    
def display_lines(image,lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            cv2.line(line_image,(x1,y1),(x2,y2),(0,255,0),10)
    return line_image
def calc_coordinates(image,line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1-intercept) / slope)
    x2 = int((y2-intercept) / slope)
    return np.array([x1,y1,x2,y2])

def average_slope(image,lines):
    left = []
    right = []
    for line in lines:
        x1,y1,x2,y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2),(y1,y2),1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left.append((slope,intercept))
        else:
            right.append((slope,intercept))

    left_avg = np.average(left,axis=0)
    right_avg = np.average(right,axis=0)
    left_line = calc_coordinates(image,left_avg)
    right_line = calc_coordinates(image,right_avg)

    return np.array([left_line,right_line])


###### COMMENT FROM HERE FOR TESTING PNG FILE #######
cap = cv2.VideoCapture("test.mp4")
while True:
    ret, frame = cap.read()
    if ret:
        res = transform(frame)

        cropped = set_roi(res)
        lines = cv2.HoughLinesP(cropped,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)

        average_line = average_slope(frame,lines)

        line_image = display_lines(frame,average_line)
        combined_image = cv2.addWeighted(frame,0.8,line_image,1,1)
        cv2.imshow("result",combined_image)
        if cv2.waitKey(1) == ord("q"):
            break
""" 
image = cv2.imread("test.png")
res = transform(image)

cropped = set_roi(res)
lines = cv2.HoughLinesP(cropped,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)

average_line = average_slope(image,lines)

line_image = display_lines(image,average_line)
combined_image = cv2.addWeighted(image,0.8,line_image,1,1)
cv2.imshow("result",combined_image)
cv2.waitKey(0)
"""
cv2.destroyAllWindows()