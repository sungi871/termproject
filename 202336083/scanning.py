import cv2
import numpy as np

def order_points(pts):
    """문서의 4개의 꼭짓점을 정렬"""
    rect = np.zeros((4, 2), dtype="float32")

    # x+y가 가장 작은 점은 좌상단, 가장 큰 점은 우하단
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # x-y가 가장 작은 점은 우상단, 가장 큰 점은 좌하단
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def four_point_transform(image, pts):
    """투영 변환을 적용"""
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # 새로운 이미지의 폭과 높이 계산
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = int(max(widthA, widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = int(max(heightA, heightB))

    # 변환 후 직사각형 좌표
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")

    # 투영 변환 매트릭스 계산 및 적용
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

# 이미지 읽기
image = cv2.imread("/Users/admin/Documents/openswterm/docu1.jpeg")
if image is None:
    raise FileNotFoundError("이미지를 찾을 수 없습니다. 경로를 확인하세요.")

orig = image.copy()

# 1. 그레이스케일 변환 및 엣지 검출
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 50, 150)

# 2. 윤곽선 탐지
contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

# 3. 문서 윤곽선 찾기
for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    if len(approx) == 4:  # 꼭짓점이 4개인 윤곽선 선택
        screen_contour = approx
        break

# 4. 투영 변환
warped = four_point_transform(orig, screen_contour.reshape(4, 2))

# 5. 결과 저장
original_output_path = "/Users/admin/Documents/openswterm/original_output.jpg"
scanned_output_path = "/Users/admin/Documents/openswterm/scanned_output.jpg"
cv2.imwrite(original_output_path, orig)
cv2.imwrite(scanned_output_path, cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY))

print(f"Original image saved to: {original_output_path}")
print(f"Scanned image saved to: {scanned_output_path}")
