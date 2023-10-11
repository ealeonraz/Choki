import os
import cv2

# Load image, grayscale, Gaussian blur, Otsu's threshold
def crop_image(path):
    # Load the image using OpenCV
    im = cv2.imread(path)
    original = im.copy()  # Create a copy of the original image

    # Convert the image to grayscale
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the grayscale image
    blur = cv2.GaussianBlur(gray, (25, 25), 0) #25 x 25 kernel, 0 indicates OpenCV will choose the standard deviation based on kernel size

    # Apply Otsu's thresholding to the blurred image combined with binary inversion based on otsus threshold
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] # 0 - minval set to maxval which is 255 (White), flag is set to INV binary and OTSUs threshold

    # Perform morphological operations to further process the image
    nKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)) #Create a rectangle that is 3x3 pixels used for morphology 
    #Morphological opening is applied using the 3x3 rectangle as the structuring element, first erodes the image then dilate the eroded image
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, nKernel, iterations=2)

    #Morphological closing is applied on the previous "open" image
    cKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)) # 7x7 structuring element
    #Morphological closing is applied to openming using the 7x7 structuring element 3 times
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, cKernel, iterations=3)

    # Find the bounding box and crop the region of interest
    coords = cv2.findNonZero(close) #Find all non-zero (white) pixels in the 'close' image
    x, y, w, h = cv2.boundingRect(coords) #Calculates the bounding rectangle (Smallest) that can enclose all the points from coords
    cv2.rectangle(im, (x, y), (x + w, y + h), (36, 255, 12), 2) #Draws the rectangle on the original image using the bounding box coordinates
    crop = original[y:y+h, x:x+w]  # Crop the original image based on the rectangle
    return crop

# Loops through a directory and performs the crop_image function on all images within that directory
def dir_loop(folder):
    path = "./im_output"  # Output directory for cropped images
    count = 0  # Initialize a count for naming the output images

    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        file = "%s/%s" % (folder, filename)
        fileFL = f"im{count}.jpg"  # Name the output file based on the count
        count += 1

        # Crop the image and save the cropped image
        cropped_image = crop_image(file)
        cv2.imwrite(os.path.join(path, fileFL), cropped_image)