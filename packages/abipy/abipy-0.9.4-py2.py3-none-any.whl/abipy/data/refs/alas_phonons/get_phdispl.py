#!/usr/bin/env python

from abipy.abilab import abiopen

with abiopen("trf2_3_DDB") as ddb:
    # ifcflag 0 means that no Fourier interpolation is performed in anaddb
    # hence the q-point must belong the IBZ used in the DFPT calculation.
    # ifcflag 1 activates the Fourier interpolation of the dynamical matrix.
    # In this case, so one can pass an arbitrary q-point to get interpolated quantities.
    phbands = ddb.anaget_phmodes_at_qpoint(qpoint=[0.0, 0, 0], ifcflag=0)

    print("Ph frequencies in eV", phbands.phfreqs)

    #phdispl_cart: [nqpt, 3*natom, 3*natom] array with displacement in Cartesian coordinates in Angstrom.
    #    The last dimension stores the cartesian components.
    #    This is an array of complex numbers

    mode = 0
    print(f"phdispl_cart for phonon mode {mode}:\n", phbands.phdispl_cart[0, mode])
