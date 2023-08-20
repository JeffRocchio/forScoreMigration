import glob
import re

# Declare pattern that finds all the forScore exported 'editable' setlist files.
forScoreSetlistFiles = r'*.4ss'

# Declare the file name we will write the MobileSheets XML .mss data into.
xmlOutFile = '0510_Setlist-Import.mss'

# Make a list of all forScore setlist files found the directory this script is executed from
files = glob.glob(forScoreSetlistFiles)

# Regex patterns we need to match in the forScore setlist export files.
pat_SetlistStart = r'<forScore kind=".+\stitle="(.+?)">'
pat_SetlistEnd = r'</forScore>.*'
pat_SongLine = r'<score title="(.+?)"\spath="(.+?)"\s*?/>'

# A list variable where we will build the MobileSheets XML data structures.
xmlOutLines = [ ]
xmlOutLines.append('<?xml version="1.0" encoding="UTF-8" ?>\n')
xmlOutLines.append('<Setlists>\n')

for file in files:
    with open(file, mode="r") as forScoreSLFile:
        k = 0
        for line in forScoreSLFile:
            line = line.strip()
            print('LINE ' + str(k) + ':' + line)

            match = re.search(pat_SetlistStart, line)
            if match:
                xmlOutLines.append('    <Setlist><Name>' + match.group(1) + '</Name>')

            match = re.search(pat_SetlistEnd, line)
            if match:
                xmlOutLines.append('    </Setlist>\n')

            match = re.search(pat_SongLine, line)
            if match:
                xmlOutLines.append('        <Song><Title>' + match.group(1) + '</Title><FileName>' + match.group(2) + '</FileName><FileType>1</FileType></Song>')

            k = k + 1

xmlOutLines.append('</Setlists>')

print("\n**** OUTPUT XML ****\n")
for item in xmlOutLines:
    print(item)

print("\n********************\n")
print("Writing the XML Output File: " + xmlOutFile + "\n")

with open(xmlOutFile, mode='w') as outFile:
    for item in xmlOutLines:
        outFile.write(item + '\n')


