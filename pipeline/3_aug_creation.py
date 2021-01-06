import _util_prepare_ as util
import random
import os
import shutil

"""given a csv it opens all its images (if possible), augments all of them and updates all paths writing a new csv"""

"""FUNDAMENTAL ARGS"""
"""
[WARNING]
root is where to find dataset
if it's the first time you run this code,
write your relative dataset path here
"""
#root = "./../../complete_train"
root="./ultra_lite_train"
"""where to find original csv"""
csv_path='./temp_csvs/toAug.csv'
"""where to find print updated csv"""
output_path = "./augmented_csv/"


"""BEGINNING OF THE SCRIPT"""
if not os.path.isdir(root):
    print("modify root constant in the code with your relative path to dataset root")
    exit(404)

if os.path.isdir(root+"/augment"):
    print("removing old augment images...")
    shutil.rmtree(root+"/augment")
os.mkdir(root+"/augment")

if os.path.isdir(output_path):
    shutil.rmtree(output_path)

os.mkdir(output_path)

rows = util.read_csv(csv_path)

"""it shuffles read rows to use a random corruption for all of them"""
random.shuffle(rows)


augmented = util.augment(rows, root)


util.write_csv(output_path+"augmented.csv",augmented)








