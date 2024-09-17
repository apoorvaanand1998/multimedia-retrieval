import csv 
import math
## s2.s2

def min_max(csv_path: str) -> tuple[tuple[int, int], tuple[int, int]]:
    """((min vc, max vc), (min fc, max fc))"""
    max_vc, max_fc = 0, 0
    min_vc, min_fc = math.inf, math.inf

    minvc, maxvc, minfc, maxfc = "", "", "", ""

    with open(csv_path) as stat_file:
        stat_reader = csv.reader(stat_file, delimiter=',', quotechar='"')
        for row in stat_reader:
            if int(row[2]) > max_vc: max_vc, maxvc = float(row[2]), row[0]
            if int(row[2]) < min_vc: min_vc, minvc = float(row[2]), row[0]
            if int(row[3]) > max_fc: max_fc, maxfc = float(row[3]), row[0]
            if int(row[3]) < min_fc: min_fc, minfc = float(row[3]), row[0]

    print(minvc, maxvc, minfc, maxfc)
    return ((min_vc, max_vc), (min_fc, max_fc))

def avg_shape(csv_path: str) -> tuple[int, int]:
    """(average vertex count, average face count)"""
    n, total_vc, total_fc = 0, 0, 0
    with open(csv_path) as stat_file:
        stat_reader = csv.reader(stat_file, delimiter=',', quotechar='"')
        for row in stat_reader:
            total_vc += int(row[2])
            total_fc += int(row[3])
            n        += 1
    return (total_vc/n, total_fc/n)

def check_all_faces_are_triangles(csv_path: str) -> bool:
    with open(csv_path) as stat_file:
        stat_reader = csv.reader(stat_file, delimiter=',', quotechar='"')
        for row in stat_reader:
            face_count = int(row[3])
            tri_count  = eval(row[4])[0]
            if face_count != tri_count:
                print(row)
                return False
    return True

print(min_max("../Output_Temp/stats.csv"))