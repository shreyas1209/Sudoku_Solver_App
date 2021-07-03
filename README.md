
# Sudoku Solver App

## Overview
The Sudoku Solver  is a project that makes use of Computer Vision to solve a sudoku puzzle. It takes an image of the sudoku puzzle as the input and generates the solved sudoku as the output.

## Frameworks used
This project is mainly written in Python and uses frameworks like PyTorch and OpenCV for training of the model and image preprocessing.

## Parts of the Project
1.[Image preprocessing for the Input Sudoku](#image-preprocessing-for-the-input-sudoku)\
2.[Training the Model for Digit Recognition](#training-the-model-for-digit-recognition)\
3.[Solving the Sudoku](#solving-the-sudoku)\
4.[Displaying the Solution](#displaying-the-solution)


## Image Preprocessing for the Input Sudoku
The image preprocessing is done by using OpenCV. Images of the sudoku taken need to be heavily preprocessed before each digit can be classified by the classification model. \
Let us take an example of a sample sudoku :
<  image>
The procedure I followed for preprocessing is:
 ### 1. Converting the Colorspace from BGR to Grayscale
 The OpenCV command used for this was :
 ```
 image_gray  =  cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  ```
 ### 2. Gaussian blur
Apply a Gaussian blur to the input Sudoku image with a kernel size 7 and standard deviation of  3 to reduce noise in the image
 The OpenCV command used for this was :
 ```
 image_blur  =  cv2.GaussianBlur(image_gray,(7,7),3)
  ```
  The imageof the sample sudoku after this step:\
  < insertimage >
  ### 3. Adaptive Thresholding
Thresholding is an operation that works such that if the pixel value is smaller than the threshold, it is set to 0, otherwise it is set to a maximum value.
 Adaptive threshold method where the threshold value is calculated for smaller regions. Max pixel value to be given after thresholding is 255 ( white color)
 * ADAPTIVE_THRESH_GAUSSIAN_C − Threshold value is the weighted sum of neighborhood values where weights are a Gaussian window.
* cv2.THRESH_BINARY_INV - Inverts the case of binary thresholding

 The OpenCV command used for this was :
 ```
 image_threshold  =  cv2.adaptiveThreshold(image_blur, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
  ```
  The complete code for these three sections can be found in the 
  **sudoku_detector(img,show  =  True, dilate  =  False ,erode  =  False):** function in  the file   **sudoku_detector.py**.\
  The image of the sample sudoku after this step:
  < insertimage >
 ### 4. Finding the Boundary of The Sudoku Grid
 To find the boundary of the sudoku grid in the image , first step was to  find  the contours in the image by using the OpenCV command:
 ```
 contours  =  cv2.findContours(img.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  ```
  The next step was iterating through all the contours to find one that has a shape similar to a rectangle by using the command:
  ```
approx_box = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True) 
if len(approx_box)==4:
	X,Y,W,H = cv2.boundingRect(approx_box) 
  ```
  One issue I faced using this method was that very small boxes were being detected.Hence to fix that issue I put a condition for the size of the box.
 Further I found the coordinates of the four corners of the bounding box such that:
 * Top Left corner has smallest x+y value
* Top Right has the maximum x-y value
* Bottom Left has the smallest x-y value
 * Bottom Right has the largest x+y value

The code for this is:

  ```
if (H>3 and W>3): 
	cv2.drawContours(original_pic, [approx_box], 0, (0,0,255),5) 

	top_left , _ = min(enumerate([tl[0][0] + tl[0][1] for tl in approx_box]), key= operator.itemgetter(1))
	top_right , _ = max(enumerate([tr[0][0] - tr[0][1] for tr in approx_box]), key= operator.itemgetter(1))
	bottom_left , _ = min(enumerate([bl[0][0] - bl[0][1] for bl in approx_box]), key= operator.itemgetter(1))
	bottom_right , _ = max(enumerate([br[0][0] + br[0][1] for br in approx_box]), key= operator.itemgetter(1))
  ```
 The complete code for this is in the function **find_boundary(original_img,img,show  =  True):** which can be found in the file   **sudoku_detector.py**.
 The image of the sample sudoku after this step:
  < insertimage >
 ### 5.Cropping and Warping
Next I wrote a function that crops the sudoku's bounding box from the rest of the image and gives us a top-down view.For this I made use of two OpenCV commands:
```
image_perspective = cv2.getPerspectiveTransform(box_array,destination_pts)
image_warped = cv2.warpPerspective(original_img,image_perspective,(int(max_side),int(max_side))

```
The detailed code for this can be found in the function **crop_and_warp(original_img,img,box_array,show  =  True):** in the file **sudoku_detector.py**.
The image of the sample sudoku after this step:
  < insertimage >
  ### 6. Extracting Digits  From the Sudoku Grid
 In order to perform this step, I reshaped the input image to 360x360 before extracting the digit followed by which I changed its colorspace from BGR to Grayscale using:
   ```
 image_gray  =  cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  ```
  Next I extracted the box using image coordinates which are given as an input to the function digit_extraction(img,position,img_size,grid_size,extracted_img_size,show  =  True).
  The code for this part is:
   ```
image_processed = image_gray

block_size_h = img_size[0]//grid_size[0]
block_size_w = img_size[1]//grid_size[1]

h_i = block_size_h*(position[0]) 
h_f = h_i + block_size_h 
w_i = block_size_w*(position[1]) 
w_f = w_i + block_size_w 

digit = image_processed[h_i:h_f,w_i:w_f] 
 
   ```
  Once the box is extracted the next step is to perform some preprocessing before it is sent to the model for digit recognition.
  The steps to perform the preprocessing were:
   #### 1. Otsu Thresholding:
 Otsu's method avoids having to choose a threshold value and determines it automatically by determining an optimal global threshold value from the image histogram.
 ```
 digit  =  cv2.threshold(digit,0,255, cv2.THRESH_BINARY_INV  |  cv2.THRESH_OTSU)[1]
 ```
 #### 2.Clearing the border
 The cropped out boxes have some part of the grid border in it which might interfere with the digit recognition process.Hence the border was cleared using:
 ```
 digit  =  clear_border(digit)
 ```
 #### 3. Masking the image:
 This step involves finding the largest contour in the box, if it exists and then drawing that contour on the mask. The code for this part is:
 ```
 digit_contours = cv2.findContours(digit.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#finding the contours

digit_contours = imutils.grab_contours(digit_contours) #adds a counter to the contour

if len(digit_contours)!=0:
	digit_contour = max(digit_contours, key=cv2.contourArea)
	background = np.zeros(digit.shape,dtype = np.uint8)
	cv2.drawContours(background,[digit_contour],-1,255,-1) 
	digit = cv2.bitwise_and(digit,digit, mask=background) 
 ```
 
 The entire code to this section can be found in the 
 **digit_extraction(img,position,img_size,grid_size,extracted_img_size,show  =  True)** which can be found in the file   **sudoku_detector.py**.

## Training the Model for Digit Recognition

## Solving the Sudoku

## Displaying the Solution
