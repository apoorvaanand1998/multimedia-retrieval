import csv
import os
import utils
import anand

SHAPE_DESCRIPTORS_PATH = os.path.join("..", "..", "Output", "ShapePropDesc")
GLOBAL_DESCRIPTORS_PATH = os.path.join("Output", "Descriptors", "remeshed_normalized_filled_ShapeDB", "descriptors.csv")

def main():
    db = "remeshed_normalized_filled_ShapeDB"
    global_descriptors = utils.get_output_descriptors(db)

    for idx, global_descriptor in enumerate(global_descriptors):
        class_name = global_descriptor.path.split('/')[-2].split('.')[0]
        c_mesh = class_name + "/" + global_descriptor.name.split('.')[0]
        # d is one of 'a3', 'd1', 'd2', 'd3', 'd4' """

        a3 = anand.get_vec('a3', c_mesh, db)
        d1 = anand.get_vec('d1', c_mesh, db)
        d2 = anand.get_vec('d2', c_mesh, db)
        d3 = anand.get_vec('d3', c_mesh, db)
        d4 = anand.get_vec('d4', c_mesh, db)

        if a3 is None or d1 is None or d2 is None or d3 is None or d4 is None:
            print("Skipping " + c_mesh)
            print("A3: " + str(a3))
            print("D1: " + str(d1))
            print("D2: " + str(d2))
            print("D3: " + str(d3))
            print("D4: " + str(d4))
            continue

        global_descriptor.set_a3(a3[0])
        global_descriptor.set_d1(d1[0])
        global_descriptor.set_d2(d2[0])
        global_descriptor.set_d3(d3[0])
        global_descriptor.set_d4(d4[0])

        print(str(idx + 1) + "/" + str(len(global_descriptors)))

    utils.save_output_descriptors(db + "_united", global_descriptors)
main()
