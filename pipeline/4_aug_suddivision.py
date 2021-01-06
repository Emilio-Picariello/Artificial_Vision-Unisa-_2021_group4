import random
import _util_prepare_ as util
import pathlib

"""given an augmented csv it splits its rows in n parts and append each one to all n original csvs """
"""(supposing original images are not there)"""


"""FUNDAMENTAL ARGS"""
"""where to find augment csv"""
csv_path='./augmented_csv/augmented.csv'
"""where to find original csvs"""
root_original_csvs = "./divided_csv/"


"""BEGINNING OF THE SCRIPT"""
rows = util.read_csv(csv_path)
random.shuffle(rows)

"""it takes all original csvs read as lists"""
p = pathlib.Path(root_original_csvs)
csvs_to_modify = [x for x in p.iterdir() if x.is_file()]

"""if no csv is there tells user to put them in the arg root directory"""
num = len(csvs_to_modify)
if num == 0:
    print("paste your csvs to modify in "+ root_original_csvs +" and reload this script.")
    exit(300)

"""it splits in equal n parts augment csv according to n original csvs except for the last one"""
num_to_add_per_csv = int(len(rows)/num)
to_write = [rows[i:i + num_to_add_per_csv] for i in range(0, len(rows), num_to_add_per_csv)]
to_write = to_write[:num]

"""it appends one augment part to each original csv"""
for i in range(0,len(to_write)):
    util.append_csv(root_original_csvs+str(csvs_to_modify[i]).split("\\").pop(),to_write[i])
print("all "+ str(len(to_write)) + " file(s) have been written")





