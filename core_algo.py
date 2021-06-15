import sys, os, numpy, math

try: # Pillow
  from PIL import Image
except:
  print 'Error: Pillow has not been installed.'
  sys.exit(0)

try: # PyOpenGL
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print 'Error: PyOpenGL has not been installed.'
  sys.exit(0)


 def applyBrightnessAndContrast( brightness, contrast ):
	
  width  = currentImage.size[0]
  height = currentImage.size[1]

  srcPixels = tempImage.load()
  dstPixels = currentImage.load()
  
  # YOUR CODE HERE
  for i in range(width):
    for j in range(height):
        #obtain new intensity after adjusted contrast and brightness
        k = contrast * srcPixels[i,j][0] + brightness
        
        #put new intensity into destination pixel
        tmp = list(dstPixels[i,j])
        tmp[0] = int(round(k))
        dstPixels[i,j] = tuple(tmp)
  print 'adjust brightness = %f, contrast = %f' % (brightness,contrast)



  def performHistoEqualization( radius ):
	 
  pixels = currentImage.load()
  width  = currentImage.size[0]
  height = currentImage.size[1]

  # YOUR CODE HERE
  #make a copy of original image
  tmpImage = currentImage.copy()
  pixels_copy = tmpImage.load()
    
  #size of neighbourhood
  n = (2 * radius + 1) * (2 * radius + 1)

  for i in range(width):
    for j in range(height):
        #obtain start and end bounds of neighbourhood
        start_x = i - radius
        end_x = i + radius
        start_y = j - radius
        end_y = j + radius
        
        #moderate values that are out of bounds
        if (start_x < 0):
            start_x = 0
        if (start_y < 0):
            start_y = 0
        if (end_x > width - 1):
            end_x = width - 1
        if (end_y > height - 1):
            end_y = height - 1
        
        number = 0
        
        for a in range(start_x, end_x + 1):
            for b in range(start_y, end_y + 1):
                #find number of neighbouring pixels whose value is smaller than target pixel
                if pixels[a,b][0] <= pixels[i,j][0]:
                    number += 1
                
        new_pixel_val = (256/ n)* number + 0 - 1
        
        #put new intensity into pixels_copy
        tmp = list(pixels_copy[i,j])
        tmp[0] = int(round(new_pixel_val))
        pixels_copy[i,j] = tuple(tmp)
        
  #copy the temporary image to the original image      
  for i in range(width):
    for j in range(height):
      pixels[i,j] = pixels_copy[i,j]
      
  print 'perform local histogram equalization with radius %d' % radius


def scaleImage( factor ):
	
  width  = currentImage.size[0]
  height = currentImage.size[1]

  srcPixels = tempImage.load()
  dstPixels = currentImage.load()

  #srcPixels2 = tempImage.load()
  new_width = int(width * factor)
  new_height = int(height * factor)

  # YOUR CODE HERE
  T = numpy.matrix([[factor, 0], [0, factor]])
  #obtain inverse matrix
  T_inv = numpy.linalg.inv(T)

  #center_width = int(math.floor(width / 2))
  #center_height = int(math.floor(height / 2))

  for i in range(width):
    for j in range(height):
        #using backward projection to obtain coordinates in original image
        new_coords = numpy.matrix([[i],[j]])
        original_coords = numpy.matmul(T_inv, new_coords)
        x = original_coords[0][0]
        y = original_coords[1][0]
        #x = x_1 - x_2
        #y = y_1 - y_4

        X = int(numpy.floor(x))
        Y = int(numpy.floor(y))
        
        _X = X + 1
        _Y = Y + 1
        
        #moderate values that are out of bounds
        if (X > width - 1):
            X = width - 1
            _X = width - 1
        elif (X < 0):
            X = 0
            _X = 0
        
        if (Y > height - 1):
            Y = height - 1
            _Y = height - 1
        elif (Y < 0):
            Y = 0
            _Y = 0

        #using bilinear interpolation
        #put new value of tuple into dstPixels
        alpha = x - X
        beta = y - Y
        
        tmp = list(dstPixels[i,j])
        for l in range(3):
          val = (1-alpha) * (1-beta) * srcPixels[X,Y][l] + (alpha) * (1-beta) * srcPixels[_X,Y][l] + (1-alpha) * (beta) * srcPixels[X,_Y][l] + (alpha) * (beta) * srcPixels[_X,_Y][l] 
          tmp[l] = int(val)
        
        dstPixels[i,j] = tuple(tmp)
  for w in range(new_width, width):
    for h in range(0, height):
      dstPixels[w, h] = (255, 128, 128)
  for n in range(0, width):
    for m in range(new_height, height):
      dstPixels[n, m] = (255, 128, 128)

  # original_center = numpy.matrix([[center_width],[center_height]])

  # new_center = numpy.matmul(T, original_center)

  # delta_x = int(center_width - new_center[0][0])
  # delta_y = int(center_height - new_center[1][0])



  # for w in range(width):
  #   for h in range(height):
  #     new_w = w + delta_x
  #     new_y = y + delta_y
  #     dstPixels[w, h] = srcPixels2[int(math.floor(w+new_w)), int(math.floor(y+new_y))]
  
  #currentImage = currentImage.transform(currentImage.size, Image.AFFINE, (1, 0, -delta_x, 0, 1, delta_y))

  print 'scale image by %f' % factor


