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

'''
sudoku_detector(img,show = True, dilate  = False , erode = False):Applies basic image preprocessing on an image
like converting to grayscale, blurring the image using gaussian blur, and adaptive thresholding.
The parameters are - 
img: The image to which the preprocessing is done
show : Default is True.It shows each step of the preprocessing
dilate: Default is False. It applies dilation onto the image
erode: Default is False. It applies erosion onto the image

This function returns the processed image
'''
def sudoku_detector(img,show = True, dilate = False ,erode = False):
  image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#converts colorspace from RGB to graysacle
  
  image_blur = cv2.GaussianBlur(image_gray,(7,7),3) #adding a gaussian blur with kernel size 7 and stddev 3 to reduce noise in the image
  
  #adaptive threshold method where the threshold value is calculated for smaller regions 
  #max pixel  value to be given after thresholding is 255 ( white color)
  #ADAPTIVE_THRESH_GAUSSIAN_C − threshold value is the weighted sum of neighborhood values where weights are a Gaussian window.
  #cv2.THRESH_BINARY_INV - Inverts the case of binary thresholding
  #threshold uses 11 neighboring pixels
  image_threshold = cv2.adaptiveThreshold(image_blur, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

  
  image_processed = image_threshold
  #adding an option dilation and erosion 
  
  if dilate == True:
    kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]],np.uint8) #kernel finds the maximum overlap in dilation and minimum overlap in erosion
    image_processed = cv2.dilate(image_threshold, kernel)
  if erode == True:
    kernel = np.ones((5,5),np.uint8)
    image_processed = cv2.erode(image_processed,kernel,iterations = 1)
		
  original_pic = img.copy()
  #displaying the preprocces_images
  if show == True:
        cv2_imshow(cv2.resize(image_gray,(360,360)))
        cv2_imshow(cv2.resize(image_blur,(360,360)))
        cv2_imshow(cv2.resize(image_threshold,(360,360)))
        cv2_imshow(cv2.resize(image_processed,(360,360)))
          
  return(image_processed)
#end of sudokupreprocessing

'''
find_boundary(original_img,img,show = True): Finds the boundary for the bounding box in the given image
Parameters-
original_img: The non preprocessed image
img : The preprocessed image
show: Default is True. Shows the bounding box
returns tuple for coordinates in the form (top_left,top_right, bottom_right,bottom_left)
'''

def find_boundary(original_img,img,show = True):
  contours = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#finding the contours

  contours = imutils.grab_contours(contours)#adds a counter to the contour
  original_pic = original_img.copy()
  from google.colab.patches import cv2_imshow
  for i,contour in enumerate(contours):  #iterating for all the detected contours
    approx_box = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True) #approximates a contour shape to another shape with less number of vertices with 0.01 precision 
    if len(approx_box)==4:#finding if the box is quadrilateral in shape
      X,Y,W,H = cv2.boundingRect(approx_box)   #x,y coordinates of top left corner and w,h are width and height of the box 
      
      if (H>3 and W>3):      #avoiding smaller contours
        cv2.drawContours(original_pic, [approx_box], 0, (0,0,255),5)  #plotting the edge of the box
        #operation.itemgetter allows us to get max and min values of the index of the point
        #Each point is an array of X and Y coordinates so [0] represents X coordinate and [1] represents Y coordinate
        #top left has smallest x+y value
        #top right has the maximum x-y value
        #bottom left has the smallest x-y value
        #bottom right has the largest x+y value
        #Now using this to get the coordinates of the 4 corners of the box
        top_left , _ = min(enumerate([tl[0][0] + tl[0][1] for tl in approx_box]), key= operator.itemgetter(1))
        top_right , _ = max(enumerate([tr[0][0] - tr[0][1] for tr in approx_box]), key= operator.itemgetter(1))
        bottom_left , _ = min(enumerate([bl[0][0] - bl[0][1] for bl in approx_box]), key= operator.itemgetter(1))
        bottom_right , _ = max(enumerate([br[0][0] + br[0][1] for br in approx_box]), key= operator.itemgetter(1))
        if show ==True:
          cv2_imshow(cv2.resize(original_pic,(360,360)))
        #returns coordinates
        return(np.array([approx_box[top_left][0],approx_box[top_right][0],approx_box[bottom_right][0],approx_box[bottom_left][0]],np.float32))
        


def euclidean_distance(pt1, pt2): #finds euclidean distance
    x = pt2[0] - pt1[0] 
    y = pt2[1] - pt1[1] 
    return np.sqrt((x ** 2) + (y ** 2))
'''
crop_and_warp(original_img,img,box_array,show = True): Function that crops the sudoku's bounding box from the rest 
of the image and gives us a top-down view
Parameters-
original_img: The non preprocessed image
img : The preprocessed image
box_array:The coordinates of bounding box in the form(top_left,top_right, bottom_right,bottom_left)
show: Default is True. Shows the cropped and warped image
returns (original image warped , preprocessed image warped)
'''
def crop_and_warp(original_img,img,box_array,show = True):
  top_left,top_right,bottom_right,bottom_left = box_array
  original_pic = original_img.copy()
  #Plotting the corner points of the bounding box
  original_pic= cv2.circle(original_pic, (top_left[0],top_left[1]), radius=10, color=(255, 0, 0), thickness=-10)
  original_pic = cv2.circle(original_pic, (top_right[0],top_right[1]), radius=10, color=(255, 0, 0), thickness=-10)
  original_pic = cv2.circle(original_pic, (bottom_left[0],bottom_left[1]), radius=10, color=(255, 0, 0), thickness=-10)
  original_pic = cv2.circle(original_pic, (bottom_right[0],bottom_right[1]), radius=10, color=(255, 0, 0), thickness=-10)
  
  
  #Find the maximum amongst leengths and breadths to find the maximum side for the warped image
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
  image_warped = cv2.warpPerspective(original_img,image_perspective,(int(max_side),int(max_side)))#warping the original image
  img_warped = cv2.warpPerspective(img,image_perspective,(int(max_side),int(max_side))) #warping the grayscale image
  if show ==True:
    cv2_imshow(cv2.resize(original_pic,(360,360)))
    cv2_imshow(cv2.resize(image_warped,(360,360)))
    cv2_imshow(cv2.resize(img_warped,(360,360)))
  return (image_warped,img_warped)




from skimage.segmentation import clear_border
'''
digit_extraction(img,position,img_size,grid_size,extracted_img_size,show = True):Function that
extracts each digit from the 9x9 grid
Parameters:
img: The preprocessed image that only contains the sudoku
position: Tuple containing index of a particular square in the grid
grid_size:Size of the entire sudoku grid
extracted_img_size : Tuple for the size of the extracted image digit
show: Default is True. Shows the extracted digit
returns (extracted image)
'''
def digit_extraction(img,position,img_size,grid_size,extracted_img_size,show = True):
  image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Converting to grayscale
  image_processed = image_gray
  block_size_h = img_size[0]//grid_size[0] #height of each number block
  block_size_w = img_size[1]//grid_size[1] #width of each number block
  h_i = block_size_h*(position[0]) #top height of the digit box
  h_f = h_i + block_size_h #bottom height of the digit box
  w_i = block_size_w*(position[1]) #left coordinate of the digit box
  w_f = w_i + block_size_w #right coordinate of the digit box
  digit = image_processed[h_i:h_f,w_i:w_f] #cropping out the digit box
  #Otsu's method avoids having to choose a threshold value and determines it automatically by
  # determining an optimal global threshold value from the image histogram
  digit = cv2.threshold(digit,0,255, cv2.THRESH_BINARY_INV |  cv2.THRESH_OTSU)[1] #applying OTSU threshold with binary inversion
  digit = clear_border(digit) #clears objects connected to the image border

  digit_contours = cv2.findContours(digit.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#finding the contours
  digit_contours = imutils.grab_contours(digit_contours) #adds a counter to the contour
  #image masking
  if len(digit_contours)!=0: #checking if there are any contours in the image 
    digit_contour = max(digit_contours, key=cv2.contourArea) #Finding the contour housing the largest area
    background = np.zeros(digit.shape,dtype = np.uint8) #Creating a  mask of the size of digit
    cv2.drawContours(background,[digit_contour],-1,255,-1) #drawing the digit contour on the mask
    digit = cv2.bitwise_and(digit,digit, mask=background) #bitwiseAND is true if and only if both pixels are greater than zero
    


  digit = cv2.resize(digit,extracted_img_size) #resizing the digit to desired output shape
      
      
  if show == True:
    cv2_imshow(digit)

  return(digit)

        
      

  
