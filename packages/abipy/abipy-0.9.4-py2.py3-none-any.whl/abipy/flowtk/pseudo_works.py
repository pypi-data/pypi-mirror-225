"""
"""
from __future__ import annotations

import abc
import os
import json
import numpy as np

#from typing import
#from monty.io import FileLock
#from pymatgen.core.xcfunc import XcFunc
from abipy.core.structure import Structure
#from abipy.abio.factories import ion_ioncell_relax_input
#from abipy.flowtk.abiobjects import SpinMode, Smearing, KSampling, RelaxationMethod
#from abipy.flowtk.tasks import RelaxTask
#from abipy.flowtk.works import Work, RelaxWork, PhononWork
#from pseudo_dojo.core.dojoreport import DojoReport, dojo_dfact_esults, dojo_gbrv_results
#from pseudo_dojo.refdata.gbrv import gbrv_database
#from pseudo_dojo.refdata.deltafactor import df_database
#from pseudo_dojo.refdata.lantanides.database import raren_database

from abipy.electrons.gsr import GsrRobot
from abipy.abio.inputs import AbinitInput
from abipy.abio.factories import gs_input
#from abipy.flowtk.pseudos import Pseudo
from abipy.flowtk.works import Work
from abipy.flowtk.flows import Flow


#class PseudoTestsFlow(Flow):

    #@classmethod
    #def from_pseudo_filepath(cls, pseudo_filepath, ecut_list, workdir):
    #    flow = cls(workdir=workdir)
    #    flow.pseudo_filepath = os.path.abspath(pseudo_filepath)
    #    scf_input = _build_scf_input_from_pseudo(pseudo)
    #    work = GsEcutConvWork.from_scf_input(cls, scf_input, pseudo, ecut_list)
    #    flow.register_work(work)

    #    return flow

    #def on_all_ok(self):
    #    """
    #    This method is called when all tasks have reached S_OK.
    #    It reads the energies and the volumes from the GSR file
    #    """
    #    for work in self:
    #        with open(work.outdir.path_in("ecut_conv.json"), "wt") as fh:
    #            data[work.KEY] = json.read(fh)

    #    with open(self.outdir.path_in("ecut_conv.json"), "wt") as fh:
    #        json.dump(data, fh, indent=4, sort_keys=True)

#class _PseudoFlow(Flow):
#    """Base class for Flow."""


class _PseudoWork(Work):
    """Base class for Works."""
    #__metaclass__ = abc.ABCMeta

    #@abc.abstractproperty
    #def dojo_pseudo(self):
    #    """:class:`Pseudo` object"""

    #@abc.abstractproperty
    #def dojo_trial(self):
    #    """String identifying the DOJO trial. Used to write results in the DOJO_REPORT."""

    #@property
    #def djrepo_path(self):
    #    """Path to the djrepo file."""
    #    root, ext = os.path.splitext(self.dojo_pseudo.filepath)
    #    return root + ".djrepo"

    #def add_entry_to_dojoreport(self, entry, overwrite_data=False, pop_trial=False):
    #    """
    #    Write/update the DOJO_REPORT section of the pseudopotential.
    #    Important parameters such as the name of the dojo_trial and the energy cutoff
    #    are provided by the sub-class.
    #    Client code is responsible for preparing the dictionary with the data.

    #    Args:
    #        entry: Dictionary with results.
    #        overwrite_data: If False, the routine raises an exception if this entry is
    #            already filled.
    #        pop_trial: True if the trial should be removed before adding the new entry.
    #    """
    #    djrepo = self.djrepo_path
    #    self.history.info("Writing dojreport data to %s" % djrepo)

    #    # Update file content with Filelock.
    #    with FileLock(djrepo):
    #        # Read report from file.
    #        file_report = DojoReport.from_file(djrepo)

    #        # Create new entry if not already there
    #        dojo_trial = self.dojo_trial

    #        if pop_trial:
    #            file_report.pop(dojo_trial, None)

    #        if dojo_trial not in file_report:
    #            file_report[dojo_trial] = {}

    #        # Convert float to string with 1 decimal digit.
    #        dojo_ecut = "%.1f" % self.ecut

    #        # Check that we are not going to overwrite data.
    #        if dojo_ecut in file_report[dojo_trial]:
    #            if not overwrite_data:
    #                raise RuntimeError("dojo_ecut %s already exists in %s. Cannot overwrite data" %
    #                        (dojo_ecut, dojo_trial))
    #            else:
    #                file_report[dojo_trial].pop(dojo_ecut)

    #        # Update file_report by adding the new entry and write new file
    #        file_report[dojo_trial][dojo_ecut] = entry

    #        # Write new dojo report and update the pseudo attribute
    #        file_report.json_write()
    #        self._pseudo.dojo_report = file_report


class GsEcutConvWork(_PseudoWork):
    """
    This work computes GS properties for different value of ecut
    and save the results in the outdata directory of the Work.
    """

    KEY = "gs_vs_ecut"

    @classmethod
    def from_pseudo(cls, pseudo, ecut_list: list, a=4) -> GsEcutConvWork:
        """
        High-level constructor to build the work from a pseudo and a list of ecut energies in Ha.
        """
        species = [pseudo.symbol]
        structure = Structure.fcc(a, species, primitive=True, units="ang")

        #scf_input = AbinitInput(structure, pseudo)
        scf_input = gs_input(structure, pseudo,
                 kppa=None, ecut=None, pawecutdg=None, scf_nband=None, accuracy="normal", spin_mode="unpolarized",
                 smearing="fermi_dirac:0.1 eV", charge=0.0, scf_algorithm=None)

        # Some optimization.
        scf_input.set_vars(nstep=50, prtwf=-1)

        return cls.from_scf_input(scf_input, ecut_list)

    @classmethod
    def from_scf_input(cls, scf_input: AbinitInput, ecut_list: list) -> GsEcutConvWork:
        """
        Low-level constructor to build the work from a template and a list of ecut energies.
        """
        work = cls()
        for ecut in ecut_list:
            work.register_scf_task(scf_input.new_with_vars(ecut=ecut))

        return work

    def on_all_ok(self):
        """
        This method is called when all tasks in GsEcutWork have reached S_OK.
        It reads the energies and the volumes from the GSR file
        and produces the `gs_vs_ecut.json` file in the outdir of the work.
        """
        with GsrRobot.from_work(self) as gsr_robot:
            df = gsr_robot.get_dataframe(with_geo=False)
            df.to_excel(self.outdir.path_in("gs_vs_ecut.xlsx"))

            with gsr_robot.get_pyscript(self.outdir.path_in("gsr_robot.py")) as script:
                script.add_text("""
# Set convergence criteria for absolute convergence in ytols_dict.
# NB: Energies are in eV, pressure in GPa.

ytols_dict = dict(energy_per_atom=1e-3, pressure=1e-2)
ca = robot.get_convergence_analyzer("ecut", ytols_dict)
print(ca)
ca.plot()
""")

        return super().on_all_ok()


#class GsEcutConvFlowPseudos(Flow):
#    """
#    """
#
#    @classmethod
#    def from_scf_input(cls, scf_input, pseudos_to_test, ecut_list, workdir=None):
#        flow = cls(workdir=workdir)
#        for pseudo in pseudos_to_test:
#            flow.append_work(GsEcutConvWork.from_scf_input(scf_input, pseudo, ecut_list))
#
#        return flow
#
#    def on_all_ok(self):
#        """
#        This method is called when all works in the Flow have reached S_OK.
#        """
#        for work in self:
#            with open(work.outdir.path_in("gs_vs_ecut.json"), "wt") as fh:
#                data = json.load(fh)



class PhEcutConvWork(_PseudoWork):
    """
    This work computes DFPT phonons for different ecut values
    and save the results in the outdata directory of the Work.
    """

    KEY = "phonons_vs_ecut"

    def from_scf_input(cls, scf_input, pseudo, ecut_list, workdir=None):
        work = cls(workdir=workdir)
        work.natom = len(scf_input.structure)
        work.ecut_list = list(ecut_list)
        #for ecut in self.ecut_list:
        #    work.register_scf_task(scf_input.new_with_vars(ecut=ecut))

        return work

    def on_all_ok(self):
        """
        This method is called when all tasks have reached S_OK.
        It reads the energies and the volumes from the GSR file
        """
        energy_per_atom_ev = []
        #pressure_gpa = []
        for task in self:
            with task.open_ddb() as ddb:
                print(ddb)

        data = dict(
            natom=self.natom,
            #ecut_list=self.ecut_list,
            #energy_per_atom_ev=energy_per_atom_ev,
            #pressure_gpa=pressure_gpa,
        )

        with open(self.outdir.path_in("ecut_conv.json"), "wt") as fh:
            json.dump(data, fh, indent=4, sort_keys=True)
