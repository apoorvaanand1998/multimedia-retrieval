import csv
import vedo as vd

def subsample(csv_path: str, output_path: str) -> list[int]:
    lines_changed = []
    l             = 0
    with open(csv_path) as curr_stat_file:
        with open(output_path, 'w') as new_stat_file:
            cs_reader = csv.reader(curr_stat_file, delimiter=',', quotechar='"')
            ns_writer = csv.writer(new_stat_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in cs_reader:
                l += 1
                v  = int(row[2])
                f  = int(row[3])
                m  = vd.load(row[0])
                
                if not cond(v, f):
                    lines_changed.append(l)
                    i = 0
                    while not cond(v, f):
                        print("i%2", i%2, fs(m)[i%2][0])
                        m = fs(m)[i%2][1]
                        v = m.dataset.GetNumberOfPoints()
                        f = m.dataset.GetNumberOfCells()
                        print("New", m)
                        i += 1
                    vd.show(m)
                ns_writer.writerow([row[0], v, f])
            return lines_changed

def cond(v, f):
    return (v >= 4000 and v <= 6000) or (f >= 9000 and f <= 11000)

def fs(m):
    return [("sub", vd.Mesh.subdivide(m, 10)), ("dec", vd.Mesh.decimate(m, 0.1))]

subsample("../Output/stats.csv", "../Output/resampled.csv")        