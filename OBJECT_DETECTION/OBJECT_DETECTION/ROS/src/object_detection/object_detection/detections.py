import rclpy
from rclpy.node import Node

from interfaces.msg import DetectionList

import numpy as np
import cv2

class DetectionSubscriber(Node):

    def __init__(self):
        super().__init__('detection_subscriber')
        self.subscriber = self.create_subscription(DetectionList, '/detections', self.detections_callback, 10)

        self.classes = {
            0: "Container",
            1: "TrashBag",
            2: "RubbleBag",
            3: "WoodTrash"
        }

        self.colors = {
            0: (91, 175, 181),
            1: (91, 181, 112),
            2: (191, 100, 67),
            3: (227, 141, 208)
        }

        print("Ready!")

    def detections_callback(self, msg):

        np_arr = np.frombuffer(msg.image.data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        for detection in msg.detections:
            
            if detection.label == -1:
                break

            point_min = (int(image.shape[1] * detection.xmin), int(image.shape[0] * (1 - detection.ymin)))
            point_max = (int(image.shape[1] * detection.xmax), int(image.shape[0] * (1 - detection.ymax)))

            image = cv2.rectangle(image, point_min, point_max, self.colors[detection.label], 2)
            #image = cv2.putText(image, detection.label, (point_min[0], point_max[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (32, 32, 32), 1)
            #cv2.imwrite("./image.jpg", image)

        cv2.imshow("Object Detection", image)
        cv2.waitKey(1)


    

def main(args=None):
    
    rclpy.init(args=args)

    detection_subscriber = DetectionSubscriber()

    rclpy.spin(detection_subscriber)

    detection_subscriber.destroy_node()
    rclpy.shutdown()
