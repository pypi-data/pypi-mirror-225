# coding: utf-8
"""
Work subclasses for the computation Linear Response Hubbard U and Hund's J with LRUJ post-processor
"""
from __future__ import annotations

from abipy.core.structure import Structure
from abipy.flowtk.works import Work

from typing import List, Any


class LrujWork(Work):

    @classmethod
    def from_pawujv(cls, scf_input, pawujv_ha_list, workdir=None, manager=None) -> LrujWork:
        work = cls(workdir=workdir, manager=manager)

        #scf_task = work.register_scf_task(scf_input)
        #for pawujv in pawujv_ha:
        #    new_inp = scf_input.new_with_vars(pawujv=pawujv, prtwf=-1)
        #    work.register_scf_task(new_inp, deps={scf_task: "WFK"})

        return work

    def on_all_ok(self):
        """
        This method is called once the `Work` is completed i.e. when all tasks have reached status S_OK.
        """



def test_lruj_work():
    # Antiferro. II NiO, 4 atom | Hubbard U on Ni 3d | LMac 2022  ##
    from abipy.core.structure import Structure

    pseudos = []
    structure = Structure.from_abistring("""
#################################################################
## Automatic test/tutorial for ABINIT:                         ##
## Linear Response Hubbard U and Hund's J (LRUJ)               ##
## post-processing utility for the determination of            ##
## said parameters in situ and ab initio                       ##
##    Initialization of WFK files                              ##
##                                                             ##
## Antiferro. II NiO, 4 atom | Hubbard U on Ni 3d | LMac 2022  ##
#################################################################

#Run Parameters
nstep 30                          #Higher than normal because of magnetic state
tolvrs 10d-12
ecut 10
pawecutdg 20
chkprim 0                         #Will complain otherwise with AFII magnetic state
occopt 0
nband 26                          #24 occupied + 2 unoccupied
occ  24*1.0 2*0.0 24*1.0 2*0.0

#Structural Parameters
natom 4                           #NOTE: Converge U(J) wrt supercell size!
ntypat 3                          #Specify perturbed Ni atom as a separate species
typat 1 2 3 3                     #to that of the other Ni atom.
znucl 28 28 8                     #First two are Ni atoms, last two are O
acell 3*7.8800
xred  0.0000000000 0.0000000000 0.0000000000
      0.5000000000 0.5000000000 0.5000000000
      0.2500000000 0.2500000000 0.2500000000
      0.7500000000 0.7500000000 0.7500000000

rprim 0.5000000000 0.5000000000 1.0000000000
      1.0000000000 0.5000000000 0.5000000000
      0.5000000000 1.0000000000 0.5000000000

#Spin Parameters
nsppol 2
nspden 2
nspinor 1
spinat 0 0 3                      #Set high to enforce convergence to high magnetic state
       0 0 -3                     #Otherwise, it may collapse to non-magnetic state
       0 0 0
       0 0 0

#Kpoint Grid
kptopt 1                          #Monkhorst-Pack Mesh
chksymbreak 0                     #Don't check for symmetry breaking
ngkpt 4 4 4

# DFT+U
usepawu 1                         #Alert Abinit to use of DFT+U
lpawu 2 2 1                       #Subspaces of interest: Ni 3d, O 2p
upawu 0.0 0.0 0.0 eV              #Raw (non-corrected) XC functional required to establish U(J)
jpawu 0.0 0.0 0.0 eV
dmatpuopt 3

#Pseudos
pp_dirpath "$ABI_PSPDIR/Pseudodojo_paw_pbe_standard/"
pseudos "Ni.xml,Ni.xml,O.xml"     #Use same pseudopotential for both Ni atoms
""")
    print(structure)
    print(structure.to_abivars())

    scf_input = None

    pawujv_ha = [1, 2, 3]
    work = LrujWork.from_pawujv(scf_input, pawujv_ha)
    print(work)


if __name__ == "__main__":
    test_lruj_work()
