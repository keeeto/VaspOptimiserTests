from __future__ import print_function
from ase.dft.kpoints import *
import numpy as np
import os
import ase
from ase.calculators.vasp import Vasp
from datetime import datetime
import csv


def isif2(bulk,max_steps=100):
    calc_opt = Vasp(system = "System",
                   istart = 0,iniwav = 1,icharg = 0,gamma=True,reciprocal=True,
                   prec="Accurate", lreal = False, algo = "Normal", encut = 400.00,
                   nelm = 200, ediff = 1e-6, xc='PBE', kspacing=0.442,
                   ediffg = -1e-2, nsw = max_steps, ibrion = 1, isif = 2, isym = 0,
		   npar = 4,kpar = 8,
                   ismear = 0)

    bulk.set_calculator(calc_opt)
    energy = bulk.get_potential_energy()
    print("Energy: {}".format(energy))
    cmdstring = "mv OUTCAR OUTCAR.i2"
    os.system(cmdstring)

def isif7(bulk,max_steps=4):
    calc_opt = Vasp(system = "System",
                   istart = 1,iniwav = 1,icharg = 0,gamma=True,reciprocal=True,
                   prec="Accurate", lreal = False, algo = "Normal", encut = 400.00,
                   nelm = 200, ediff = 1e-6, xc='PBE', kspacing=0.442,
                   ediffg = -1e-2, nsw = max_steps, ibrion = 1, isif = 7, isym = 0,
		   npar = 4,kpar = 8,
                   ismear = 0)
    bulk.set_calculator(calc_opt)
    energy = bulk.get_potential_energy()
    print("Energy: {}".format(energy))
    cmdstring = "mv OUTCAR OUTCAR.i7"
    os.system(cmdstring)

def isif4(bulk,max_steps=10):
    calc_opt = Vasp(system = "System",
                   istart = 1,iniwav = 1,icharg = 0,gamma=True,reciprocal=True,
                   prec="Accurate", lreal = False, algo = "Normal", encut = 400.00,
                   nelm = 200, ediff = 1e-6, xc='PBE', kspacing=0.442,
                   ediffg = -1e-2, nsw = max_steps, ibrion = 1, isif = 4, isym = 0,
		   npar = 4,kpar = 8,
                   ismear = 0)

    bulk.set_calculator(calc_opt)
    energy = bulk.get_potential_energy()
    print("Energy: {}".format(energy))
    cmdstring = "mv OUTCAR OUTCAR.i4"
    os.system(cmdstring)

def isif3(bulk,max_steps=20):
    calc_opt = Vasp(system = "System",
                   istart = 1,iniwav = 1,icharg = 0,gamma=True,reciprocal=True,
                   prec="Accurate", lreal = False, algo = "Normal", encut = 400.00,
                   nelm = 200, ediff = 1e-6, xc='PBE', kspacing=0.442,
                   ediffg = -1e-2, nsw = max_steps, ibrion = 1, isif = 3, isym = 0,
		   npar = 4,kpar = 8,
                   ismear = 0)
    bulk.set_calculator(calc_opt)
    energy = bulk.get_potential_energy()
    print("Energy: {}".format(energy))
    cmdstring = "mv OUTCAR OUTCAR.i3"
    os.system(cmdstring)
    return energy

def check_finished(infile='OUTCAR'):
    search = open(infile)
    finished = False
    for line in search:
        if 'reached required accuracy - stopping structural energy minimisation' in line:
	    finished = True
    return finished

# Build workflow here:
structures = []
for filename in os.listdir('./'):
    if filename.endswith(".cif"):
	structures.append(filename)

#structures = [ 'GaN.cif', 'CdS_mp-672_conventional_standard.cif', 'SrO_mp-2472_conventional_standard.cif']
startTime = datetime.now()

for structure in structures:
    run_times = [0.,0.]
    energies = [0.,0.]
    bulk = ase.io.read(structure)
    os.environ['VASP_BINARY'] = "/home/e05/shared/red/vasp5"
    os.environ['VASP_COMMAND'] = "aprun -n $NPROC $VASP_BINARY > vasp.out"
## The 2-7-3 
    finished = False
    while not finished:
        isif2(bulk)
        bulk = ase.io.read('CONTCAR')
        isif7(bulk)
        bulk = ase.io.read('CONTCAR')
        isif4(bulk)
        bulk = ase.io.read('CONTCAR')
        energy = isif3(bulk,max_steps=10)
        bulk = ase.io.read('CONTCAR')
        energies[0] = isif3(bulk,max_steps=1)
        finished = check_finished('OUTCAR.i3')
        bulk = ase.io.read('CONTCAR')

    print("Runtime: {}".format(datetime.now() - startTime))
    run_times[0] = (datetime.now() - startTime)
    cmdstring = "rm CONTCAR"
    os.system(cmdstring)
    cmdstring = "rm CONTCAR"
    os.system(cmdstring)
    ## The straight 3
    startTime = datetime.now()
    bulk = ase.io.read(structure)
    finished = False
    while not finished:
        if os.path.exists('CONTCAR'):
            bulk = ase.io.read('CONTCAR')
        energy = isif2(bulk,max_steps=6)
        bulk = ase.io.read('CONTCAR')
        energy = isif3(bulk,max_steps=6)
        bulk = ase.io.read('CONTCAR')
        energies[1] = isif3(bulk,max_steps=1)
        finished = check_finished('OUTCAR.i3')
    run_times[1] = (datetime.now() - startTime)
    print("Runtime: {}".format(datetime.now() - startTime))
    cmdstring = "rm CONTCAR WAVECAR CHG* OSZI* IBZ* REPORT PCDAT vasprun.xml"
    print("Finished with {}".format(structure))
    os.system(cmdstring)

    with open('timings.csv','a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(run_times)
    with open('energies.csv','a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(energies)
    cmdstring = "mv %s %s.done" % (structure,structure)
    os.system(cmdstring)

