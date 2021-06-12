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


def sudoku_detector(img,show = True, dilate = False ,erode = False):
  image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
  image_blur = cv2.GaussianBlur(image_gray,(7,7),3)
  
  image_threshold = cv2.adaptiveThreshold(image_blur, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

  
  image_processed = image_threshold
  if dilate == True:
    kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]],np.uint8)
    image_processed = cv2.dilate(image_threshold, kernel)
  if erode == True:
    kernel = np.ones((5,5),np.uint8)
    image_processed = cv2.erode(image_processed,kernel,iterations = 1)
		

  
  original_pic = img.copy()
  if show == True:
        cv2_imshow(image_gray)
        cv2_imshow(image_blur)
        cv2_imshow(image_threshold)
        cv2_imshow(image_processed)
          
  return(image_processed)

def find_boundary(original_img,img,show = True):
  contours = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

  contours = imutils.grab_contours(contours)
  original_pic = original_img.copy()
  from google.colab.patches import cv2_imshow
  for i,contour in enumerate(contours):
    approx_box = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True)
    if len(approx_box)==4:
      X,Y,W,H = cv2.boundingRect(approx_box)
      
      if (H>3 and W>3):
        cv2.drawContours(original_pic, [approx_box], 0, (0,0,255),5)
      
        top_left , _ = min(enumerate([tl[0][0] + tl[0][1] for tl in approx_box]), key= operator.itemgetter(1))
        top_right , _ = max(enumerate([tr[0][0] - tr[0][1] for tr in approx_box]), key= operator.itemgetter(1))
        bottom_left , _ = min(enumerate([bl[0][0] - bl[0][1] for bl in approx_box]), key= operator.itemgetter(1))
        bottom_right , _ = max(enumerate([br[0][0] + br[0][1] for br in approx_box]), key= operator.itemgetter(1))
        if show ==True:
          cv2_imshow(original_pic)
  
        return(np.array([approx_box[top_left][0],approx_box[top_right][0],approx_box[bottom_right][0],approx_box[bottom_left][0]],np.float32))
        


def euclidean_distance(pt1, pt2): 
    x = pt2[0] - pt1[0] 
    y = pt2[1] - pt1[1] 
    return np.sqrt((x ** 2) + (y ** 2))
    
def crop_and_warp(original_img,img,box_array,show = True):
  top_left,top_right,bottom_right,bottom_left = box_array
  original_pic = original_img.copy()
  original_pic= cv2.circle(original_pic, (top_left[0],top_left[1]), radius=10, color=(255, 0, 0), thickness=-10)
  original_pic = cv2.circle(original_pic, (top_right[0],top_right[1]), radius=10, color=(255, 0, 0), thickness=-10)
  original_pic = cv2.circle(original_pic, (bottom_left[0],bottom_left[1]), radius=10, color=(255, 0, 0), thickness=-10)
  original_pic = cv2.circle(original_pic, (bottom_right[0],bottom_right[1]), radius=10, color=(255, 0, 0), thickness=-10)
  
  
  #Maximum length
  breadth_1 = euclidean_distance(bottom_left,bottom_right)
  breadth_2 = euclidean_distance(bottom_left,bottom_right)
  length_1 = euclidean_distance(top_right,bottom_right)
  length_2 = euclidean_distance(top_left,bottom_left)
  max_side = max(breadth_1,breadth_2,length_1,length_2)
  #construct the set of destination points to obtain a "top-down view",  of the image, again specifying points 
  #in the top-left, top-right, bottom-right, and bottom-left order
  destination_pts = np.array([[0,0],[max_side-1,0],[max_side-1,max_side-1],[0,max_side-1]],np.float32)
  # compute the perspective transform matrix and then apply it
  image_perspective = cv2.getPerspectiveTransform(box_array,destination_pts)
  image_warped = cv2.warpPerspective(original_img,image_perspective,(int(max_side),int(max_side)))
  img_warped = cv2.warpPerspective(img,image_perspective,(int(max_side),int(max_side)))
  if show ==True:
    cv2_imshow(original_pic)
    cv2_imshow(image_warped)
    cv2_imshow(img_warped)
  return (image_warped,img_warped)




from skimage.segmentation import clear_border
def digit_extraction(img,position,img_size,grid_size,extracted_img_size,show = True,tolerance = 0):
  image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


  #image_blur = cv2.GaussianBlur(img,(1,1),3)
  #kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]],np.uint8)
  #image_processed = cv2.dilate(img, kernel)
  image_processed = image_gray
  block_size_h = img_size[0]//grid_size[0]
  block_size_w = img_size[1]//grid_size[1]
  h_i = block_size_h*(position[0])
  h_f = h_i + block_size_h
  w_i = block_size_w*(position[1])
  w_f = w_i + block_size_w
  digit = image_processed[h_i+tolerance:h_f-tolerance,w_i+tolerance:w_f-tolerance]
  digit = cv2.threshold(digit,0,255, cv2.THRESH_BINARY_INV |  cv2.THRESH_OTSU)[1]
  digit = clear_border(digit)

  digit_contours = cv2.findContours(digit.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  digit_contours = imutils.grab_contours(digit_contours)

  if len(digit_contours)!=0:
    digit_contour = max(digit_contours, key=cv2.contourArea)
    background = np.zeros(digit.shape,dtype = np.uint8)
    cv2.drawContours(background,[digit_contour],-1,255,-1)
    digit = cv2.bitwise_and(digit,digit, mask=background)
    


  digit = cv2.resize(digit,extracted_img_size)
      
      
  if show == True:
    cv2_imshow(digit)

  return(digit)

        
      

  
