SEPARATOR = ';'
JOINER = '|'
QUOTECHAR = '"'

import sys
import os
import fileinput
import argparse
import csv
from io import StringIO


prs = argparse.ArgumentParser(prog='ldif2csv')
prs.add_argument('INPUT', help='LDIF input file')
prs.add_argument('COLUMN', help='Columns to parse to CSV file', nargs='+')
args = prs.parse_args()

if not os.path.exists(args.INPUT):
    sys.stderr.write("Input file doesn't exists")
    exit(129) # ENOENT
if os.path.isdir(args.INPUT):
    sys.stderr.write("The input specified is a directory")
    exit(123) # EISDIR

ldif = open(args.INPUT, mode='r')
values={}
data={}
def endAll(code):
    ldif.close()
    exit(code)

def writeValue(column, value):
    #if column in args.COLUMN:
    if column in values:
        v=values[column]
        values[column]=(v+"|"+value)
    else:
        values[column]=value
def writeData():
    print("c")

writer = csv.DictWriter(sys.stdout, args.COLUMN, delimiter=SEPARATOR, quotechar=QUOTECHAR, quoting=csv.QUOTE_ALL)
writer.writeheader()


line=""
while True:
    try:
        line=ldif.next()
    except StopIteration:
        break

    lineData=line.split(": ", 1)
    if len(lineData)<2:
        continue # Registrar dados

    lineData[1]=lineData[1].replace('\n', '')
    print(lineData)

endAll(0)