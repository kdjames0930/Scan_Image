import cv2
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def scanImg(img):
    # img = cv2.imread('./images/document.jpg')
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
    print(f"꼭짓점의 수: {len(approx)}")
    if len(approx)!=4:
        print("사진을 다시 촬영해주세요")
        st.write("사진을 다시 촬영해주세요")
        cv2.imwrite('contour.jpg', img)
        return False
    else:
        print("사진이 정상적으로 처리되었습니다")

    # 순서대로 좌상단, 좌하단, 우상단, 우하단으로 정렬
    corners = sorted(approx, key=lambda x: x[0]+x[1])
    if corners[1][1] < corners[2][1]:
        corners[1], corners[2] = corners[2], corners[1]

    src = np.float32(corners)
    dst = np.float32([[1240, 0], [0, 0], [1240, 1754], [0, 1754]])

    M = cv2.getPerspectiveTransform(src, dst)
    dst = cv2.warpPerspective(img_rgb, M, (1240, 1754))
    
    cv2.imwrite('scanned.jpg', dst)
    return True

