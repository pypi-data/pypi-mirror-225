"""Tests for gkq module."""
import abipy.data as abidata

from abipy.core.testing import AbipyTest
from abipy.eph.gkq import GkqFile, GkqRobot


class GkqFileTest(AbipyTest):

    def test_gkq_file(self):
        """Testing GkqFile."""
        return
        with GkqFile(abidata.ref_file("al_888k_161616q_A2F.nc")) as ncfile:
            repr(ncfile); str(ncfile)
            assert ncfile.to_string(verbose=2)
            #assert ncfile.params["nspinor"] == ncfile.nspinor
            #assert ncfile.structure.formula == "Ga1 P1" and len(ncfile.structure) == 1

            #assert ncfile.ebands.
            #assert ncfile.uses_interpolated_dvdb
            #assert ncfile.params

            #assert ncfile.qpoint
            #assert ncfile.phfreqs_ha
            #assert ncfile.phdispl_cart_bohr
            #assert ncfile.phdispl_red
            #assert ncfile.becks_cart
            #assert ncfile.epsinf_cart
            #assert ncfile.eigens_ks

            # Test matplotlib methods
            if self.has_matplotlib():
                assert ncfile.plot(mode="phonon", with_glr=True, show=False)
                assert ncfile.plot(mode="atom", with_glr=False, show=False)
                assert ncfile.plot_diff_with_other(ncfile, mode="phonon", show=False)

            # Test jupyter notebook creation
            if self.has_nbformat():
                ncfile.write_notebook(nbpath=self.get_tmpname(text=True))


#class GkqRobotTest(AbipyTest):
#
#    def test_gkq_robot(self):
#        """Testing V1qAvgRobot."""
#        files = abidata.ref_files(
#                "al_888k_161616q_A2F.nc",
#        )
#
#        with GkqRobot.from_files(files[0]) as robot:
#            robot.add_file("same_a2f", files[0])
#            assert len(robot) == 2
#            repr(robot); str(robot)
#            robot.to_string(verbose=2)
#
#             robot.kpoints
#
#            # Test matplotlib methods
#            if self.has_matplotlib():
#                assert robot.plot_gkq2_qpath(band_kq, band_k, kpoint=0,
#                                             with_glr=False, qdamp=None, nu_list=None, # spherical_average=False,
#                                             ax=None, fontsize=8, eph_wtol=EPH_WTOL, **kwargs):
#
#                assert robot.plot_gkq2_diff(self, iref=0, **kwargs)
#
#            # Test jupyter notebook creation
#            if self.has_nbformat():
#                robot.write_notebook(nbpath=self.get_tmpname(text=True))
