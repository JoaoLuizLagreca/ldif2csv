SEPARATOR = ';'
JOINER = '|'
QUOTECHAR = '"'
DATA_LIMIT=524288

import sys
import os
import argparse
import csv


prs = argparse.ArgumentParser(prog='ldif2csv', formatter_class=argparse.RawTextHelpFormatter, description="""
Convert big LDIF files to CSV with the specified columns
The CSV format is thrown to STDOUT, columns are case-sensitive

Example usage:
python ldif2csv.py LDIF_FILE.ldif COLUMN1 COLUMN2 COLUMN3 > CSV_FILE.csv

Made for Python 2.7
""")
prs.add_argument('INPUT', help='LDIF input file')
prs.add_argument('COLUMN', help='Columns to parse to CSV file', nargs='+')
args = prs.parse_args()

if not os.path.exists(args.INPUT):
    sys.stderr.write("Input file doesn't exists")
    exit(129) # ENOENT
if os.path.isdir(args.INPUT):
    sys.stderr.write("The input specified is a directory")
    exit(123) # EISDIR

ldif = open(args.INPUT, mode='rb')
maxindex = float(os.path.getsize(args.INPUT))
values={}
data=[]

def printCompletion():
    completion = round(ldif.tell()/maxindex, 2)*100.
    sys.stderr.write(str(completion)+"% converted...\n")
def endAll(code):
    ldif.close()
    exit(code)

def writeValue(column, value):
    if column in args.COLUMN:
        if column in values:
            v=values[column]
            values[column]=(v+JOINER+value)
        else:
            values[column]=value

def writeData():
    data.insert(0, values.copy())
    values.clear()
    if len(data)>=DATA_LIMIT:
        writeCSV()

def writeCSV():
    try:
        while len(data)>0:
            writer.writerow(data.pop())
    except IOError:
        raise
        endAll(132) # ENOMEM
    except:
        raise
        endAll(-1)
    finally:
        printCompletion()



writer = csv.DictWriter(sys.stdout, args.COLUMN, delimiter=SEPARATOR, quotechar=QUOTECHAR, quoting=csv.QUOTE_ALL, lineterminator = '\n')
writer.writeheader()
printCompletion()

line=""
while True:
    try:
        line=ldif.next()
    except StopIteration:
        break

    lineData=line.split(": ", 1)
    if len(lineData)<2:
        writeData()
        continue

    lineData[1]=lineData[1].replace('\n', '')
    writeValue(lineData[0], lineData[1])

writeCSV()

sys.stderr.write("Conversion completed!\n")
endAll(0)