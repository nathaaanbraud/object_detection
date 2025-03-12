import os
import sys
import cv2
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.detection.light.lowlight_test import enhance_image

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

# Construct the absolute paths for the images
frame_ref_cam4_path = os.path.join(project_dir, "images/frame_ref_cam4_light.jpg")
frame_ref_cam5_path = os.path.join(project_dir, "images/frame_ref_cam5_light.jpg")
frame_ref_cam7_path = os.path.join(project_dir, "images/frame_ref_cam7_light.jpg")
frame_ref_cam8_path = os.path.join(project_dir, "images/frame_ref_cam8_light.jpg")

# Load reference frames using the absolute paths
frame_ref_cam4 = cv2.imread(frame_ref_cam4_path)
frame_ref_cam5 = cv2.imread(frame_ref_cam5_path)
frame_ref_cam7 = cv2.imread(frame_ref_cam7_path)
frame_ref_cam8 = cv2.imread(frame_ref_cam8_path)


"""
Description: Matches the camera number to the corresponding reference frame.
Inputs:
    - camera: The camera number (int).
Outputs:
    - frame_ref: The reference frame corresponding to the camera number (numpy array).
"""
def match_frame_reference(camera):
    match camera:
        case 4:
            frame_ref = frame_ref_cam4
        case 5:
            frame_ref = frame_ref_cam5
        case 7:
            frame_ref = frame_ref_cam7
        case 8:
            frame_ref = frame_ref_cam8
        case _:
            print("Erreur : Camera non reconnue")
            exit()
    return frame_ref


"""
Description: Draws a parallelogram on the given image.
Inputs:
    - image: The image on which to draw the parallelogram (numpy array).
    - pts: The points defining the parallelogram (list of tuples).
    - color: The color of the parallelogram (tuple of BGR values).
    - thickness: The thickness of the parallelogram lines (int).
Outputs: None
"""
def draw_parallelogram(image, pts, color, thickness):
    pts = np.array(pts, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(image, [pts], isClosed=True, color=color, thickness=thickness)


"""
Description: Defines the coordinates of the occlusion zones for a given camera.
Inputs:
    - camera: The camera number (4,5,7 or 8).
Outputs:
    - coord: A list of lists, where each inner list contains four tuples representing the coordinates of a parallelogram.
"""
def define_coordinates_parallelograms(camera):
    coord = []
    match camera:
        case 4:
            x1, y1, x2, y2 = 730, 90, 1020, 100 # (x1, y1) top left, (x2, y2) top right of the parallelogram
            x3, y3, x4, y4 = 1098, 120, 1250, 138
            x5, y5, x6, y6 = 0, 0, 210, 0
            x7, y7, x8, y8 = 400, 90, 690, 80
            x9, y9, x10, y10 = 565, 150, 700, 150
            x11, y11, x12, y12 = 380, 160, 460, 160
            coord.append([(x1, y1), (x2, y2), (x2, y2 + 330), (x1, y1 + 245)]) # (top left, top right, bottom right, bottom left) coordinates of the parallelogram
            coord.append([(x3, y3), (x4, y4), (x4, y4 + 390), (x3, y3 + 370)])
            coord.append([(x5, y5), (x6, y6), (x6, y6 + 800), (x5, y5 + 800)])
            coord.append([(x7, y7), (x8, y8), (x8, y8 + 70), (x7, y7 + 67)])
            coord.append([(x9, y9), (x10, y10), (x10, y10 + 175), (x9, y9 + 135)])
            coord.append([(x11, y11), (x12, y12), (x12, y12 + 65), (x11, y11 + 60)])
        case 5:
            x1, y1, x2, y2 = 795, 90, 1065, 100
            x3, y3, x4, y4 = 1125, 120, 1275, 155
            x5, y5, x6, y6 = 455, 75, 750, 75
            x7, y7, x8, y8 = 0, 0, 210, 0
            x9, y9, x10, y10 = 620, 130, 655, 130
            x11, y11, x12, y12 = 425, 140, 515, 140
            coord.append([(x1, y1), (x2, y2), (x2, y2 + 325), (x1, y1 + 230)])
            coord.append([(x3, y3), (x4, y4), (x4, y4 + 378), (x3, y3 + 350)])
            coord.append([(x5, y5), (x6, y6), (x6, y6 + 50), (x5, y5 + 60)])
            coord.append([(x7, y7), (x8, y8), (x8, y8 + 800), (x7, y7 + 800)])
            coord.append([(x9, y9), (x10, y10), (x10, y10 + 145), (x9, y9 + 135)])
            coord.append([(x11, y11), (x12, y12), (x12, y12 + 70), (x11, y11 + 35)])
        case 7:
            x1, y1, x2, y2 = 770, 90, 1040, 100
            x3, y3, x4, y4 = 1125, 120, 1265, 147
            x5, y5, x6, y6 = 425, 75, 730, 75
            x7, y7, x8, y8 = 0, 0, 210, 0
            x9, y9, x10, y10 = 610, 130, 645, 130
            x11, y11, x12, y12 = 415, 140, 500, 140
            coord.append([(x1, y1), (x2, y2), (x2, y2 + 320), (x1, y1 + 230)])
            coord.append([(x3, y3), (x4, y4), (x4, y4 + 378), (x3, y3 + 350)])
            coord.append([(x5, y5), (x6, y6), (x6, y6 + 50), (x5, y5 + 60)])
            coord.append([(x7, y7), (x8, y8), (x8, y8 + 800), (x7, y7 + 800)])
            coord.append([(x9, y9), (x10, y10), (x10, y10 + 145), (x9, y9 + 135)])
            coord.append([(x11, y11), (x12, y12), (x12, y12 + 70), (x11, y11 + 35)])
        case 8:
            x1, y1, x2, y2 = 800, 90, 900, 100
            x3, y3, x4, y4 = 675, 95, 744, 100
            x5, y5, x6, y6 = 1085, 140, 1279, 160
            x7, y7, x8, y8 = 901, 100, 1070, 115 
            x9, y9, x10, y10 = 0, 0, 210, 0
            x11, y11, x12, y12 = 355, 90, 524, 80
            coord.append([(x1, y1), (x2, y2), (x2, y2 + 190), (x1, y1 + 180)])
            coord.append([(x3, y3), (x4, y4), (x4, y4 + 174), (x3, y3 + 184)])
            coord.append([(x5, y5), (x6, y6), (x6, y6 + 360), (x5, y5 + 335)])
            coord.append([(x7, y7), (x8, y8), (x8, y8 + 330), (x7, y7 + 295)])
            coord.append([(x9, y9), (x10, y10), (x10, y10 + 800), (x9, y9 + 800)])
            coord.append([(x11, y11), (x12, y12), (x12, y12 + 40), (x11, y11 + 40)])
        case _:
            print("Erreur : Camera non reconnue")
            exit()
    return coord



"""
Description: Performs background subtraction to detect objects in a video frame using edge detection.
The difference between the current frame and the reference frame is displayed with
the detected differences in green and the exclusion zones in blue.
Inputs:
    - camera: The camera number (int).
    - frame_tested: The frame to be tested (numpy array).
Outputs: None
"""
def background_substraction_on_edges(camera, frame_tested):

    # Select the reference frame corresponding to the camera number 
    frame_ref = match_frame_reference(camera)
        
    # Luminosity treatment
    frame_cur_light = enhance_image(frame_tested)

    # --- ADD A BLUE RECTANGLE FOR EXCLUSION ZONES ---

    coord = define_coordinates_parallelograms(camera)

    # Define the points of the parallelograms
    parallelograms = []
    parallelos = []

    for points in coord:
        parallelogram = np.array(points, np.int32)
        parallelo = points
        parallelograms.append(parallelogram)
        parallelos.append(parallelo)
       
    
    # Convert to grayscale
    gray_ref = cv2.cvtColor(frame_ref, cv2.COLOR_BGR2GRAY)
    gray_cur = cv2.cvtColor(frame_cur_light, cv2.COLOR_BGR2GRAY)

    # Apply a blur to reduce noise
    gray_ref = cv2.GaussianBlur(gray_ref, (5,5), 0)
    gray_cur = cv2.GaussianBlur(gray_cur, (5,5), 0)

    # Apply Canny edge detection
    edges_ref = cv2.Canny(gray_ref, 200, 300) # (frame, minVal, maxVal)
    edges_cur = cv2.Canny(gray_cur, 200, 300)

    # Edge substraction
    diff = cv2.absdiff(edges_ref, edges_cur)

    # Threshold to detect significant differences
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)


    # Remove window zones (set pixels in this region to zero)
    for parallelogram in parallelograms:
        cv2.fillPoly(thresh, [parallelogram], 0)

    # Apply morphological operations to reduce noise
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Detect contours of present objects
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small objects
    min_size = 25  # (minimum size in pixels)
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_size ** 2]

    # Draw detected objects on the current image
    output = frame_tested.copy()
    for cnt in filtered_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)


    # Draw a blue rectangle on the image to visualize the exclusion zone
    for parallelo in parallelos:
        draw_parallelogram(output, parallelo, (255, 0, 0), 2)


    # Display the result
    cv2.imshow("Objets detectes", output)
    cv2.waitKey(0)

    # Release resources
    cv2.destroyAllWindows()



"""
Description: Performs background subtraction to detect objects in a video frame. 
The difference between the current frame and the reference frame is displayed with
the detected differences in green and the exclusion zones in blue.
Inputs:
    - camera: The camera number (int).
    - frame_tested: The frame to be tested (numpy array).
Outputs: None
"""
def background_substraction(camera, frame_tested):

    # Select the reference frame corresponding to the camera number 
    frame_ref = match_frame_reference(camera)
    
     
    # Luminosity treatment
    frame_cur_light = enhance_image(frame_tested)


    # --- ADD A BLUE RECTANGLE FOR EXCLUSION ZONES ---

    coord = define_coordinates_parallelograms(camera)

    # Define the points of the parallelograms
    parallelograms = []
    parallelos = []

    for points in coord:
        parallelogram = np.array(points, np.int32)
        parallelo = points
        parallelograms.append(parallelogram)
        parallelos.append(parallelo)
       

        # Convert to grayscale for subtraction
        gray_ref = cv2.cvtColor(frame_ref, cv2.COLOR_BGR2GRAY)
        gray_cur = cv2.cvtColor(frame_cur_light, cv2.COLOR_BGR2GRAY)

        # Apply image subtraction
        diff = cv2.absdiff(gray_ref, gray_cur)

        # Threshold to detect significant differences
        _, thresh = cv2.threshold(diff, 75, 255, cv2.THRESH_BINARY)


    # Remove window zones (set pixels in this region to zero)
    for parallelogram in parallelograms:
        cv2.fillPoly(thresh, [parallelogram], 0)

    # Apply morphological operations to reduce noise
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Detect contours of present objects
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small objects
    min_size = 25  # (minimum size in pixels)
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_size ** 2]

    # Draw detected objects on the current image
    output = frame_tested.copy()
    for cnt in filtered_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)


    # Draw a blue rectangle on the image to visualize the exclusion zone
    for parallelo in parallelos:
        draw_parallelogram(output, parallelo, (255, 0, 0), 2)


    # Display the result
    cv2.imshow("Objets detectes", output)
    cv2.waitKey(0)

    # Release resources
    cv2.destroyAllWindows()
