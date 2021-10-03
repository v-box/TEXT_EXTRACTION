#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 08:55:07 2021

@author: vb
"""

import glob
from pdf2image import convert_from_path
import cv2
import pytesseract
import os
import img2pdf
#%%

pdf_list = glob.glob("pdfslist/*.pdf")
for i in range(0,len(pdf_list)):
    pdf = pdf_list[i]
    print('single pdf selected')
    pages = convert_from_path(pdf,0)
    print('All {} converted to images'.format(pdf))
    img_count = 1
    filename = (pdf.replace('.pdf','')).split('/')
    for page in pages:
        img_name = ("{}_img_"+str(img_count)+".jpg").format(filename[1])
        page.save(img_name,'JPEG')
        img_count += 1
        print(img_name,"image saved")
        img = cv2.imread(img_name)
        img = cv2.resize(img, (1240,1755))
        hImg, wImg, _ = img.shape
        
        boxes = pytesseract.image_to_boxes(img)
        for box in boxes.splitlines():
            box = box.split(' ')
            x, y, z, a = int(box[1]),int(box[2]),int(box[3]),int(box[4])
            cv2.rectangle(img, (x, hImg - y), (z, hImg - a), (0, 255, 0), 2) 
            cv2.putText(img, box[0], (x, hImg - y + 13), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 205, 50), 1)
            boxed_image = ("{}_boxed_image_"+str(img_count-1)+".jpg").format(filename[1])
            cv2.imwrite(boxed_image,img)
        print('Completed_DrawBoxes in ', img_name)
        # extracting started 
        with open(('{}_FULL_TEXT.txt').format(filename[1]), 'a') as output:
            print("output file created")
            text = str((pytesseract.image_to_string(img_name)))
            text = text.strip()
            output.write(text + "\n\n\n\n")
            print('text extracted of ',img_name)
        output.close()
        os.remove(img_name)

        pdf_name = ("{}_BOXED.pdf").format(filename[1])
        with open(pdf_name,'wb') as creat_pdf:
            pdf_bytes = img2pdf.convert(glob.glob("*.jpg"))
            creat_pdf.write(pdf_bytes)
        creat_pdf.close()
        
    for file in glob.glob("*.jpg"):
        os.remove(str(file))
    print('Boxed pdf and Extraction created of ', (pdf.split('/'))[1])        
#%%

