SEPARATOR = ';'
JOINER = '|'
QUOTECHAR = '"'

import sys
import os
import fileinput
import argparse
import csv
from io import StringIO

def isDigit(c):
    #return c.isdigit() or c.isalpha()
    return True #TEMPORARIO
ws = {'\n'}


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


c=''
state=0
column = StringIO()
value = StringIO()
while True:
    print "Unimplemented"

endAll(0)