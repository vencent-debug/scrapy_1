import csv

f = open("test.csv", 'rt')
try:
    for row in csv.reader(f, delimiter=' ', skipinitialspace=True):
        print(' '.join(row))
finally:
        f.close()