
# Sudoku Solver App

## Overview
The Sudoku Solver  is a project that makes use of Computer Vision to solve a sudoku puzzle. It takes an image of the sudoku puzzle as the input and generates the solved sudoku as the output.

## Frameworks used
This project is mainly written in Python and uses frameworks like PyTorch and OpenCV for training of the model and image preprocessing.

## Parts of the Project
1.[Image preprocessing for the input sudoku](#image-preprocessing-for-the-input-sudoku)\
2.[Training the model for digit recognition](#training-the-model-for-digit-recognition)\
3.[Solving the Sudoku](#solving-the-sudoku)\
4.[Displaying the solution](#displaying-the-solution)


## Image Preprocessing for the Input Sudoku
The image preprocessing is done by using OpenCV. Images of the sudoku taken need to be heavily preprocessed before each digit can be classified by the classification model. 
Let us take an example of a sample sudoku :
<  image>
The procedure I followed for preprocessing is:
 ### 1. Converting the Colorspace from BGR to Grayscale
 The OpenCV command used for this was :
 ```
 image_gray  =  cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  ```
 ### 2. Gaussian blur
 I applied a Gaussian blur to the input Sudoku image with a kernel size 7 and standard deviation of  3 to reduce noise in the image
 The OpenCV command used for this was :
 ```
 image_blur  =  cv2.GaussianBlur(image_gray,(7,7),3)
  ```
  ### 3. Adaptive Thresholding
Thresholding is an operation that works such that if the pixel value is smaller than the threshold, it is set to 0, otherwise it is set to a maximum value.
 Adaptive threshold method where the threshold value is calculated for smaller regions. Max pixel value to be given after thresholding is 255 ( white color)
 * ADAPTIVE_THRESH_GAUSSIAN_C − Threshold value is the weighted sum of neighborhood values where weights are a Gaussian window.
* cv2.THRESH_BINARY_INV - Inverts the case of binary thresholding

 The OpenCV command used for this was :
 ```
 image_threshold  =  cv2.adaptiveThreshold(image_blur, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
  ```
  

## Training the Model for Digit Recognition

## Solving the Sudoku

## Displaying the Solution

