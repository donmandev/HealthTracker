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
from openpyxl import load_workbook


def main():
    # argument check
    if len(sys.argv) < 2:
        print("Too few arguments!\nPlease pass in the file to analyzed.")
        sys.exit()

    file = archive_original()
    total_calories(file)


"""
    The purpose of this function is to create a copy of the passed in file and append 'OLD' to the 
    copy. This allows for archiving the original file should the user want it back.

    return: path and file name to file to be analyzed
"""
def archive_original():
    file_path_and_name = sys.argv[1]
    file_path_and_name_no_ext, file_ext = os.path.splitext(sys.argv[1])

    # replace original_file_rename with alternative string if desired
    original_file_rename = file_path_and_name_no_ext + "OLD" + file_ext

    # Makes a copy of the original file with 'OLD' appended to the end
    shutil.copy2(file_path_and_name, original_file_rename)

    return file_path_and_name

"""
    The purpose of this function is to fill in the 'Total Day Cals' column. A total calorie amount will
    be added to the row where the last entry for that day was found.
"""
def total_calories(file):
    df = pd.read_excel(file, skip_blank_lines=True, sep=",", error_bad_lines=False)
    print(df.iat[1,0])

    print(df)

    # Check if totals have already been calculated
    if df['Total Day Cals'].iloc[-1] > 0:
        print( "All Calorie totals up to date.")
        return

    # Drop rows where every cell is empty
    df.dropna(axis=0, how='all', thresh=None, subset=None, inplace=True)

    done = False
    day_index = 0
    
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
                else:
                    df.iat[day_index-1,9] = None
            except:
                end_of_day = True
                if df.iat[day_index-1,9] != total_cals: # checking if write is necessary
                    df.iat[day_index-1,9] = total_cals
                else:
                    df.iat[day_index-1,9] = None
                done = True
    
    print(df)
    print(df.iat[1,0])
    df.to_excel(file, index=False)


main()