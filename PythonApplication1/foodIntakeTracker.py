"""
	This script will run analysis on the food monitoring spreadsheet.

	Author: Donald Mannise
	Date: 3/2/2020
"""

import csv
import math
import sys
import os
import shutil
import ntpath
import xlrd
import pandas as pd


def main():
    # argument check
    if len(sys.argv) < 2:
        print("Too few arguments!\nPlease pass in the file to analyzed.")
        sys.exit()

    file = convert_to_csv()
    total_calories(file)


"""
    The purpose of this function is to create a copy of the passed in file if it is not a .csv, and make the new
    copy a csv. The original will have 'OLD' appended to the file name (this can be altered, see below). The path
    and file name of either the new csv file or the orignal if it was already a csv will be returned.

    return: path and file name to file to be analyzed
"""
def convert_to_csv():
    file_path_and_name = sys.argv[1]
    file_path_and_name_no_ext, file_ext = os.path.splitext(sys.argv[1])

    # if passed in file was not a csv
    if str(sys.argv[1])[-3:] != "csv":
        print("Converting file to csv..")
        file_path = sys.argv[1][:-len(ntpath.basename(sys.argv[1]))]
        file_name_with_ext = ntpath.basename(sys.argv[1])
        
        # replace original_file_rename with alternative string if desired
        original_file_rename = file_path_and_name_no_ext + "OLD" + file_ext
        new_file_type = ".csv"
        

        # The following code copies over the original file's content to a newly created csv
        old_path_new_name = r'%s' % file_path_and_name_no_ext+new_file_type
        try:
            wb = xlrd.open_workbook(file_path_and_name, 'w')
        except:
            print("The file %s could not be found" % file_path_and_name)
            sys.exit()
        sh = wb.sheet_by_name('Sheet1')
        new_csv = open(old_path_new_name, 'w')
        wr = csv.writer(new_csv, quoting=csv.QUOTE_ALL)

        for rownum in range(sh.nrows):
            wr.writerow(sh.row_values(rownum))
        new_csv.close()

        # adds "OLD" to original file for clarity
        os.rename(file_path_and_name, original_file_rename)

        # return the path and name of the newly created csv file
        return old_path_new_name

    # if passed in file was a csv
    else:
        # replace original_file_rename with alternative string if desired
        original_file_rename = file_path_and_name_no_ext + "OLD" + file_ext

        try:
            # makes the copy of the file with the new name 'original_file_rename'
            shutil.copy2(file_path_and_name, original_file_rename)
        except:
            print("The file %s could not be found" % file_path_and_name)
            sys.exit()

        # File was already a csv, return the passed in file path+name
        return sys.argv[1]


def total_calories(file):
    df = pd.read_csv(file, skip_blank_lines=True, sep=",", error_bad_lines=False)
    # Drop rows where every cell is empty
    df.dropna(axis=0, how='all', thresh=None, subset=None, inplace=True)

    done = False
    day_index = 0
    print(df)
    while done == False:
        end_of_day = False
        total_cals = 0
        current_date = df['Date'][day_index]
        while end_of_day == False:
            total_cals += df['Cal'][day_index]
            day_index = day_index + 1
            try:
                if df['Date'][day_index] != current_date:
                    end_of_day = True
                    if df.iat[day_index-1,9] != total_cals: # checking if write is necessary
                        df.iat[day_index-1,9] = total_cals
            except:
                end_of_day = True
                if df.iat[day_index-1,9] != total_cals: # checking if write is necessary
                    df.iat[day_index-1,9] = total_cals
                done = True
    
    print(df)
    df.to_csv(file)


main()