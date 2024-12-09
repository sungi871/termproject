import cv2

def detect_color(frame, color_range):
   
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # BGR -> HSV 변환
    #색상 감지
 
    mask = cv2.inRange(hsv_frame, color_range['lower'], color_range['upper'])
    
 
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    return mask, result
