import csv
import numpy as np
from GenderRecognitionFramework.training.corruptions import *
from GenderRecognitionFramework.training.ferplus_aug_dataset import *
from GenderRecognitionFramework.dataset.face_detector import FaceDetector as fd

"""Utility functions"""


def read_csv(csv_file_path):
    """Opens a csv whose path is given as input and has format [path,age] and gives a list of couples [path,age]"""
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        age_paths = []
        count = 0
        for row in reader:

            count = count + 1
            if count % 50000 == 0:
                print(str(count) + " rows have been read")
            if row == ['path', 'age']:
                continue
            age_paths.append(row)

        print("all of " + str(count) + " rows have been read")

    return age_paths


def write_csv(output, to_write):
    """given a list of couples [path,age] writes from scratch a csv in the output location"""
    with open(output, 'w', newline='') as file:
        fieldnames = ['path', 'age']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        count = 0

        for el in to_write:

            count = count + 1
            if count % 50000 == 0:
                print(str(count) + " rows have been written")

            writer.writerow({'path': el[0], 'age': el[1]})
        print("all of " + str(count) + " rows have been written")


def append_csv(output, toWrite):
    """given a list of couples [path,age] appends its content to a csv in the output location"""
    with open(output, 'a', newline='') as file:
        fieldnames = ['path', 'age']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        count = 0

        for el in toWrite:

            count = count + 1
            if count % 1000 == 0:
                print(str(count) + " rows have been written")

            writer.writerow({'path': el[0], 'age': el[1]})
        print("all of " + str(count) + " rows have been written")


def detect(image_path, size):
    """given an image path and an output size via Mivia's Face Detector it detects, crops, resize gives back a face"""
    img = cv2.imread(image_path)
    detector = fd(min_confidence=0.9)
    image = np.array(img)
    results = detector.detect(image)
    if len(results) != 0:
        """in case more faces have been detected biggest face is chosen"""
        image_return = results[0]["img"]
        biggest = image_return.shape
        for i in range(0, len(results)):
            if len(results[i]["img"]) != 0 and results[i]["img"].shape[0] != 0 and results[i]["img"].shape[1] != 0:
                if results[i]["img"].shape > biggest:
                    biggest = results[i]["img"].shape
                    image_return = results[i]["img"]
        if len(image_return) != 0 and image_return.shape[0] != 0 and image_return.shape[1] != 0:
            image_return = cv2.resize(image_return, size, cv2.INTER_AREA)
            return image_return
        else:
            """if no face is detected it returns None"""
            return None


def augment(to_augment, root):
    """
    Summary line.

    it reads images and (assuming their order has been already shuffled) via a predetermined sequence of corruptions
    it modifies them, prints them and updates thei current path

    Parameters
    ----------
    to_augment : []
        a list of an already read [path,age] csv
    root : str
        root where images are and where write new ones too

    Returns
    -------
    int
        an updated version of the input list where path is now referred to each modified image

    """
    for i in range(0, len(to_augment)):
        path_image = to_augment[i][0]
        image = np.array(cv2.imread(root + "/" + path_image))

        if image is None or image.ndim == 0:
            continue

        case = i % 4
        if case == 0:
            image = contrast_plus(image, severity=3)
        elif case == 1:
            image = brightness_plus(image, severity=4)
        elif case == 2:
            image = brightness_minus(image, severity=5)
        elif case == 3:
            image = gaussian_blur(image)

        if i % 1000 == 0:
            print( str(i) + " image(s) have been modified and augmented")
        new_path = "augment/" + str(i) + path_image.split("/")[1]
        cv2.imwrite(root + "/" + new_path, image)

        to_augment[i][0] = new_path

    return to_augment
