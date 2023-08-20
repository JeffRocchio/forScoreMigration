This python directory contains python scripts which can be used as alternatives to using Spreadsheets to create the *0500_ExifTool-Input.csv* file and the *0510_Setlist-Import.mss* file.

### TBD - Python Script to Create Metadata Import File
The *fsCSVtransform.py* script will generate the *0500_ExifTool-Input.csv* file using the *Export.csv* in the */scores* directory. Status as of 08/19/2023:
   - Logic of the script completed and tested against the sample data set.
   - Next step is to have the script write the output to a .csv file.


### 8/17/2023: Initial Python Script to Create Setlists Import File
The *setlists.py* script will generate the *0510_Setlist-Import.mss* file using all the **.4ss* files in the */setlists* directory that you exported from forScore. This script must be run from the */setlists* directory.

**STATUS:** I have written this script and it works on my small set of test data.

**Notes:**
   - There are no command line options, so you do have to execute it, from a command line ('command prompt' in Windows) from within the directory where you put the exported forScore .4ss files.
   - The script will read in all those files and produce a consolidated MobileSheets .mss file named *0510_Setlist-Import.mss* which you can "Import" into MobileSheets.
   - Upon import MobileSheets will place the designated scores into each setlist you exported from forScore.
   - If the setlist doesn't yet exist in MobileSheets it will be created automatically. Scores named in the 0510_Setlist-Import.mss file but not found in MobileSheets will be skipped.

