# coding: utf-8
"""
Task and Work subclasses related to structure relaxations.
"""
from __future__ import annotations

from abipy.core.structure import Structure
from abipy.dynamics.hist import HistRobot
from abipy.abio.inputs import AbinitInput
from abipy.flowtk.tasks import RelaxTask
from abipy.flowtk.works import Work


class RelaxTaskWithTargetDilatmx(RelaxTask):
    """
    Relaxation Task that iteratively reduces the value of
    dilatmx until a target value is reached.

    .. rubric:: Inheritance Diagram
    .. inheritance-diagram:: RelaxTaskWithTargetDilatmx
    """

    @classmethod
    def from_scf_input(cls, scf_input: AbinitInput,
                       target_dilatmx=1.001, workdir=None, manager=None) -> RelaxTaskWithTargetDilatmx
        """
        Build an instance from an Abinit input representing a GS calculation.
        """
        relax_input = scf_input.new_with_vars(
            optcell=2,
            ionmov=22,
            ecutsm=0.5,
            dilatmx=1.1,
        )

        task = cls(relax_input, workdir=workdir, manager=manager)
        task.target_dilatmx = target_dilatmx

        return task

    def on_ok(self):
        """
        This method is called once the `Task` has reached status S_OK.
        """
        actual_dilatmx = self.input["dilatmx"]
        if self.target_dilatmx < actual_dilatmx:
            self.reduce_dilatmx(self.target_dilatmx)
            self.history.info('Converging dilatmx. Value reduced from {} to {}.'
                               .format(actual_dilatmx, self.input['dilatmx']))
            self.restart()
            self.finalized = False
            return dict(returncode=0, message="Restarting task with smaller dilatmx")
        else:
            self.history.info(f"Reached target dilatmx: {self.target_dilatmx}. Finalized set to True")
            self.finalized = True
            return dict(returncode=0, message="Restarting task with smaller dilatmx")


class RelaxTaskWithM3gnet(RelaxTask):
    """
    Relaxation Task that performs an initial relaxation with m3gnet
    followed by an ab-initio relaxation with Abinit.

    .. rubric:: Inheritance Diagram
    .. inheritance-diagram:: RelaxTaskWithM3gnet
    """

    @classmethod
    def from_scf_input(cls, scf_input: AbinitInput) -> RelaxTaskWithM3gnet
        """
        Build an instance from an Abinit input representing a GS calculation.
        """
        # Run m3gnet.
        relaxed_structure = scf_input.structure.relax(calculator="m3gnet", relax_cell=True)
        relaxed_structure.__class__ = Structure

        #relaxed_structure = relaxed_structure.refine()
        relaxed_structure = relaxed_structure.abi_sanitize()

        relax_input = scf_input.new_with_vars(
            ionmov=22,
            optcell=2,
            ecutsm=0.5,
            dilatmx=1.1,
            #toldff=1e-6,
            #tolmxf=1e-5,
            #ntime=100,
        )

        relax_input.set_structure(relaxed_structure)

        return cls(relax_input)


class AbiVsM3gnetWork(Work):
    """
    This work is mainly used for benchmarking/testing purposes.
    It contains two tasks performing two structural relaxations.
    The first task performs a full ab-initio relaxation starting from the input structure,
    The second one performs an initial relaxation using m3gnet before calling Abinit.

    .. rubric:: Inheritance Diagram
    .. inheritance-diagram:: AbiVsM3gnetWork
    """

    @classmethod
    def from_relax_input(cls, relax_input: AbinitInput) -> AbiVsM3gnetWork:
        """Build the work from an input for structura relaxations."""
        work = cls()
        work.abi_relax_task = work.register_relax_task(relax_input)
        work.m3g_relax_task = m3g_task = RelaxTaskWithM3gnet(relax_input)
        work.register_task(m3g_task)
        return work

    def on_all_ok(self):
        """
        This method is called once the `Work` is completed i.e. when all tasks have reached status S_OK.
        """
        filepaths = [work.abi_relax_task.hist_path, work.m3g_relax_task.hist_path]
        with HistRobot.from_files(filepaths) as robot:
            print(robot)
            df = robot.get_dataframe()
            df.to_excel(self.outdir.path_in("abivsm3gnet.xlsx"))

            with robot.get_pyscript(self.outdir.path_in("hist_robot.py")) as script:
                script.add_text("""
df = robot.get_dataframe()
for what in robot.what_list:
    robot.gridplot(what=what, tight_layout=True)
    #robot.combiplot(what=what, tight_layout=True)
""")

        return super().on_all_ok()
