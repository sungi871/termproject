import cv2

def detect_color(frame, color_range):
<<<<<<< HEAD
    # 이미지에서 색상을 감지하는 함수
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # BGR -> HSV 변환
    
    # 주어진 색상의 범위에 맞는 마스크 생성
    mask = cv2.inRange(hsv_frame, color_range['lower'], color_range['upper'])
    
    # 마스크를 이용하여 원본 이미지에서 색상 필터링
=======
   
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # BGR -> HSV 변환
    
 
    mask = cv2.inRange(hsv_frame, color_range['lower'], color_range['upper'])
    
 
>>>>>>> origin/main
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    return mask, result
