import stag
import cv2
import numpy as np

# load image
image = cv2.imread("example.jpg")

# detect markers
(corners, ids, rejected_corners) = stag.detectMarkers(image, 21)

img_out = image

# draw detected markers
for bounding_box, id in zip(corners, ids):
    bounding_box = np.round(bounding_box[0]).astype(int)
    green = (50, 255, 50)
    red = (0, 0, 255)
    white = (255, 255, 255)

    center = tuple(np.round(np.mean(bounding_box, axis=0)).astype(int))

    # draw white circle at top-left corner
    img_out = cv2.circle(img_out, bounding_box[0], 6, white, -1, cv2.LINE_AA)
    # draw white border
    for i in range(4):
        img_out = cv2.line(img_out, tuple(map(int, bounding_box[i])), tuple(map(int, bounding_box[(i+1)%4])), white, 3, cv2.LINE_AA)

    # draw green circle at top-left corner
    img_out = cv2.circle(img_out, bounding_box[0], 5, green, -1, cv2.LINE_AA)
    # draw green border
    for i in range(4):
        img_out = cv2.line(img_out, tuple(map(int, bounding_box[i])), tuple(map(int, bounding_box[(i+1)%4])), green, 2, cv2.LINE_AA)

    # draw white circle at center
    img_out = cv2.circle(img_out, center, 6, white, -1, cv2.LINE_AA)
    # draw green circle at center
    img_out = cv2.circle(img_out, center, 6, green, -1, cv2.LINE_AA)

    img_out = cv2.putText(img_out, f"{id}", center, cv2.FONT_HERSHEY_DUPLEX, 2, white, 5, cv2.LINE_AA)
    img_out = cv2.putText(img_out, f"{id}", center, cv2.FONT_HERSHEY_DUPLEX, 2, red, 2, cv2.LINE_AA)

# draw rejected quads
for bounding_box in rejected_corners:
    bounding_box = np.round(bounding_box[0]).astype(int)
    purple = (255, 0, 255)
    white = (255, 255, 255)

    center = tuple(np.round(np.mean(bounding_box, axis=0)).astype(int))

    # draw white border
    for i in range(4):
        img_out = cv2.line(img_out, tuple(map(int, bounding_box[i])), tuple(map(int, bounding_box[(i+1)%4])), white, 3, cv2.LINE_AA)

    # draw purple border
    for i in range(4):
        img_out = cv2.line(img_out, tuple(map(int, bounding_box[i])), tuple(map(int, bounding_box[(i+1)%4])), purple, 2, cv2.LINE_AA)


cv2.imwrite("example_result.jpg", img_out)
print("Detected Corners: ", corners)
print("Detected Ids: ", ids)
print("Results are visualized in example_result.jpg")

