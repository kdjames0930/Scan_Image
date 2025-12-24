import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import streamlit as st
import scan as sc

st.title("문서 스캔 웹 애플리케이션")
st.write("문서를 스캔하는 프로그램입니다 \n 사진을 찍어 문서를 스캔해보세요!")

uploaded_file = st.file_uploader("이미지 업로드하기")
if uploaded_file is not None:
   image = Image.open(uploaded_file)
   # st.image(image, caption='Input', use_container_width=True)
   img_array = np.array(image)
   cv2.imwrite('uploaded.jpg', cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR))
   img = cv2.imread('uploaded.jpg')
   st.write("업로드된 파일: ", uploaded_file.name)
   success = sc.scanImg(img)
   if success:
      output = Image.open('scanned.jpg')
      st.image(output, caption='Output', use_container_width=True)
   else:
      output = Image.open('contour.jpg')
      st.image(output, caption='Output failed', use_container_width=True)

if st.button("이미지 촬영하기"):
   cap = cv2.VideoCapture(0)
   while cap.isOpened():
      ret, frame = cap.read()

      if not ret:
        break

      k = cv2.waitKey(5)

      if k==ord('c'):
        cv2.imwrite('document.jpg', frame)
        img = cv2.imread('document.jpg')
        sc.scanImg(img)
        print("Image Captured")
        break
      elif k==ord('q'):
        break

      cv2.imshow('img', frame)
   cap.release()

cv2.destroyAllWindows()