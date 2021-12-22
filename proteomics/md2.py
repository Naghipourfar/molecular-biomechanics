from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
import MDAnalysis as md
import nglview as ng
from sys import stdout


def read_pdb(path: str):
    file0 = open(path, 'r')
    counter = 0
    for line in file0:
        if counter < 10:
            print(line)
        counter += 1

    u = md.Universe(path)
    ng.show_mdanalysis(u, gui=True)
