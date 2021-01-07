import tensorflow as tf
import csv
import pathlib
import numpy as np
import random
import _util_prepare_ as util
import os
import shutil


"""given some csvs it reads imges, detects face, puts image on it and adds it to one of n tfrecord files"""

"""FUNDAMENTAL ARGS"""
"""
[WARNING]
root is where to find dataset
if it's the first time you run this code,
write your relative dataset path here
"""
#root = "./../../complete_test"
root = "./ultra_lite_train"
"""where to find original csvs to work with"""
"""WG:this script is very slow, I do not suggest to read all csv at once but to indicate a 'cache folder'
for a bunch of csvs"""
output = "./tf_records"
"""size to resize each image to"""
size = 96

"""number of tf records to organize test set in"""
number_tfs = 4

tf.executing_eagerly()



"""SUPPORT FUNCTIONS"""
"""it is useless to put all of those in util py file those are created only to keep the code readable"""

"""All raw values should be converted to a type compatible with tf.Example."""


def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))



def tfRecordCreator(folder,to_store,name,size):
    """
          Summary line.

          it reads images, detects faces, resizes them, puts them in a tfrecord

          Parameters
          ----------
          folder : str
              a path for an output folder to write to
          to_store : []
              a list of couples [path,age] to read from
          name : str
              a name for the resultant tfrecord file
          size : int
              desired dimension (size*size)


          Returns
          -------
          int
              a tf record with extracted faces and their original relative file path

    """


    num_img = 0
    print("from " + str(name))
    tfrecord_writer = tf.io.TFRecordWriter(folder + "/" + name + ".tfrecords")
    for elem in to_store:
        num_img = num_img +1
        img_path = elem
        relative_path = img_path.split("\\")[-2]+ "/" +img_path.split("\\")[-1]
        face = util.detect(img_path, (size,size))



        if face is None:
            num_img = num_img -1
            continue
        image_string = face.tobytes()
        relative_bytes = (relative_path.encode())

        example = tf.train.Example(features=tf.train.Features(feature={
              'image': _bytes_feature(image_string),
              'relative_path': _bytes_feature(relative_bytes),
        }))
        tfrecord_writer.write(example.SerializeToString())
        if num_img % 1000 == 0 :
            print("for "+name+" tfrecord "+str(num_img)+" images have been written")
        # close writer
    tfrecord_writer.close()
    print(name +" tfrecord contains images " + str(num_img))




def read_image_paths_from_root(root,n_chunks):
    """it reads each image from a given root and gives it in output organized in equal [n_chunks] chunks"""
    test = pathlib.Path(root)
    images = []
    i = 0
    for path in test.iterdir():
        if path.is_dir():
            for image in path.iterdir():
                if image.is_file():
                    images.append(str(image))
                    i = i+1
                    if i%10000==0:
                        print(str(i)+" images have been detected")

    print(str(i) + " images have been detected")

    random.shuffle(images)

    size_chunk = int(len(images) / n_chunks)
    img_chunks = [images[i:i + size_chunk] for i in range(0, len(images), size_chunk)]


    if len(img_chunks) > n_chunks :
        img_chunks[n_chunks-1] = img_chunks[n_chunks-1] + img_chunks[n_chunks]

    return img_chunks[:n_chunks]



"""BEGINNING OF THE SCRIPT"""
if not os.path.isdir(root):
    print("modify root constant in the code with your relative path to testset root")
    exit(404)

if os.path.isdir(output):
    shutil.rmtree(output)

os.mkdir(output)

img_chunks = read_image_paths_from_root(root, number_tfs)
for idx, chunk in enumerate(img_chunks):
    tfRecordCreator(output, chunk, "test"+str(idx),size)





print("END.")