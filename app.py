import streamlit as st 
import os
import pytesseract as pt
import cv2
from PIL import Image
def save_uploadedfile(uploadedfile):
        with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
            f.write(uploadedfile.getbuffer())
        return st.success("Image Loaded")
uploaded_file=st.file_uploader('Choose Image file',type=['jpg','jpeg','png'])
if uploaded_file is not None:
    save_uploadedfile(uploaded_file)
    img_object = cv2.imread(os.path.join("tempDir",uploaded_file.name))
    gray_image = cv2.cvtColor(img_object, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17) 
    edged = cv2.Canny(gray_image, 30, 200) 
    cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
    screenCnt = None
    i=7
    flag=0
    for c in cnts:
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
            if len(approx) == 4: 
                    screenCnt = approx
                    x,y,w,h = cv2.boundingRect(c) 
                    new_img=img_object[y:y+h,x:x+w]
                    cv2.imwrite('./'+str(i)+'.png',new_img)
                    i+=1
                    flag=1
                    break

    Cropped_loc = './7.png'
    plate = pt.image_to_string(Cropped_loc, lang='eng')
    st.write("Plate Number:")
    if(flag):
        st.write( plate)
