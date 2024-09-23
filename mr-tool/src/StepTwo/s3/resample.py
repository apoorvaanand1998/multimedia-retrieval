import csv
import vedo as vd
import math

def subsample(csv_path: str, output_path: str) -> list[int]:
    lines_changed = []
    l             = 0
    with open(csv_path) as curr_stat_file:
        with open(output_path, 'w') as new_stat_file:
            cs_reader = csv.reader(curr_stat_file, delimiter=',', quotechar='"')
            ns_writer = csv.writer(new_stat_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in cs_reader:
                v = int(row[2])
                f = int(row[3])
                m = vd.load(row[0])
                
                while v <= 4000 or v >= 6000:
                    m_copy = m.copy()
                    lines_changed.append(l)
                    if v >= 6000:
                        m.decimate(n=5000)
                        v = m.dataset.GetNumberOfPoints()
                    elif v <= 4000:
                        m1 = m.copy()
                        m2 = m.copy()
                        m3 = m.copy()
                        m4 = m.copy()
                        m.subdivide()
                        m1.subdivide()
                        m2.subdivide()
                        m3.subdivide()
                        m4.subdivide()

                        vs = [(m, m.dataset.GetNumberOfPoints()),
                              (m1, m1.dataset.GetNumberOfPoints()),
                              (m2, m2.dataset.GetNumberOfPoints()),
                              (m3, m3.dataset.GetNumberOfPoints()),
                              (m4, m4.dataset.GetNumberOfPoints())]
                        print(vs)
                        res  = max(vs, key=lambda x : x[1])
                        m, v = res
                    if v == 0:
                        m = m_copy
                        v = m.dataset.GetNumberOfPoints()
                        f = m.dataset.GetNumberOfCells()
                        print(m)
                        vd.show(m)
                        break
                    f = m.dataset.GetNumberOfPoints()
                    print(m)
                    vd.show(m)
                ns_writer.writerow([row[0], m, v, f])
                l += 1
            return lines_changed

subsample("../Output/stats.csv", "../Output/resampled.csv")        