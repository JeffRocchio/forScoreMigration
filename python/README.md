# forScore Migration to MobileSheets

This python directory contains python scripts which can be used as alternatives to using Spreadsheets to create the *0500_ExifTool-Input.csv* file and the *0510_Setlist-Import.mss* file.

I would now recommend using these scripts instead of the Spreadsheets as I believe they will be both easier to use and more reliable.

## Two Scripts

### 8/21/2023 - Python Script to Create Metadata Import File
The *fsCSVtransform.py* script will generate the *0500_ExifTool-Input.csv* file using the *Export.csv* file of metadata exported from forScore.

**STATUS:** Completed and tested with my 1000+ scores from forScore.


### 8/17/2023: Initial Python Script to Create Setlists Import File
The *setlists.py* script will generate the *0510_Setlist-Import.mss* file using all the **.4ss* files in the */setlists* directory that you exported from forScore. This script must be run from the */setlists* directory.

**STATUS:** Completed and tested with about 15 Setlists containing about 600 scores.

**Notes:**
    - There are no command line options, so you do have to execute it, from a command line ('command prompt' in Windows) from within the directory where you put the exported forScore .4ss files.
    - The script will read in all those files and produce a consolidated MobileSheets .mss file named *0510_Setlist-Import.mss* which you can "Import" into MobileSheets.
    - Upon import MobileSheets will place the designated scores into each setlist you exported from forScore.
    - If the setlist doesn't yet exist in MobileSheets it will be created automatically. Scores named in the 0510_Setlist-Import.mss file but not found in MobileSheets will be skipped.

## Usage Instructions

**NOTE**: On 8/21/2023 I did an end-to-end full-scale run of the below instructions and all worked fine. Obviously we all have somewhat different circumstances so it is certainly possible that you may encounter some glitches. If so, I may be able to help. Post an Issue here on github if you have an account, or else post in the topic I created on the MobileSheets forum. And...**make backups before you do anything!**

1. On your desktop PC (or laptop) install two applications:
    1. **Python 3.11**. Get this from your app store (e.g., 'Microsoft Store,' or Apple App Store).
    2. **ExifTool**. Goto [https://exiftool.org/](https://exiftool.org/) and obtain and install the version for your system.

2. Somewhere in your home directory create the following subdirectory structure:

            forScoreMigration
                | scores
                | setlists

3. Export from forScore:
    > Refer to Section 3 in [0010_Step-by-Step-Instructions.pdf](https://github.com/JeffRocchio/forScoreMigration/blob/main/0010_Step-by-Step-Instructions.pdf).

    1. Copy all your scores off you iPad, from the forScore directory in the iPad's File Manager. Get those into the *forScoreMigration/scores* directory on your PC. The easiest way to do this is by using a cloud service. In my case, for example, I use Dropbox.
    2. Export your metadata out of forScore into the forScoreMigration/scores directory as filename Export.csv.
    3. Export your setlists, as "editable," out of forScore into the forScoreMigration/setlists directory.

4. Download three items from this github site:
    1. Download *python/fsCSVtransform.py* to your *forScoreMigration/scores* directory.
    1. Download the file *python/ExifTool_config* to your *forScoreMigration/scores* directory.
    1. Download *python/setlists.py* to your *forScoreMigration/setlists* directory.

5. Open a terminal (in Windows this is called the 'Command Prompt') and do the following:
    1. CD (change directory) into the *forScoreMigration/scores* directory.
    1. In the terminal window run the following:

                python3.11 fsCSVtransform.py

        This will run and "translate" the forScore exported metadata for each score into a form that MobileSheets can use. The result is a new file in your *forScoreMigration/scores* directory named *0500_ExifTool-Input.csv*.

    1. Now in the terminal window run this command:

                exiftool -config ExifTool_config -csv=0500_ExifTool-Input.csv -csvDelim ',' -overwrite_original *.pdf

        This will populate all your exported score documents with the transformed metadata to make them ready for import into forScore.

    1. To bring your forScore setlists into MobileSheets do the following:
        1. CD into *forScoreMigration/setlists* directory.
        1. In the terminal window run the following:

                python3.11 setlists.py

            This will read in all the forScore exported setlist files (those have the file extension .4ss) and produce an output file that MobileSheets can import to create the setlists and assign the scores to them. The created output file for MobileSheets will be named *0510_Setlist-Import.mss*.

6. Make sure you have a clean MobileSheets on your device. If necessary perform a full backup, then a full delete of your library.

7. Now you can import your scores and setlists:
    1. First, make sure the setting to automatically read metadata from PDF files on import is set to ON. In MobileSheets goto *Settings / Import Settings / Extract PDF Metadata* - make sure it is set to **ON**
    1. Create a directory on a cloud service that your MobileSheets app can see and import from. Copy all your scores to that directory.
    1. Next, import all your scores. Use MobileSheets' 'Batch' import option. Point it to the cloud directory where you copied all your scores. Let it import them. As MobileSheets imports each it will populate the metadata files from the PDF docs due to how we used ExifTool to set the metadata into the PDFs.
    1. Now you can import your setlists.
        1. Copy the *forScoreMigration/setlists/0510_Setlist-Import.mss* file over to your cloud directory.
        2. Go into your MobileSheets app and import it. MobileSheets will create the setlists.

**DONE**
