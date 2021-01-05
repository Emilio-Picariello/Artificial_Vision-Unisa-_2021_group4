import _util_prepare_ as util
import random

"""given a csv it opens all its images (if possible), augments all of them and updates all paths writing a new csv"""

"""FUNDAMENTAL ARGS"""
"""where to find original csv"""
csv_path='./__script_files/__1aug_csv/toAug.csv'
"""where to find dataset"""
root = "./../../complete_train"
"""where to find print updated csv"""
output_path = "./__script_files/__3augmented/"


"""BEGINNING OF THE SCRIPT"""
rows = util.read_csv(csv_path)

"""it shuffles read rows to use a random corruption for all of them"""
random.shuffle(rows)
augmented = util.augment(rows,root)

util.write_csv(output_path+"augmented.csv",augmented)








