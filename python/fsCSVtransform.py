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
# 08/19/2023 Jeff Rocchio:
#   - Logic of the script completed and tested against the sample data set.
#   - Next step is to have the script write the output to a .csv file.
#


import glob
import csv
import re

# **** FUNCTION DEFINITIONS ***********************************************************************

def message_Complete(stats_Rows, stats_Bookmarks):
    print(f'\n************* METADATA TRANSFORM COMPLETED *************')
    print('* ')
    print(f'* STATISTICS --')
    print(f'*\t{stats_Rows-1} Rows Processed')
    print(f'*\t{stats_Bookmarks} Bookmarked Virtual Scores Skipped')
    print(f'*\t{stats_Rows - stats_Bookmarks} Unique Score Rows in New CSV File')
    print('* ')
    print(f'* {csvOutFile} <-- Output has been written to this file.')
    print(f'*\tUse the above file as the input to ExifTool to ')
    print(f'*\tpopulate your metadata into your score docs ')
    print(f'*\tprior to import into MobileSheets.')
    print('* ')
    print(f'********************************************************\n')



def display_forScoreFieldNames(reader):
    print(f'Column Names are: {", ".join(reader.fieldnames)}')



def display_forScoreRow(row, kRowNum):
    print(f'Row Number: {kLineNum}----------------------------------------------------------')
    kColNum = 0
    for col in row:
        print(f'{reader.fieldnames[kColNum]}: >{row[col]}<')
        kColNum += 1
    print("\n")



def display_passbackList(passbackList):
    print(f'--- passbackList: {passbackList} -----------\n')



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
def transform_Row(row, forScoreColName, forScoreKeyLookup):
    passbackList = [ ]
    passbackList.append(row[forScoreColName[0]])  # Filename -> Filename
    passbackList.append(row[forScoreColName[1]])  # Title -> Title
    passbackList.append(row[forScoreColName[4]])  # Composer (often renamed to Arranger) -> Composer
    passbackList.append(row[forScoreColName[5]])  # Genres -> Genre
    passbackList.append(row[forScoreColName[6]])  # Tags -> Keywords
    passbackList.append(row[forScoreColName[7]])  # Books -> Albums
    passbackList.append(row[forScoreColName[8]])  # Reference -> SourceType
    passbackList.append(row[forScoreColName[9]])  # Rating -> Rating
    passbackList.append(row[forScoreColName[10]]) # Difficulty -> Difficulty
                                                  # Minutes+Seconds -> Duration
    if row[forScoreColName[11]].isnumeric and row[forScoreColName[12]].isnumeric:
        minutes = row[forScoreColName[11]]
        seconds = row[forScoreColName[12]]
        duration = (int(minutes.strip() or 0)*60) + int(seconds.strip() or 0)
        passbackList.append(duration)
    else:
        passbackList.append("")

                                                  # keysf+keymi (OR "Key:aaa in Tags) -> Key
    if row[forScoreColName[13]]:                                   # Value present in keysf column. Trumps Tags field.
        keyTblRowIx = int(row[forScoreColName[13]].strip() or 0) + 10
        keyTblColIx = int(row[forScoreColName[14]].strip() or 0)
        print(f"Rows In Table: {len(forScoreKeyLookup)}   || keyTblRowIx: {keyTblRowIx}  || keyTblColIx: {keyTblColIx}")
        passbackList.append(forScoreKeyLookup[keyTblRowIx][keyTblColIx])
    elif re.search(pat_Key, row[forScoreColName[6]]):              # Regex search in Tags field for 'Key:aaa'
        match = re.search(pat_Key, row[forScoreColName[6]])
        passbackList.append(match.group(1))
    else:
        passbackList.append("")

    display_passbackList(passbackList)
    return passbackList


# **** INITIALIZATIONS ****************************************************************************

        # forScore exported CSV filename.
forScoreCSV = r'Export.csv'

        # Base file name we will write the ExifTool CSV to.
#csvOutFile = '0500_ExifTool-Input.csv'
csvOutFile = '00_csvOut.csv'

        # Regex patterns we need to match text in forScore csv export file.
pat_Key = r'[kK]ey:(.+?)[, $]?'

        # forScore Key Signature lookup table.
        # Documentation: See the tab "forScore Key Values" in /Documentation/0110_FieldMappingAndSuch.ods
forScoreKeyLookup = ["INVALID", "INVALID"], ["INVALID", "INVALID"], ["INVALID", "INVALID"], \
    ["Cb", "INVALID"], ["Gb", "Ebm"], ["Db", "Bbm"], ["Ab", "Fm"], ["Eb", "Cm"], ["Bb", "Gm"], \
    ["F", "Dm"], ["C", "Am"], ["G", "Em"], ["D", "Bm"], ["A", "F#m"], ["E", "C#m"], ["B", "G#m"], \
    ["F#", "D#m"], ["C#", "INVALID"]


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



# **** TRANSFORM THE METADATA *********************************************************************

        # Do the work. Read forScore Export file, do transforms, and produce ExifTool input file.
with open(forScoreCSV, newline='') as csvFileIn:
    reader = csv.DictReader(csvFileIn, delimiter=',')
    forScoreColName = reader.fieldnames
    kLineNum = 0
    for row in reader:
        if kLineNum == 0:
            display_forScoreFieldNames(reader)
        else:
            if row['Start Page (Bookmark)'] == "":
                display_forScoreRow(row, kLineNum)
                transform_Row(row, forScoreColName, forScoreKeyLookup)
            else:
                stats_Bookmarks += 1
                print("*** SKIPPING ROW DUE TO VIRTUAL SCORE ***")
                display_forScoreRow(row, kLineNum)
        kLineNum += 1

stats_Rows = kLineNum
message_Complete(stats_Rows, stats_Bookmarks)


