import cv2
import numpy as np

# Start capturing the video using laptop webcam
cap = cv2.VideoCapture(0)

# Initialize Centroid
pre_cx = 0;
pre_cy = 0;

i = False;

# Creates an empty Canvas
img = np.zeros((512, 512, 3), np.uint8)


def nothing():
    pass

cv2.namedWindow('Colorbars')

# assign strings for ease of coding
hh = 'Hue High'
hl = 'Hue Low'
sh = 'Saturation High'
sl = 'Saturation Low'
vh = 'Value High'
vl = 'Value Low'
wnd = 'Colorbars'

# Begin Creating trackbars for each
cv2.createTrackbar(hl, wnd, 110, 179, nothing)
cv2.createTrackbar(hh, wnd, 130, 179, nothing)
cv2.createTrackbar(sl, wnd, 50, 255, nothing)
cv2.createTrackbar(sh, wnd, 255, 255, nothing)
cv2.createTrackbar(vl, wnd, 50, 255, nothing)
cv2.createTrackbar(vh, wnd, 255, 255, nothing)

while (1):
    # Take each frame
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # # read trackbar positions for each trackbar
    # hul = cv2.getTrackbarPos(hl, wnd)
    # huh = cv2.getTrackbarPos(hh, wnd)
    # sal = cv2.getTrackbarPos(sl, wnd)
    # sah = cv2.getTrackbarPos(sh, wnd)
    # val = cv2.getTrackbarPos(vl, wnd)
    # vah = cv2.getTrackbarPos(vh, wnd)
    #
    # # make array for final values
    # HSVLOW = np.array([hul, sal, val])
    # HSVHIGH = np.array([huh, sah, vah])

    # Array of HSV Bounds
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Mask the hsv to the image
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imshow("MASK", mask)

    # Reduce noise using Median Blur Filter
    median = cv2.medianBlur(mask, 5)
    cv2.imshow("MEDIAN", median)

    flipped_frame = cv2.flip(frame, 1)
    cv2.imshow('FRAME', flipped_frame)

    # Detect the contours and sorts them according to their area
    im2, contours, hie = cv2.findContours(median, 1, 2)
    cnt_sort = sorted(contours, key=cv2.contourArea, reverse=True)

    flip = cv2.flip(img, 1)

    # Find moments of the largest contour
    M = cv2.moments(cnt_sort[0])
    if M['m00'] != 0:
        if cv2.contourArea(cnt_sort[0]) > 1800.00:

            # Centroid of the object
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            if i:

                # Draw line from previous centroid to the new centroid of the object
                cv2.line(img, (pre_cx, pre_cy), (cx, cy), (255, 255, 255), 3)
                flip = cv2.flip(img, 1)
                cv2.imshow('image', flip)
            else:
                i = True
            pre_cy = cy
            pre_cx = cx
        else:
            i = False
            cv2.imwrite('photo.jpg', flip)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
