import cv2 as cv
import numpy as np
import os

class ObjectDetector:
    def __init__(self, weights_file, config_file, names_file):
        self.net = cv.dnn.readNet(weights_file, config_file)
        self.classes = []
        with open(names_file, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def detect_objects(self, image_path):
        img = cv.imread(image_path)
        height, width, channel = img.shape

        blob = cv.dnn.blobFromImage(img, 0.00392, (32, 32), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.0:
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

        for i in range(len(boxes)):
            x, y, w, h = boxes[i]
            label = str(self.classes[class_ids[i]])
            confidenceStr = 'conf: ' + "{:.5f}".format(confidences[i])
            color = self.colors[i]
            cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv.putText(img, label, (x + 15, y + 55), cv.FONT_HERSHEY_PLAIN, 2, color, 1)
            cv.putText(img, confidenceStr, (x + 15, y + 75), cv.FONT_HERSHEY_PLAIN, 2, color, 1)

        return img

    def detect_objects_and_save(self, image_path, output_path):
        output_image = self.detect_objects(image_path)
        # cv.imshow("IMG", output_image)
        output_directory = os.path.dirname(output_path)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
            print(f"Created directory: {output_directory}")

        # Save the image
        success = cv.imwrite(output_path, output_image)
        if success:
            print(f"Image saved to: {output_path}")
        else:
            print(f"Failed to save image to: {output_path}")
        cv.imwrite(output_path, output_image)
