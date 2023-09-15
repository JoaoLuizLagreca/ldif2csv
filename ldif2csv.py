import sys
import os
import fileinput
import argparse

prs = argparse.ArgumentParser(prog='ldif2csv')
prs.add_argument('INPUT', help='LDIF input file')
prs.add_argument('COLUMN', help='Columns to parse to CSV file', nargs='+')
args = prs.parse_args()

if not os.path.exists(args.INPUT):
    sys.stderr.write("Input file doesn't exists")
    exit(129)
if os.path.isdir(args.INPUT):
    sys.stderr.write("The input specified is a directory")
    exit(123)

