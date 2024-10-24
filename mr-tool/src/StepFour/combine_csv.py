import csv

def test():
    with open ('../../Output/ShapePropDesc/Rocket.csv') as curr_csv:
        r = csv.reader(curr_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in r:
            print(row)
            break

test()            