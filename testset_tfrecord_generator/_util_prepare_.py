import csv
import numpy as np
from GenderRecognitionFramework.training.corruptions import *
from GenderRecognitionFramework.training.ferplus_aug_dataset import *
from imutils.face_utils import FaceAligner
import dlib
import imutils
from imutils.face_utils import rect_to_bb
from GenderRecognitionFramework.dataset.face_detector import FaceDetector as fd

########### FX UTILITA' #############
def read_csv(csv_file_path):



    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)

        agepaths = []
        count = 0
        for row in reader:

            count = count+1
            if count % 50000 == 0 :
                print(str(count)+" rows have been read")


            if row == ['path', 'age']:
                continue
            agepaths.append(row)

        print("all of "+str(count)+ " rows have been read")

    return agepaths


def write_csv(output, toWrite):

    with open(output, 'w', newline='') as file:
        fieldnames = ['path', 'age']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        #writer.writeheader()
        count = 0

        for el in toWrite:

            count = count + 1
            if count % 50000 == 0:
                print(str(count) + " rows have been written")

            writer.writerow({'path': el[0], 'age': el[1]})
        print("all of " + str(count) + " rows have been written")

def append_csv(output, toWrite):

    with open(output, 'a', newline='') as file:
        fieldnames = ['path', 'age']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        #writer.writeheader()
        count = 0

        for el in toWrite:

            count = count + 1
            if count % 1000 == 0:
                print(str(count) + " rows have been written")

            writer.writerow({'path': el[0], 'age': el[1]})
        print("all of " + str(count) + " rows have been written")


def align_image(image_path,size):
  detector = dlib.get_frontal_face_detector()
  predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")
  fa = FaceAligner(predictor, desiredFaceWidth=size)
  image = cv2.imread(image_path)
  #image = imutils.resize(image, width=500)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  rects = detector(gray, 2)
  faceAligned = None
  for rect in rects:
    # extract the ROI of the *original* face, then align the face
    # using facial landmarks
    try:
      (x, y, w, h) = rect_to_bb(rect)
      faceOrig = imutils.resize(image[y:y + h, x:x + w], width=128)
      faceAligned = fa.align(image, gray, rect)

    except:
     # print("CANNOT SAVE")

      continue
  return faceAligned

def detect(image_path, size):
  img = cv2.imread(image_path)
  detector=fd(min_confidence=0.9)
  image=np.array(img)
  results=detector.detect(image)
  if len(results) !=0:
    image_return=results[0]["img"]
    max=image_return.shape
    for i in range(0,len(results)):
      if len(results[i]["img"]) !=0 and results[i]["img"].shape[0] !=0 and results[i]["img"].shape[1] != 0:
        if (results[i]["img"].shape >max):
          #print(max)
          max=results[i]["img"].shape
          image_return=results[i]["img"]
    if (len(image_return)!=0 and image_return.shape[0] !=0 and image_return.shape[1] != 0):
      image_return = cv2.resize(image_return,size, cv2.INTER_AREA)
      return image_return
    else:
      return None

def augment(_toAugment,root,default_dim):
    for i in range(0, len(_toAugment)):
        path_image = _toAugment[i][0]
        image = np.array(cv2.imread(root + "/" + path_image))

        #image= align_image(root+"/"+path_image,default_dim)

        if image is None:
            continue

        case = i % 4
        if case == 0:
            image = contrast_plus(image,severity=3)
        elif case == 1:
            image = brightness_plus(image, severity=4)
        elif case == 2:
            image = brightness_minus(image, severity=5)
        elif case == 3:
            image = gaussian_blur(image)

        if i%1000 == 0:
            print("modificate "+str(i)+" immagini")
        newpath = "augment/" + str(i) + path_image.split("/")[0]
        cv2.imwrite(root+"/"+newpath, image)

        _toAugment[i][0] = newpath
    # salva nuove immagini in cartella temporanea e restituisce il path dentro store
    # per ora non fa nulla e restituisce solo _toAugment

    return _toAugment
