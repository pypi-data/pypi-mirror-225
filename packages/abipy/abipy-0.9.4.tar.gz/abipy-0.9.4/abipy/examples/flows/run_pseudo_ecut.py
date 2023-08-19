#!/usr/bin/env python
r"""
Convergence study in ecut for pseudo
====================================

This script shows how to ...
"""

import os
import sys
import abipy.data as data
#import abipy.abilab as abilab

from abipy import flowtk


def build_flow(options):
    # Working directory (default is the name of the script with '.py' removed and "run_" replaced by "flow_")
    if not options.workdir:
        options.workdir = os.path.basename(sys.argv[0]).replace(".py", "").replace("run_","flow_")

    pseudo = data.pseudo("O.psp8")
    #pseudo = data.pseudo("Si.fhi")

    flow = flowtk.Flow(workdir=options.workdir)
    from abipy.flowtk.pseudo_works import GsEcutConvWork

    ecut_list = [35, 40, 45, 50, 55, 60, 65]
    #ecut_list = [35, 40, 45]
    work = GsEcutConvWork.from_pseudo(pseudo, ecut_list)
    flow.register_work(work)

    return flow


# This block generates the thumbnails in the AbiPy gallery.
# You can safely REMOVE this part if you are using this script for production runs.
if os.getenv("READTHEDOCS", False):
    __name__ = None
    import tempfile
    options = flowtk.build_flow_main_parser().parse_args(["-w", tempfile.mkdtemp()])
    build_flow(options).graphviz_imshow()


@flowtk.flow_main
def main(options):
    return build_flow(options)


if __name__ == "__main__":
    sys.exit(main())


############################################################################
#
# Run the script with:
#
#     run_si_gwr.py -s
#
# The last three tasks (``w0_t3``, ``w0_t4``, ``w0_t5``) are the SigmaTask who have produced
# a netcdf file with the GW results with different number of bands.
# We can check this with the command:
#
#    abirun.py flow_si_g0w0/ listext SIGRES
#
# .. code-block:: bash
#
#       Found 3 files with extension `SIGRES` produced by the flow
#       File                                        Size [Mb]    Node_ID  Node Class
#       ----------------------------------------  -----------  ---------  ------------
#       flow_si_g0w0/w0/t3/outdata/out_SIGRES.nc         0.05     241325  SigmaTask
#       flow_si_g0w0/w0/t4/outdata/out_SIGRES.nc         0.08     241326  SigmaTask
#       flow_si_g0w0/w0/t5/outdata/out_SIGRES.nc         0.13     241327  SigmaTask
#
# Let's use the SIGRES robot to collect and analyze the results:
#
#    abirun.py flow_si_g0w0/ robot SIGRES
#
# and then, inside the ipython terminal, type:
#
# .. code-block:: ipython
#
#       In [1]: df = robot.get_dataframe()
#       In [2]: df
#       Out[2]:
#                                                 nsppol     qpgap            ecutwfn  \
#       flow_si_g0w0/w0/t3/outdata/out_SIGRES.nc       1  3.627960  5.914381651684836
#       flow_si_g0w0/w0/t4/outdata/out_SIGRES.nc       1  3.531781  5.914381651684836
#       flow_si_g0w0/w0/t5/outdata/out_SIGRES.nc       1  3.512285  5.914381651684836
#
#                                                            ecuteps  \
#       flow_si_g0w0/w0/t3/outdata/out_SIGRES.nc  3.6964885323070074
#       flow_si_g0w0/w0/t4/outdata/out_SIGRES.nc  3.6964885323070074
#       flow_si_g0w0/w0/t5/outdata/out_SIGRES.nc  3.6964885323070074
#
#                                                          ecutsigx scr_nband  \
#       flow_si_g0w0/w0/t3/outdata/out_SIGRES.nc  5.914381651684846        25
#       flow_si_g0w0/w0/t4/outdata/out_SIGRES.nc  5.914381651684846        25
#       flow_si_g0w0/w0/t5/outdata/out_SIGRES.nc  5.914381651684846        25
#
#                                                sigma_nband gwcalctyp scissor_ene  \
#       flow_si_g0w0/w0/t3/outdata/out_SIGRES.nc          10         0         0.0
#       flow_si_g0w0/w0/t4/outdata/out_SIGRES.nc          20         0         0.0
#       flow_si_g0w0/w0/t5/outdata/out_SIGRES.nc          30         0         0.0
#
#                                                 nkibz
#       flow_si_g0w0/w0/t3/outdata/out_SIGRES.nc      6
#       flow_si_g0w0/w0/t4/outdata/out_SIGRES.nc      6
#       flow_si_g0w0/w0/t5/outdata/out_SIGRES.nc      6
#
#       In [3]: %matplotlib
#       In [4]: df.plot("sigma_nband", "qpgap", marker="o")
#
# .. image:: https://github.com/abinit/abipy_assets/blob/master/run_si_g0w0.png?raw=true
#    :alt: QP results in Si plotted vs the KS energy e0.
#
