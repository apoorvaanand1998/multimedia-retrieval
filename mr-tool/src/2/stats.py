import csv 

## 2.2

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

print(avg_shape("../Output/stats.csv"))