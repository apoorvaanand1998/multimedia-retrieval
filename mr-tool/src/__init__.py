from vedo import load, show
from sys import argv

def main():
    objFile = argv[1]
    meshes  = load("ShapeDatabase_INFOMR/" + objFile)
    show(meshes)

main()