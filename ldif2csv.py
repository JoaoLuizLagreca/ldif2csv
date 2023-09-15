SEPARATOR = ';'
JOINER = '|'
QUOTECHAR = '"'

import sys
import os
import fileinput
import argparse
import csv

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
def endAll(code):
    ldif.close()
    exit(code)

writer = csv.DictWriter(sys.stdout, args.COLUMN, delimiter=SEPARATOR, quotechar=QUOTECHAR, quoting=csv.QUOTE_ALL)
writer.writeheader()

data={}
c=''
state=0
while True:
    c=ldif.next()

    if state==0:
        continue
    else:
        sys.stderr("Unknown state "+state)
        endAll(-1)

endAll(0)