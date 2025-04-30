from ultralytics import YOLO
import os

class Predict:
    def __init__(self, model, image, user_classes):
        self.model = model
        self.image = image
        self.user_classes = user_classes

    def predict(self):
        base_dir = os.path.dirname(__file__)
        weights_path = os.path.join(base_dir, "best.pt")

        if self.model == "yolov8s":
            weights_path = os.path.join(base_dir, "best.pt")
        elif self.model == "yolov8m":
            weights_path = os.path.join(base_dir, "last.pt")
        elif self.model == "yolov8x":
            weights_path = os.path.join(base_dir, "epoch25.pt")

        model = YOLO(weights_path)
        # model = YOLO("best.pt")

        # Define custom classes
        model.set_classes(self.user_classes)

        # Execute prediction for specified categories on an image
        results = model.predict(self.image)

        return results
