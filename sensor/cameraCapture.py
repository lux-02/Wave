import cv2
import numpy as np

# 카메라 캡처 시작
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # HSV 색공간으로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 피부색에 해당하는 HSV 범위 정의 (이 값은 조정이 필요할 수 있습니다)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # 피부색 범위로 마스크 생성
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # 마스크에서 노이즈 제거
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # 경계 찾기
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 가장 큰 경계 찾기
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        print("Detected palm area:", area)

        # 경계 그리기
        cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 3)

    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
