import tensorflow as tf
import csv
import pathlib
import numpy as np
import random
import _util_prepare_ as util


"""given some csvs it reads imges, detects face, puts image on it and adds it to one of n tfrecord files"""

"""FUNDAMENTAL ARGS"""
"""where to find original csvs to work with"""
"""WG:this script is very slow, I do not suggest to read all csv at once but to indicate a 'cache folder'
for a bunch of csvs"""
csv_root = "./__script_files/__4divided_csv_with_aug"
#csv_root = "./__script_files/cache_csvs"
"""where to find dataset"""
root = "./../../complete_train"
"""where to print csvs"""
output = "./__script_files/__5tf_records"
"""size to resize each image to"""
size = 96


"""SUPPORT FUNCTIONS"""
"""it is useless to put all of those in util py file those are created only to keep the code readable"""

"""All raw values should be converted to a type compatible with tf.Example."""


def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _float_feature(value):
    """Returns a float_list from a float / double."""
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))


def _int64_feature_old_(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _list_feature(value):
    """Returns a list useful for classification"""
    class_list = [0] * 101

    age = int(value)

    if (value - float(age)) > 0.5:
        age = age + 1
    if age > 100 :
        age = 100

    class_list[age] = 1
    arr = np.array(class_list)

    return _bytes_feature(arr.tobytes())


def _int64_feature(value):
    """Returns an int in one shot format."""
    class_list=np.array([0]*101, dtype=np.int64)
    age = int(value)
    if (value - float(age)) > 0.5 :
        age = age +1
    class_list[age] = 1
    return tf.train.Feature(int64_list=tf.train.Int64List(value=class_list))


def _int64_feature_order(value):
    """Returns a list in an ordered format."""
    class_list=np.array([0]*101, dtype=np.int64)

    age = int(value)
    if (value - float(age)) > 0.5 :
        age = age +1

    for i in range(0,age):
        class_list[i] = 1

    return tf.train.Feature(int64_list=tf.train.Int64List(value=class_list))


def _intify(num):
    """approximates an int to the nearest integer"""
    age = int(num)

    if (num - float(age)) > 0.5:
        age = age + 1
    if age > 100:
        age = 100

    return age


def tfRecordCreator(folder,to_store, name, size):
    """
    Summary line.

    it reads images, detects faces, resizes them, puts them in a tfrecord with label

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
        a tf record with extracted faces and labels (in a lot of different variants because multiple tests
        where done with different scripts)

    """

    num_img = 0
    print("from " + str(name))
    tfrecord_writer = tf.io.TFRecordWriter(folder + "/" + name + ".tfrecords")

    """begins read and write operation on a tfrecord for each image in the list"""
    for elem in to_store:
        num_img = num_img +1
        filename = elem[0]
        label = elem[1]
        img_path = root+"/"+filename
        face = util.detect(img_path, (size,size))
        if face is None:
            num_img = num_img -1
            continue
        image_string = face.tobytes()

        """example is wrote with image in bytes and label in multiple versione (instead of making multiple
           tfrecords version it has been chosen to put everything needed in one)"""
        example = tf.train.Example(features=tf.train.Features(feature={
              'label_regr': _float_feature(float(label)),
              'label_regr_int': _int64_feature_old_(_intify(float(label))),
              'label_class':_int64_feature(float(label)),
              'label_order': _int64_feature_order(float(label)),
              'image': _bytes_feature(image_string),

        }))

        tfrecord_writer.write(example.SerializeToString())
        if num_img % 1000 == 0 :
            print("for "+name+" tfrecord "+str(num_img)+" images have been written")

    tfrecord_writer.close()
    print(name +" tfrecord contains images " + str(num_img))


def csv_reader_with_check(root_path, csv_file_path):
    """it reads each [image,label] from a csv checking if image does exist from a given root and gives it in output"""
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)

        actual_images = []

        for row in reader:
            csv_old_path = row[0]
            age = row[1]

            new_path= root_path+"/"+csv_old_path
            image = pathlib.Path(new_path)

            if image.exists() and not row[1] in (None,""):

                actual_images.append([csv_old_path, age])

    return actual_images


tf.executing_eagerly()


"""BEGINNING OF THE SCRIPT"""
"""it collects each csv found in the folder"""
p = pathlib.Path(csv_root)
found_csvs = [x for x in p.iterdir() if x.is_file()]

"""every csv root is elaborated in a list of couple [csv_root,bare_name] as support"""
csvs_to_record = []
for cs in found_csvs:
    name = str(cs).split("\\").pop()
    stuff = [csv_root+"/"+name ,name.split(".")[0]]
    csvs_to_record.append(stuff)

"""for each csv images are read, shuffled and sent to tf print function"""
for cs in csvs_to_record:
    to_store_list = csv_reader_with_check(root,cs[0])
    print(str(len(to_store_list)) + " images read from " + cs[1] + ".csv and ready to be recorded.")
    random.shuffle(to_store_list)
    tfRecordCreator(output,to_store_list, cs[1],size)


print("END.")