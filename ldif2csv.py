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
    c=ldif.read(1)
    #sys.stdout.write(c)
    if(c==""):
        break

    if state==0:
        column.truncate(0)
        value.truncate(0)
        if c in ws:
            state=5
            continue
        if isDigit(c):
            state=1
            ldif.seek(-1, 1)
            continue
    elif state==1:
        if c == ':':
            state=2
            continue
        if isDigit(c):
            column.write(unicode(c, 'unicode-escape'))
            continue
    elif state==2:
        if c == ' ':
            state=3
            continue
        if isDigit(c):
            state=4
            ldif.seek(-1, 1)
            continue
    elif state==3:
        if isDigit(c):
            state=4
            ldif.seek(-1, 1)
            continue
    elif state==4:
        if c in ws:
            writeValue(column.getvalue(), value.getvalue())
            state=0
            continue
        if isDigit(c):
            value.write(unicode(c, 'unicode-escape'))
            continue
    elif state==5:
        print("a")
        if c in ws:
            print("b1")
            writeData()
            state=0
            continue
        if isDigit(c):
            print("b2")
            state=1
            ldif.seek(-1, 1)
            continue
    else:
        sys.stderr.write("Unknown state "+str(state))
        endAll(-1)

    sys.stderr.write("Unknown lexical error, state "+str(state)+" char "+c)
    endAll(-1)

endAll(0)