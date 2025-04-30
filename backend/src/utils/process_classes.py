from backend.src.constants.constants import coco_classes


def process_classes(user_input):
    # split the user input and identify the classes
    print("USER INPUT:", user_input)
    classes = user_input.split(" ")
    # remove whitespace
    classes = [cls.strip() for cls in classes]
    print("CLASSES:", classes)
    # check if the classes are in the coco_classes list
    classes = [cls for cls in classes if cls in coco_classes]
    return classes
