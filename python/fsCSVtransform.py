# =================================================================================================
# PROJECT: forScore Migration to MobileSheets
# COMPONENT: fsCSVtransform.py
#
# This script transforms forScore metadata into MobileSheets compatable metadata. The script
# consumes a .csv file of metadata exported from forScore and produces a .csv file of metadata
# suitable as input for the ExifTool utility to set the MobileSheets metadata into all of the
# scores exported out of forScore. Once that has been done those scores can be imported into
# MobileSheets and the metadata will automatically detected and set by MobileSheets.
#
# My key learning reference for reading and writing to CSV files in Python is a page
# at 'Real Python' : Reading and Writing CSV Files in Python @ https://realpython.com/python-csv/
#
# 08/19/2023 Jeff Rocchio:
#   - Logic of the script completed and tested against the sample data set.
#   - Next step is to have the script write the output to a .csv file.
#

VERSION = "1.0 08-21-2023"

import sys
import os
import csv
import re
import argparse # For defining and handling command line arguments.

# =================================================================================================
#    FUNCTION DEFINITIONS
# =================================================================================================

    # ---------------------------------------------------------------------------------------------
    # This function configures the command line to accept certain arguments.
    # Reference: https://machinelearningmastery.com/command-line-arguments-for-your-python-script/
    # Note the following:
    #    - Hyphens in a command line param names get converted to an underscore for variable
    #      name reference purposes.
    #    - To access a param defined with type=argparse.FileType('r') you need to go an add'l
    #      level deeper into the object. E.g., args.file_path.name.
    # RETURNS args object, which contains all the arguments from the command line.
def commandline():
    parser = argparse.ArgumentParser(description="forScore to MobilSheets Metadata .CSV file Conversion Tool", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--verbose", action="store_true", help="Show conversion activity on terminal screen.")
    parser.add_argument("-i", "--input-file-path", default="Export.csv", help="forScore CSV file name, may be full path to file. Default is Export.csv.")
    parser.add_argument("-o", "--output-file-path", default="0500_ExifTool-Input.csv", help="Output file name, may be full path to file. Default is Exiftool-Import.csv.")
    args = parser.parse_args()
    if args.verbose:
        print(f'\nCommand Line Arguments: {args}')
    return args


    # ---------------------------------------------------------------------------------------------
    # This function validates that we can find our way to the csv file to operate on.
    # We may be using the default path, or user may have specified one on the command line.
    # Also validate the path to the output file. This file likely does not yet exist, so
    # I am only checking for the existence of any path to the file, not the pre-existence
    # of the file itself. (Thus, if the path is invalid we are NOT going to create it.)
    # NOTE:
    #   - If user does not provide an argument for the output file, OR provides only the
    #     name of a file with no path spec, then we have an empty string for the path to the
    #     output file. In a test for valid path this returns False. So we test for this
    #     condition and if it is the case we pre-pend the current working directory.
    # NOTE:
    #   - Two things: the command line arguments list, in this case the variable 'args', is
    #     writable. Prior to trying this I probably would have thought it was not.
    #   - The variable 'args' passed into this function is evidently passed in by reference.
    #     Even tho I've written to it inside this function, the new value for args.output_file_path
    #     shows up to the caller. So that was unexpected, and I couldn't explain in which cases
    #     function params are passed by value vs by reference in Python.
    #
    # RETURNS 0 if both are valid, -1 if input file is invalid, -2 if output path is invalid.
    #
def files_Invalid(args):
    result = 0
    if not os.path.isfile(args.input_file_path):
        result = -1
    if len(os.path.dirname(args.output_file_path)) == 0:
        args.output_file_path = os.path.join(os.getcwd(), os.path.basename(args.output_file_path))
    if not os.path.dirname(args.output_file_path):
        result = -2
    return result


    # ---------------------------------------------------------------------------------------------
    # This function displays results of the processing. To be called when all processing has
    # completed.
def message_Complete(stats_Rows, stats_Bookmarks):
    print(f'\n************* METADATA TRANSFORM COMPLETED *************')
    print(f'* ')
    print(f'* fsCSVtransform Version {VERSION} ')
    print(f'* ')
    print(f'* STATISTICS --')
    print(f'*\t{stats_Rows-1} Rows Processed')
    print(f'*\t{stats_Bookmarks} Bookmarked Virtual Scores Skipped')
    print(f'*\t{stats_Rows - stats_Bookmarks} Unique Score Rows in New CSV File')
    print(f'* ')
    print(f'* {csvOutFile} <-- Output has been written to this file.')
    print(f'*\tUse the above file as the input to ExifTool to ')
    print(f'*\tpopulate your metadata into your score docs ')
    print(f'*\tprior to import into MobileSheets.')
    print(f'* ')
    print(f'********************************************************\n')



def display_csvColumnNames(args, reader, msFieldNames):
    if args.verbose:
        print(f'\nforScore Column Names Are: {", ".join(reader.fieldnames)}')
        print(f'Output CSV File Column Name Are: {", ".join(msFieldNames)}\n')



def display_forScoreRow(args, row, kRowNum, bookMark=False):
    if args.verbose:
        if bookMark:
            print("*** SKIPPING ROW DUE TO VIRTUAL SCORE ***")
        print(f'Row Number: {kLineNum}----------------------------------------------------------')
        kColNum = 0
        for col in row:
            print(f'{reader.fieldnames[kColNum]}: >{row[col]}<')
            kColNum += 1
        print("\n")



def display_passbackDict(args, passbackDict):
    if args.verbose:
        print(f'--- passbackDict: {passbackDict} -----------\n')



    # ---------------------------------------------------------------------------------------------
    # This function creates a list of the column names found in the forScore metadata export
    # file. I am doing this for two reasons. One, metadata names may be renamed in forScore, and
    # it is the potentially renamed field names that get exported in the csv file.
    # Two: Unlike a list, you cannot use numberic index references for the row/columns of a
    # file bring read in line by line; you have to reference the column data by using the
    # column name in row 1 of the csv file. Thus I have to dereference those by this
    # mechanism.
def build_ColNameList(reader):
    nameList = [ ]
    kColNum = 0
    for colName in reader.fieldnames:
        nameList[colName]
        print(nameList[kColNum])
        kColNum += 1
    return nameList



    # ---------------------------------------------------------------------------------------------
    # This function does the work of translating from forScore's metadata tag names
    # values over to what MobileSheets needs to take in to populate the matching
    # metadata fields. For reference see the worksheet: 0110_FieldMappingAndSuch.ods
    #
    # RETURNS: A dictionary object that contains the output row we will write to the output file.
def transform_Row(row, forScoreColName, forScoreKeyLookup, msFieldNames):

    # ********
    # passbackDict needs to be updated to include the column headings with the data.
    # Try to make it so that we use the msFieldNames list to be sure we are in
    # lock-step.
    # ********

    passbackDict = {}
    passbackDict[msFieldNames[0]] = row[forScoreColName[0]]  # Filename -> Filename
    passbackDict[msFieldNames[1]] = row[forScoreColName[1]]  # Title -> Title
    passbackDict[msFieldNames[2]] = row[forScoreColName[4]]  # Composer (often renamed to Arranger) -> Composer
    passbackDict[msFieldNames[3]] = row[forScoreColName[5]]  # Genres -> Genre
    passbackDict[msFieldNames[4]] = row[forScoreColName[6]]  # Tags -> Keywords
    passbackDict[msFieldNames[5]] = row[forScoreColName[7]]  # Books -> Albums
    passbackDict[msFieldNames[6]] = row[forScoreColName[8]]  # Reference -> SourceType
    passbackDict[msFieldNames[7]] = row[forScoreColName[9]]  # Rating -> Rating
    passbackDict[msFieldNames[8]] = row[forScoreColName[10]] # Difficulty -> Difficulty
                                                  # Minutes+Seconds -> Duration
    if row[forScoreColName[11]].isnumeric and row[forScoreColName[12]].isnumeric:
        minutes = row[forScoreColName[11]]
        seconds = row[forScoreColName[12]]
        duration = (int(minutes.strip() or 0)*60) + int(seconds.strip() or 0)
        passbackDict[msFieldNames[9]] = duration
    else:
        passbackDict[msFieldNames[9]] = ""

                                                  # keysf+keymi (OR "Key:aaa in Tags) -> Key
    if row[forScoreColName[13]]:                  # Value present in keysf column trumps Tags field.
        keyTblRowIx = int(row[forScoreColName[13]].strip() or 0) + 10
        keyTblColIx = int(row[forScoreColName[14]].strip() or 0)
        #print(f"Rows In Table: {len(forScoreKeyLookup)}   || keyTblRowIx: {keyTblRowIx}  || keyTblColIx: {keyTblColIx}")
        passbackDict[msFieldNames[10]] = forScoreKeyLookup[keyTblRowIx][keyTblColIx]
    elif re.search(pat_Key, row[forScoreColName[6]]):    # Regex search in Tags field for 'Key:aaa'
        match = re.search(pat_Key, row[forScoreColName[6]])
        passbackDict[msFieldNames[10]] = match.group(1)
    else:
        passbackDict[msFieldNames[10]] = ""

    display_passbackDict(args, passbackDict)
    return passbackDict




# **** SET NEEDED STATIC ITEMS ********************************************************************

msFieldNames = ['SourceFile', 'Title', 'Author', 'Subject', 'Keywords', 'Books', 'SourceType', 'Rating', 'Difficulty', 'Duration', 'Key']

        # Regex patterns we need to match text in forScore csv export file.
        # This one captures my "Key:aaa" text that I have been putting into the Keywords field.
pat_Key = r'[kK]ey:([\w#]{1,3})[, $]?'

        # forScore Key Signature lookup table.
        # Documentation: See the tab "forScore Key Values" in /Documentation/0110_FieldMappingAndSuch.ods
forScoreKeyLookup = ["INVALID", "INVALID"], ["INVALID", "INVALID"], ["INVALID", "INVALID"], \
    ["Cb", "INVALID"], ["Gb", "Ebm"], ["Db", "Bbm"], ["Ab", "Fm"], ["Eb", "Cm"], ["Bb", "Gm"], \
    ["F", "Dm"], ["C", "Am"], ["G", "Em"], ["D", "Bm"], ["A", "F#m"], ["E", "C#m"], ["B", "G#m"], \
    ["F#", "D#m"], ["C#", "INVALID"]


# **** DECLARE KEY VARIABLES IN TRADITIONAL C STYLE SO FOR DOCUMENTATION PURPOSES *****************

        # forScore exported CSV file-path-name. We get this from command line arguments.
forScoreCSV = ""

        # Output CSV file-path-name. Will get this from command line arguments
csvOutFile = ""

        # To deal with potential forScore metadata field having been renamed by users we
        # need to use the column headings in the forScore export file to access the fields
        # in each row we are processing (cannot access by an numberic index number for a
        # csv file read line-by-line). So this list is used to store forScore csv column
        # headings.
forScoreColName = [ ]

stats_Rows = 0
stats_Bookmarks = 0

        # A list variable where we will build the ExifTool CSV output.
csvOutLines = [ ]
csvOutLines.append('<?xml version="1.0" encoding="UTF-8" ?>\n')


# =================================================================================================
#    MAIN BODY OF THE PROGRAM
# =================================================================================================

# **** INITIAL VALIDATIONS ************************************************************************

        # Configure and retrieve command line arguments.
args = commandline()

        # Validate input and output file-paths.
error = files_Invalid(args)
if error == -1:
    print(f'\nERROR - Input file not found: {args.input_file_path}\n')
    sys.exit()
elif error == -2:
    print(f'\nERROR - Directory for Output file does not exist: {os.path.dirname(args.output_file_path)}\n')
    sys.exit()
else:
    forScoreCSV = args.input_file_path
    csvOutFile = args.output_file_path
    if args.verbose:
        print(f'\nInput File-Path: {args.input_file_path}')
        print(f'Output File-Path: {args.output_file_path}')



        # forScore exported CSV file-path-name. Will get from command line arguments.
forScoreCSV = args.input_file_path

        # Output CSV file-path-name. Will get from command line arguments
csvOutFile = args.output_file_path


# **** TRANSFORM THE METADATA *********************************************************************

        # Do the work. Read forScore Export file, do transforms, and produce ExifTool input file.
with open(forScoreCSV, newline='') as csvFileIn:
    reader = csv.DictReader(csvFileIn, delimiter=',')
    forScoreColName = reader.fieldnames
    display_csvColumnNames(args, reader, msFieldNames)
    kLineNum = 0
    # Open the output file for writing.
    outFile = open(csvOutFile, mode='w')
    writer = csv.DictWriter(outFile, fieldnames=msFieldNames)
    writer.writeheader()
    for row in reader:
        if row['Start Page (Bookmark)'] == "":
            display_forScoreRow(args, row, kLineNum)
            passbackDict = transform_Row(row, forScoreColName, forScoreKeyLookup, msFieldNames)
            writer.writerow(passbackDict)
        else:
            stats_Bookmarks += 1
            display_forScoreRow(args, row, kLineNum, bookMark=True)
        kLineNum += 1

        # Successful completion - clean up, provide some statistics and lightweight
        # instructions then exit.
outFile.close
stats_Rows = kLineNum
message_Complete(stats_Rows, stats_Bookmarks)


