import csv 

## 2.2
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

print(check_all_faces_are_triangles("../Output/stats.csv"))