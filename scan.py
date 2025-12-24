import cv2
import numpy as np

def scanImg(img):
    """
    Returns:
      success (bool) 스캔 성공 여부,
      scanned_rgb (np.ndarray | None) 스캔된 이미지,
      img (np.ndarray | None) 객체 윤곽선 그려진 이미지, 
      message (str) 스캔 성공 여부
    """
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh_binary = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

    sortedContours = sorted(contours, key=cv2.contourArea, reverse=True)
    cv2.drawContours(img, [sortedContours[0]], -1, (0, 255, 0), 3)

    peri = cv2.arcLength(sortedContours[0], True)
    approx = cv2.approxPolyDP(sortedContours[0], 0.02 * peri, True)
    approx = np.squeeze(approx, axis=1)
    if len(approx)!=4:
        message = f"사진을 다시 촬영해주세요. 꼭짓점의 수 {len(approx)}개"
        return False, None, img, message
    else:
        message ="정상적으로 스캔되었습니다."

    # 순서대로 좌상단, 좌하단, 우상단, 우하단으로 정렬
    corners = sorted(approx, key=lambda x: x[0]+x[1])
    if corners[1][1] < corners[2][1]:
        corners[1], corners[2] = corners[2], corners[1]

    src = np.float32(corners)
    dst = np.float32([[1240, 0], [0, 0], [1240, 1754], [0, 1754]])

    M = cv2.getPerspectiveTransform(src, dst)
    dst = cv2.warpPerspective(img_rgb, M, (1240, 1754))
    
    cv2.imwrite('scanned.jpg', dst)
    return True, dst, img, message