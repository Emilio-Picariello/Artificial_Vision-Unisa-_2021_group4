import random
import _util_prepare_ as util

"""given a csv it splits it two, one to be kept as it is and another to be augmented"""

"""FUNDAMENTAL ARGS"""
"""where to find original csv"""
csv_path = 'train.age_detected.csv'
"""where to print csvs"""
output_path = "./__script_files/__1aug_csv/"
"""augment percentage"""
percent_aug = 15


"""BEGINNING OF THE SCRIPT"""
rows = util.read_csv(csv_path)

"""it divides all rows read in two lists according to percentage chosen"""
lenAug = int((len(rows)/100)*percent_aug)
random.shuffle(rows)
toAug = rows[:lenAug]
toKeep = rows[lenAug:]

util.write_csv(output_path+"toAug.csv",toAug)
util.write_csv(output_path+"toKeep.csv",toKeep)







