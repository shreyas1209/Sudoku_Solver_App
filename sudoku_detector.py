# -*- coding: utf-8 -*-
"""sudoku_detector.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1WV08oBuRLOibzbsG1AXPVD-uKe5GpkY0
sudoku_detector(img):
Transforms on image:
1.cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) converts the image to grayscale
2.Adding GaussianBlur
3.Image thresholding is an important intermediary step for image processing pipelines. Thresholding can help us to remove lighter or darker regions and contours of images
"""
import cv2
import imutils
import numpy as np
from imutils.perspective import four_point_transform
from google.colab.patches import cv2_imshow
import operator


def sudoku_detector(img,show = False, dilate = True):
  image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
  image_blur = cv2.GaussianBlur(image_gray,(5,5),3)
  
  image_threshold = cv2.adaptiveThreshold(image_blur, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
  
  kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]],np.uint8)
  
  image_processed = image_threshold
  if dilate == True:
    image_processed = cv2.dilate(image_threshold, kernel)

  
  original_pic = img.copy()
  if show == True:
        cv2_imshow(image_gray)
        cv2_imshow(image_blur)
        cv2_imshow(image_threshold)
        cv2_imshow(image_processed)
          
  return(image_processed)

def find_boundary(img,show = True):
  contours,hierarchy = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key=cv2.contourArea, reverse=True)
  sudoku_box = contours[0]
  

 
	# Top-left has point smallest (x + y) value
	# Top-right point has largest (x - y) value
  # Bottom-left point has smallest (x - y) value
  # Bottom-right point has largest (x - y) value
	
  top_left , _ = min(enumerate([tl[0][0] + tl[0][1] for tl in sudoku_box]), key= operator.itemgetter(1))
  top_right , _ = min(enumerate([tr[0][0] + tr[0][1] for tr in sudoku_box]), key= operator.itemgetter(1))
  bottom_left , _ = min(enumerate([bl[0][0] + bl[0][1] for bl in sudoku_box]), key= operator.itemgetter(1))
  bottom_right , _ = min(enumerate([br[0][0] + br[0][1] for br in sudoku_box]), key= operator.itemgetter(1))
  print(top_left,top_right,bottom_left,bottom_right)






  
  '''for i,contour in enumerate(contours):
    approx_box = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True)
    if len(approx_box)==4:
      X,Y,W,H = cv2.boundingRect(approx_box)
      
      if (H>3 and W>3):
        cv2.drawContours(original_pic, [approx_box], 0, (0,0,255),5)
        cv2_imshow(original_pic)
        puzzle = four_point_transform(img, approx_box.reshape(4, 2))


        if show == True:
          cv2_imshow(image_gray)
          cv2_imshow(image_blur)
          cv2_imshow(image_threshold)
          cv2_imshow(image_processed)
          cv2_imshow(puzzle)

          contours = cv2.findContours(image_processed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
          contours = imutils.grab_contours(contours)
          contours = sorted(contours, key=cv2.contourArea, reverse=True)
          largest_contour = contours[0]

  return(puzzle)'''

'''
digit_extraction(img,position,img_size,grid_size, show = False):
img is the image
position is the tuple for the position in the grid (zero_indexed)
img_size is the tuple for the image size()
grid_size is the tuple for the size of the grid (like (9,9))
extracted_img_size is the tuple for the size for the extracted image
All tuples are of the form(height,width)
'''

from skimage.segmentation import clear_border
def digit_extraction(img,position,img_size,grid_size,extracted_img_size,show = False):
  image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  block_size_h = img_size[0]//grid_size[0]
  block_size_w = img_size[1]//grid_size[1]
  h_i = block_size_h*(position[0])
  h_f = h_i + block_size_h
  w_i = block_size_w*(position[1])
  w_f = w_i + block_size_w
  digit = image[h_i:h_f,w_i:w_f]
  digit = cv2.resize(digit,extracted_img_size)
  #digit_gray = cv2.cvtColor(np.array(digit, dtype=np.uint8), cv2.COLOR_BGR2GRAY)
  digit_threshold = cv2.adaptiveThreshold(digit , 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,27,2)
      
      
  if show == True:
    cv2_imshow(digit)
    cv2_imshow(digit_threshold)

  return(digit_threshold)

        
      

  
