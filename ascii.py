"""
ascii.py
A python program that convert images to ASCII art.
"""
#import libraries
import argparse
import numpy as np
from PIL import Image;

def getAverageL(image): #Given PIL Image, return average value of greyscale value
    
   
    im = np.array(image)  # get input image as numpy array
    
    w,h = im.shape# get shape of array using shape 
    
    return np.average(im.reshape(w*h)) # get average of reshaped array

def convertImageToAscii(fileName, cols, scale, moreLevels):  #Given Image and dims (rows, cols) returns an m*n list of Images 
    
    # grey scale level values from: 
    # http://paulbourke.net/dataformats/asciiart/
    
    
    gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. " # 70 levels of grey 
    
    gscale2 = '@%#*+=-:. ' # 10 levels of grey 

    
    image = Image.open(fileName).convert('L') # open image in given file path and convert to greyscale 

   
    W, H = image.size[0], image.size[1]  # store dimensions of image using size method 
    print("input image dims: %d x %d" % (W, H))
    # compute width of tile/column
    w = W / cols
   
    h = w / scale  # compute tile/row height based on aspect ratio and scale
  
    rows = int(H / h)   # compute number of rows 

    # print statements tell dimensions of the image and of the tiles
    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))
    
    
    if cols > W or rows > H: # check if image size is too small for given cols or rows
        print("Image too small for specified cols!")
        exit(0)
        
    
   
    aimg = []  # ascii image - list of character strings

    
    
    for j in range(rows):# generate list of dimensions using nested for loop
        # y1 pattern: 0, h, 2h, 3h, ...; y2 pattern: h, 2h, 3h, 4h, ...
        y1 = j*int(h)
        y2 = (j+1)*int(h)
       
        if j == rows-1:  # correct last tile
            y2 = H
        
        aimg.append("")# append an empty string
        for i in range(cols):
            
            x1 = i*int(w) # crop image to tile
            x2 = (i+1)*int(w)
           
            if i == cols-1:  # correct last tile
                x2 = W
           
            img = image.crop((x1, y1, x2, y2))  # crop image to extract tile

            
            avg = int(getAverageL(img)) # get average luminance of cropped tile 
           
            if moreLevels:  # look up ascii char by generating a string index based on avg
                gsval = gscale1[int((avg*69/255))]
            else:
                gsval = gscale2[int((avg*9/255))]
          
            aimg[j] += gsval   # append ascii char to string
    
   
    return aimg   # return txt image as a list of strings (1 string = 1 row of text file)
  
    

def main():
    
    descStr = "This program converts an image into ASCII art." # creates a command line parser object using built-in argparse library
    parser = argparse.ArgumentParser(description=descStr)
    # add arguments 
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--morelevels',dest='moreLevels',action='store_true')

   
    args = parser.parse_args()  # parse args, stores ALL user input as strings
    
    imgFile = args.imgFile
   
    outFile = 'out.txt'  # set default output file
   
    # check if an input is entered for outFile
    if args.outFile:
        outFile = args.outFile  # Rewrite default value with user value
        
    
    scale = 0.43 # set scale default as 0.43 - should always be a float
    if args.scale:
        scale = float(args.scale)
    
    cols = 80 # set default cols as 80 - should always be an int
    if args.cols:
        cols = int(args.cols)

    print('generating ASCII art...')
    
    aimg = convertImageToAscii(imgFile, cols, scale, args.moreLevels) # convert image to ascii txt

   
    f = open(outFile, 'w')  # open output file in write mode
    
    for k in aimg: # write to file using aimg and the for loop
        f.write(k + '\n')
    # cleanup
    f.close()
    print("ASCII art written to %s" % outFile)

    


# call main
if __name__ == '__main__':
    main()
