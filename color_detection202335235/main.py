import cv2
import os
from color_detection import detect_color


COLOR_RANGES = {
    'red': {'lower': (0, 120, 70), 'upper': (10, 255, 255)},
    'green': {'lower': (36, 100, 100), 'upper': (86, 255, 255)},
    'blue': {'lower': (94, 80, 2), 'upper': (126, 255, 255)}
}

def process_image(image_path):

    frame = cv2.imread(image_path)
    if frame is None:
        print(f"이미지를 불러올 수 없습니다: {image_path}")
        return
    

    for color, ranges in COLOR_RANGES.items():
        mask, result = detect_color(frame, ranges)
        cv2.imshow(f'{color} mask', mask)
        cv2.imshow(f'{color} detection', result)
    
    cv2.imshow('Original Image', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    
    image_path = os.path.join(os.path.dirname(__file__), 'resources', 'example_image.jpg')


    if not os.path.exists(image_path):
        print(f"오류: '{image_path}' 파일을 찾을 수 없습니다.")
        return

    print(f"이미지 파일을 처리합니다: {image_path}")
    process_image(image_path)

if __name__ == "__main__":
    main()
