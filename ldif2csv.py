SEPARATOR = ';'
JOINER = '|'

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

ldif = os.open(args.INPUT, os.O_RDONLY)

writer = csv.DictWriter(sys.stdout, args.COLUMN, delimiter=SEPARATOR, quotechar=QUOTECHAR, quoting=csv.QUOTE_ALL)
writer.writeheader()



os.close(ldif)