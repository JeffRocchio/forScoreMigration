H1 forScore to MobileSheets Migration
H2 Step-by-Step Instructions

This document contains the sequence of actions I took to migration from forScore to MobileSheets. If you are making the switch perhaps my experience can help you make the transition relatively smoothly.

What I did was document how I did it. I have not performed extensive testing on this process, so there may be errors. **Be sure to make backups!**

Also, I am a Linux guy with no access to a Windows or Mac PC. I believe that everything I've done will work on either Windows or a Mac. If someone tries it it would be good to advise any issues.

H3 Things to Know Before Getting Started
    1. This process will transfer all your scores out of forScore and into MobileSheets, including each score’s properties, or ‘metadata,’ that have set for all your scores.
    2. Annotations will *not* get transferred over as in both apps that information is unique and there is currently no way to capture it out of forScore and translate it into MobileSheets.
    3. forScore ‘Bookmarks’ will not get transferred over. The equivalent feature in MobileSheets is called ‘Snippets.’ Since I only had a half-dozen bookmarks set across my 1,000+ scores in forScore it was easier for me to just recreate them manually once my transfer was complete.
        1. Note that in addition to Snippets MobileSheets has a “bookmarks” feature. In MobileSheets this feature functions like bookmarks do in a regular PDF document – it is a link to a single page within the document. So you can create a ‘bookmark’ to jump to that spot in a PDF. Depending on how you used bookmarks in forScore this feature may be useful to you, and there is a provision in MobileSheets for importing bookmarks by using a CSV file. You can consult the MobileSheets user manual if interested in using that.
    4. forScore setlists can be transferred over in this process, and you can select which ones to transfer or not.
        1. Note: For successful setlist transfer you cannot rename scores, or their titles, after export from forScore. If you feel the need to clean up score titles you need to do that in forScore prior to beginning the migration process. If you do not plan on transferring any setlists over you could review and clean up score titles using the forScore exported metadata CSV document.
    5. This process depends upon two applications:
        1. A spreadsheet. MS-Excel or Libre Office Calc. I am a Linux guy and do not have access to a Windows or Mac computer. I used Libre Office Calc, which is freely available on all platforms. I don’t see any reason that the MS-Excel version of the spreadsheet I saved out of Libre Office won’t work, and I’d be interested in a confirmation of that if anyone uses this process with Excel.
        2. A free utility called ExifTool. This utility will be used to process the metadata. ExifTool is freely available for use on Windows, Mac, and Linux.
H3 Outline of the Process Steps
    1. *Spreadsheet Application*. Be sure you have a spreadsheet application that is MS-Excel compatible.
        1. Meaning that MS-Excel formulas will work in it. I used the Open Source application Libre Office Calc. MS-Excel should work. Google Sheets might work as well.
    2. *Acquire Exiftool*. Obtain and install ExifTool.
        1. Obtain @ https://exiftool.org/
    3. *forScore Export*.
        1. Scores. Export scores out of forScore and get them onto your desktop or laptop PC.
        2. Metadata. Export the metadata out of forScore and get the exported CSV file onto your laptop or desktop PC.
        3. Setlists. Export any setlists you wish to recreate in MobileSheets out of forScore and get those exported files onto your laptop or desktop PC.
    4. *Metadata Transformation*.
        1. Copy Metadata to Spreadsheet. Copy the forScore exported metadata CSV rows/columns into the spreadsheet I created for this purpose.
        2. Remove Bookmarks. Remove rows that represent forScore ‘Bookmark’ entries.
        3. Apply Transform Formulas. Copy formulas in spreadsheet to match the number of forScore exported scores.
    5. *Populate Scores with Metadata*.
        1. Produce ExifTool CSV. Export ExifTool/MobileSheets compatable CSV file from Spreadsheet.
        2. Set metadata into all scores by invoking ExifTool with the Spreadsheet produced CSV file.
    6. *Score Import*. Import all scores into MobileSheets.
    7. OPTIONAL – Transfer forScore Setlists
        1. *Setlist Transform*. import forScore exported setlist files into the Setlists Spreadsheet.
        2. *Create MobileSheets Import File*. Export .mss file from setlist Spreadsheet.
        3. *Import Setlists into MobileSheets*. Import .mss file into MobileSheets.

H3 Step-by-Step Guide
For a detailed description of the steps I took to make the migration, see the document *0010_Step-by-Step-Instructions.pdf*.
