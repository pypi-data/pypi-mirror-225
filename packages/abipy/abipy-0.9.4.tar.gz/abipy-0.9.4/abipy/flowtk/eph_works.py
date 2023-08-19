# coding: utf-8
"""
Works for electron-phonon calculations (high-level interface)
"""
from __future__ import annotations

import numpy as np

from abipy.abio.inputs import AbinitInput
from abipy.dfpt.ddb import DdbFile
from .nodes import Node
from .works import Work


class MeshKey:

    @classmethod
    def as_meshkey(cls, obj) -> MeshKey:
        """
        Convert an object into a MeshKey.
        """
        if isinstance(obj, (tuple, list)):
            return cls(divs=obj, shifts=(0, 0, 0))
        elif isinstance(obj, cls):
            return obj
        else:
            raise TypeError("Don't know how to convert type `%s` into a MeshKey" % type(obj))

    @classmethod
    def from_divs(cls, divs) -> MeshKey:
        """
        Build object from the number of division assuming a Gamma-centered mesh.
        """
        return cls(divs=divs, shifts=(0, 0, 0))

    def __init__(self, divs, shifts):
        """
        Args:
            divs:
            shifts:
        """
        self.divs = np.array(divs, np.int)
        assert len(self.divs) == 3 and all(n > 0 for n in self.divs)

        self.shifts = []
        for s in np.array(shifts).tolist():
            if abs(s) < 1e-12:
                s = 0.0
            elif abs(s - 0.5) < 1e-12:
                s = 0.5
            else:
                raise ValueError("Expecting 0 or 0.5 for shift component while got %s" % str(s))
            self.shifts.append(s)

        self.shifts = np.reshape(self.shifts, (-1, 3))
        self.nshifts = len(self.shifts)
        #print(self)

    def __str__(self) -> str:
        lines = []; app = lines.append
        app("divs: %s" % str(self.divs))
        app("nshifts: %s" % self.nshifts)
        app("shifts: %s" % str(self.shifts))
        return "\n".join(lines)

    def __eq__(self, other):
        if other is None: return False
        return (self.nshifts == other.nshifts and
                np.all(self.divs == other.divs) and
                np.all(self.shifts == other.shifts)
               )

    def __hash__(self):
        #print(self.nshifts, tuple(self.divs.ravel()), tuple(self.shifts.ravel()))
        return hash((self.nshifts, tuple(self.divs.ravel()), tuple(self.shifts.ravel())))

    def __mul__(self, integer):
        return self.__class__([int(integer) * s for s in self.divs_tuple], self.shifts)

    def must_be_multiple_or_equal_to(self, other):
        errors = []
        app = errors.append

        if self.nshifts != other.nshifts:
            app("MeshKey objects have different nshifts")

        if np.any(self.shifts != other.shifts):
            app("MeshKey objects have different shifts")

        #ratios = np.array(self.divs_tuple) / np.array(other.divs_tuple)
        #if ratios[0] != ratios

        if errors:
            raise ValueError("\n".join(errors))


class SertaConvergenceWork(Work):
    r"""
    """

    @staticmethod
    def build_kqs_grids_from_nksmall_range(structure, start, stop, step, double_grid_fact):
        # [k-mesh    , qmesh    , double-grid],
        kqd_grids = []
        for nksmall in range(start, stop, step):
            k_mesh = MeshKey.from_divs(structure.calc_ngkpt(nksmall))
            q_mesh = k_mesh
            d_mesh = k_mesh * double_grid_fact
            kqd_grids.append((k_mesh, q_mesh, d_mesh))

        return kqd_grids

    @classmethod
    def from_scf_input(cls, scf_input, kqd_grids, den_node, ddb_node, dvdb_node,
                       boxcutmin=1.5, mixprec=1, manager=None):
        """
        Build a work for the computation of phonon-limited mobilities within SERTA
        from an input file representing a GS calculation.

        Args:
            workdir: Working directory.
            scf_input: Input for the GS SCF run.
            den_node:
            ddb_node:
            dvdb_node:
            boxcutmin, mixprec: Abinit input variables. See documentation.
            manager: |TaskManager| object.
        """
        new = cls(manager=manager)

        # Save variables used to generate the EPH input.
        new.scf_input = scf_input.deepcopy()
        new.boxcutmin = boxcutmin
        new.mixprec = mixprec

        # Convert input to node instances.
        new.den_node = Node.as_node(den_node)
        new.ddb_node = Node.as_node(ddb_node)
        new.dvdb_node = Node.as_node(dvdb_node)

        # Get the q-mesh from the DDB file
        ddb_filepath = new.ddb_node.opath_from_ext("DDB")
        with DdbFile(ddb_filepath) as ddb_file:
            new.ddb_ngqpt = ddb_file.guessed_ngqpt

        # Remember: k-mesh >= q-mesh.
        #kqd_grids = [
        #  [ k-mesh    , qmesh    , double-grid],
        #  [ [(4, 4, 4), (4, 4, 4), (4, 4, 4)],
        #  [ [(4, 4, 4), (4, 4, 4), (8, 8, 8)],
        #  [ [(8, 8, 8), (4, 4, 4), (16, 16, 16)],
        #]

        # Build list of (k, q, d) meshes where d stands for double-grid.
        new.kqd_grids = []
        unique_kmeshes = set()
        for kqd in kqd_grids:
            k_mesh = MeshKey.as_meshkey(kqd[0])
            q_mesh = MeshKey.as_meshkey(kqd[1])
            d_mesh = MeshKey.as_meshkey(kqd[2])

            #d_mesh.must_be_multiple_or_equal_to(k_mesh)
            #d_mesh.must_be_multiple_or_equal_to(q_mesh)

            new.kqd_grids.append((k_mesh, q_mesh, d_mesh))
            unique_kmeshes.add(k_mesh)
            unique_kmeshes.add(d_mesh)

        # Perform NSCF calculation for each k-mesh.
        new.nscf_task_kmesh = {}
        for k_mesh in unique_kmeshes:
            # TODO: Rationalize this parth
            nscf_inp = scf_input.make_edos_input(ngkpt=k_mesh.divs, shiftk=k_mesh.shifts,
                                                 tolwfr=1e-20, nscf_nband=None)
            task = new.register_nscf_task(nscf_inp, deps={new.den_node: "DEN"})
            new.nscf_task_kmesh[k_mesh] = task

        new.on_all_ok_done = False
        return new

    def on_all_ok(self):
        """
        This method is called once the `Work` is completed i.e. when all the tasks
        have reached status S_OK.
        """
        if not self.on_all_ok_done:
            for k_mesh, q_mesh, d_mesh in self.kqd_grids:
                nscf_task = self.nscf_task_kmesh[k_mesh]

                eph_inp = self.scf_input.new_with_vars(
                    optdriver=7,
                    eph_task=-4,              # Compute imaginary part only.
                    ddb_ngqpt=self.ddb_ngqpt,  # q-mesh associated to the DDB file.
                    # The K-mesh associated to the WFK file (coarse one).
                    ngkpt=k_mesh.divs,
                    nshiftk=k_mesh.nshifts,
                    shiftk=k_mesh.shifts,
                    prtphdos=0,
                    boxcutmin=self.boxcutmin,
                    mixprec=self.mixprec,
                    symsigma=1,
                    eph_intmeth=2,
                    #
                    tmesh=[0, 300, 2],
                    sigma_erange="0.2 0.2 eV",  # Select kpts in fine mesh within this energy window.
                    #
                    eph_ngqpt_fine=q_mesh.divs,
                )

                #if kmesh != d_mesh:
                #    # Activate double-grid tecnique.
                #    eph_inp.set_vars(
                #)

                deps = {self.ddb_node: "DDB", self.dvdb_node: "DVDB", nscf_task: "WFK"}
                eph_task = self.register_eph_task(eph_inp, deps=deps)
                #self.eph_tasks.append(eph_task)

            # TODO: Support for eph_restart, compute sigma_erange automatically in Fortran
            # TODO: Use TransportRobot?
            #for eph_task in self.eph_tasks:
            self.flow.allocate()
            self.finalized = False
            self.on_all_ok_done = True
            self.flow.build_and_pickle_dump()

        return super().on_all_ok()

    #def get_results(self, **kwargs):
    #    """
    #    Method called once the calculations are completed.
    #    The base version returns a dictionary task_name: TaskResults for each task in self.
    #    """
    #    results = self.Results.from_node(self)
    #    return results
