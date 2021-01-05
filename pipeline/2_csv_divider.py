import _util_prepare_ as util

"""given a csv it splits it in equal n parts"""

"""FUNDAMENTAL ARGS"""
"""where to find original csv"""
csv_path='./__script_files/__1aug_csv/toKeep.csv'
"""where to print csvs"""
output_path = "./__script_files/__2divided_csv/"
"""number of parts to split original one in"""
number_csvs = 150


"""BEGINNING OF THE SCRIPT"""
rows = util.read_csv(csv_path)

"""it divides all rows read in n lists according to number_csvs chosen"""
numCsv = int(len(rows)/number_csvs)
csvs = [rows[i:i + numCsv] for i in range(0, len(rows), numCsv)]
csvs = csvs[:(len(csvs)-1)]

"""it prints each csv"""
i = 0
for csv in csvs:
    i= i+1
    util.write_csv(output_path + "dataset_part"+str(i)+".csv", csv)
    print("dataset_part"+str(i)+".csv finished")