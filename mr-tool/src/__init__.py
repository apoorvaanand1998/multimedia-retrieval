from vedo import load, show
from sys import argv

def main():
    objFile = argv[1]
    mesh    = load("ShapeDatabase_INFOMR/" + objFile)
    show(mesh)

main()