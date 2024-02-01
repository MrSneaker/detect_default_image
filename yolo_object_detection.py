import cv2 as cv
import numpy as np
from wandb import Classes

# load yolo
net = cv.dnn.readNet("yolov3_custom_last.weights",
                     "yolov3_custom.cfg")
clasees = []
with open("data/obj.names", 'r') as f:
    classes = [line.strip() for line in f.readlines()]
# print(classes)
layer_name = net.getLayerNames()
output_layer = [layer_name[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Load Image
img = cv.imread("DATASET_Sujet2/Defaut/image_300_ST_Sup_Pli.png")
img = cv.resize(img, None, fx=0.4, fy=0.4)
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
        if confidence > 0.4:
            # Object detection
            print(confidence)
            print(str(class_id))
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width) if detection[2] * width > 0 else 1  # Avoid division by zero
            h = int(detection[3] * height)
            x = int(center_x - w/2)
            y = int(center_y - h/2)
            boxes.append([x, abs(y), w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)
            break
print(len(boxes))
print(boxes[0])
number_object_detection = len(boxes)

indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

print("Indexes:", indexes)

font = cv.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    print("Current i:", i)
    # if i in indexes:
    x, y, w, h = boxes[i]
    label = str(classes[class_ids[i]])
    print(f"Box {i}: ({x}, {y}, {w}, {h}), Label: {label}")
    color = colors[i]
    cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
    cv.putText(img, label, (x, y + 30), font, 3, color, 3)

cv.imshow("IMG", img)
while True:
    key = cv.waitKey(1)
    if cv.getWindowProperty("IMG", cv.WND_PROP_VISIBLE) < 1:
        break
    if key != -1:
        break

cv.destroyAllWindows()
