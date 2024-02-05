import cv2 as cv
import numpy as np
from wandb import Classes

# load yolo
net = cv.dnn.readNet("yolov3_custom_final.weights",
                     "yolov3_custom.cfg")
clasees = []
with open("data/obj.names", 'r') as f:
    classes = [line.strip() for line in f.readlines()]
print(classes)
layer_name = net.getLayerNames()
output_layer = [layer_name[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Load Image
img = cv.imread("DATASET_Sujet2/Defaut/image_104_SL.png")
# img = cv.imread("DATASET_Sujet2/Sans_Defaut/image_69923_rotated.png")
height, width, channel = img.shape

# Detect Objects
blob = cv.dnn.blobFromImage(
    img, 0.00392, (32, 32), (0, 0, 0), True, crop=False)
net.setInput(blob)
outs = net.forward(output_layer)

# Showing Information on the screen
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        print(confidence)
        if confidence > 0.0:
            # Object detection
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w/2)
            y = int(center_y - h/2)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

number_object_detection = len(boxes)

font = cv.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    x, y, w, h = boxes[i]
    label = str(classes[class_ids[i]])
    confidenceStr = 'conf: ' + "{:.5f}".format(confidences[i])
    print(f"Box {i}: ({x}, {y}, {w}, {h}), Label: {label}")
    color = colors[i]
    cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
    cv.putText(img, label, (x + 15, y + 55), font, 2, color, 1)
    cv.putText(img, confidenceStr, (x + 15, y + 75), font, 2, color, 1)

cv.imshow("IMG", img)
while True:
    key = cv.waitKey(1)
    if cv.getWindowProperty("IMG", cv.WND_PROP_VISIBLE) < 1:
        break
    if key != -1:
        break

cv.destroyAllWindows()
