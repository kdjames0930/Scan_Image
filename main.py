import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import streamlit as st
import scan as sc
import os

st.set_page_config(page_title="문서 스캔", layout="centered")
st.title("문서 스캔 웹 애플리케이션")
st.write("문서를 스캔하는 프로그램입니다 \n 사진을 찍어 문서를 스캔해보세요!")

WORKDIR = os.path.dirname(os.path.abspath(__file__))

UPLOADED_PATH = os.path.join(WORKDIR, "uploaded.jpg")
CAPTURED_PATH = os.path.join(WORKDIR, "document.jpg")
SCANNED_PATH = os.path.join(WORKDIR, "scanned.jpg")
CONTOUR_PATH = os.path.join(WORKDIR, "contour.jpg")

def convert_img(pil_img: Image.Image) -> np.ndarray:
    rgb = np.array(pil_img.convert("RGB"))
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    return bgr

def run_scan(bgr_img: np.ndarray, source_name: str):
   st.write(f"업로드된 파일: {source_name}")
   
   cv2.imwrite(UPLOADED_PATH, bgr_img)

   success, scanned_img, debug_bgr, message = sc.scanImg(bgr_img)
   if success:
      st.image(scanned_img, caption=message, use_container_width=True)
   else:
      st.image(cv2.cvtColor(debug_bgr, cv2.COLOR_BGR2RGB), caption=message, use_container_width=True)

st.subheader("1) 이미지 업로드")
uploaded_file = st.file_uploader("이미지 업로드하기", type=['jpg', 'jpeg', 'png'])
if uploaded_file is not None:
   image = Image.open(uploaded_file)
   st.image(image, caption='Input', use_container_width=True)
   bgr_image = convert_img(image)
   run_scan(bgr_image, f"{uploaded_file.name}")

st.divider()

st.subheader("2) 카메라로 촬영 (Streamlit 방식)")
camera_file = st.camera_input("카메라로 촬영하기")

if camera_file is not None:
    pil_image = Image.open(camera_file)
    st.image(pil_image, caption="Captured", use_container_width=True)
    bgr_img = convert_img(pil_image)
    cv2.imwrite(CAPTURED_PATH, bgr_img)
    run_scan(bgr_img, "카메라 촬영")