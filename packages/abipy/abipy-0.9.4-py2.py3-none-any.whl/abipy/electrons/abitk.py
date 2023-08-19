# coding: utf-8
"""
This module provides objects to read the netcdf files produced by the abitk Fortran tool.
The majority of these files are used for testing/debugging purposes.
"""
import abipy.core.abinit_units as abu

from monty.functools import lazy_property
from monty.string import marquee, list_strings
from abipy.core.mixins import AbinitNcFile, Has_Structure, NotebookWriter
from abipy.electrons.ebands import ElectronsReader
from abipy.tools.plotting import add_fig_kwargs, get_axarray_fig_plt  #get_ax_fig_plt,


class ZinvConvFile(AbinitNcFile, Has_Structure, NotebookWriter):
    """
    .. rubric:: Inheritance Diagram
    .. inheritance-diagram:: ZinvConvFile
    """
    @classmethod
    def from_file(cls, filepath):
        """Initialize the object from a netcdf file."""
        return cls(filepath)

    def __init__(self, filepath):
        super().__init__(filepath)
        self.reader = r = ElectronsReader(filepath)

        self.ngqpt_list = r.read_value("ngqpt_list")
        self.broad_list = r.read_value("broad_list")

    def __str__(self):
        """String representation."""
        return self.to_string()

    def to_string(self, verbose=0):
        """String representation."""
        lines = []; app = lines.append

        app(marquee("File Info", mark="="))
        app(self.filestat(as_string=True))
        app("")
        app(self.structure.to_string(verbose=verbose, title="Structure"))
        app("")
        app("ngqpt_list: %s" % str(self.ngqpt_list))
        app("broad_list (eV): %s" % str(self.broad_list * abu.Ha_to_eV))

        return "\n".join(lines)

    def close(self):
        self.reader.close()

    @property
    def structure(self):
        """|Structure| object."""
        return self.reader.read_structure()

    @lazy_property
    def params(self):
        """:class:`OrderedDict` with parameters that might be subject to convergence studies."""
        return {}

    @add_fig_kwargs
    def plot_conv_wrt_qmesh(self, fontsize=8, **kwargs):
        r"""
        Plot t

        Args:
            fontsize: fontsize for legends and titles

        Returns: |matplotlib-Figure|
        """
        num_broad = len(self.broad_list)
        num_meshes = len(self.ngqpt_list)
        wmesh_eV = self.reader.read_value("wmesh") * abu.Ha_to_eV

        # Build grid of plots.
        num_plots, ncols, nrows = num_broad, 1, 1
        if num_plots > 1:
            ncols = 1
            nrows = (num_plots // ncols) + (num_plots % ncols)

        ax_list, fig, plt = get_axarray_fig_plt(None, nrows=nrows, ncols=ncols,
                                                sharex=True, sharey=True, squeeze=False)
        ax_list = ax_list.ravel()

        what_list = ["cauchy_ppart_simple", "cauchy_ppart_simtet", ]
        for ii, what in enumerate(what_list):
            # nctkarr_t("dos_simple", "dp", "nw, num_broad, num_meshes")
            values = self.reader.read_value(what)
            for ibroad, ax in enumerate(ax_list):
                broad_eV = float(self.broad_list[ibroad]) * abu.Ha_to_eV
                for imesh in range(num_meshes):
                    label = "%s, %s, broad %.3f" % (what, str(self.ngqpt_list[imesh]), broad_eV)
                    ax.plot(wmesh_eV, values[imesh, ibroad], label=label) #, color=color)
                    if ii == 0:
                        ax.set_title("broad = %.3f (eV)" % (broad_eV))

        for iax, ax in enumerate(ax_list):
            ax.grid(True)
            ax.legend(loc="best", shadow=True, fontsize=fontsize)
            if iax == len(ax_list) - 1:
                ax.set_xlabel('Energy (eV)')

        fig.suptitle("Convergence of integration methods for fixed broadening")
        return fig

    @add_fig_kwargs
    def plot_conv_method(self, fontsize=8, **kwargs):
        r"""
        Plot t

        Args:
            fontsize: fontsize for legends and titles

        Returns: |matplotlib-Figure|
        """
        num_broad = len(self.broad_list)
        num_meshes = len(self.ngqpt_list)
        wmesh_eV = self.reader.read_value("wmesh") * abu.Ha_to_eV
        what_list = ["cauchy_ppart_simple", "cauchy_ppart_simtet", ]

        # Build grid of plots.
        num_plots, ncols, nrows = len(what_list), 1, 1
        if num_plots > 1:
            ncols = 1
            nrows = (num_plots // ncols) + (num_plots % ncols)

        ax_list, fig, plt = get_axarray_fig_plt(None, nrows=nrows, ncols=ncols,
                                                sharex=True, sharey=True, squeeze=False)
        ax_list = ax_list.ravel()

        linestyles = ["--", '-', ':', '-.']
        cmap = plt.get_cmap("viridis")

        for ii, (what, ax) in enumerate(zip(what_list, ax_list)):
            ax.set_title(what)
            # nctkarr_t("dos_simple", "dp", "nw, num_broad, num_meshes")
            values = self.reader.read_value(what)
            for imesh in range(num_meshes):
                ls = linestyles[imesh % len(linestyles)]
                for ibroad, broad in enumerate(self.broad_list):
                    broad_eV = float(broad) * abu.Ha_to_eV
                    color = cmap(ibroad / len(self.broad_list))
                    label = "%s, %s, broad %.3f" % (what, str(self.ngqpt_list[imesh]), broad_eV)
                    ax.plot(wmesh_eV, values[imesh, ibroad], label=label, color=color, ls=ls)

            ax.grid(True)
            ax.legend(loc="best", shadow=True, fontsize=fontsize)
            if ii == len(ax_list) - 1:
                ax.set_xlabel('Energy (eV)')

        fig.suptitle("Convergence of integration methods")
        return fig

    def yield_figs(self, **kwargs):  # pragma: no cover
        """
        This function *generates* a predefined list of matplotlib figures with minimal input from the user.
        """
        yield self.plot_conv_wrt_qmesh(show=False)
        yield self.plot_conv_method(show=False)

    def write_notebook(self, nbpath=None):
        """
        Write a jupyter_ notebook to ``nbpath``. If nbpath is None, a temporay file in the current
        working directory is created. Return path to the notebook.
        """
        nbformat, nbv, nb = self.get_nbformat_nbv_nb(title=None)

        nb.cells.extend([
            nbv.new_code_cell("eskw = abilab.abiopen('%s')" % self.filepath),
            nbv.new_code_cell("print(eskw)"),
        ])

        return self._write_nb_nbpath(nb, nbpath)


class TetraTestFile(AbinitNcFile, Has_Structure, NotebookWriter):
    """
    .. rubric:: Inheritance Diagram
    .. inheritance-diagram:: TetraTestFile
    """
    @classmethod
    def from_file(cls, filepath):
        """Initialize the object from a netcdf file."""
        return cls(filepath)

    def __init__(self, filepath):
        super().__init__(filepath)
        self.reader = r = ElectronsReader(filepath)

        #self.nqibz = r.read_dimvalue("nqibz")
        #self.eig = r.read_value("eig")

    def __str__(self):
        """String representation."""
        return self.to_string()

    def to_string(self, verbose=0):
        """String representation."""
        lines = []; app = lines.append

        app(marquee("File Info", mark="="))
        app(self.filestat(as_string=True))
        app("")
        app(self.structure.to_string(verbose=verbose, title="Structure"))
        app("")
        #app("ngqpt_list: %s" % str(self.ngqpt_list))
        #app("broad_list (eV): %s" % str(self.broad_list * abu.Ha_to_eV))

        return "\n".join(lines)

    def close(self):
        self.reader.close()

    @property
    def structure(self):
        """|Structure| object."""
        return self.reader.read_structure()

    @lazy_property
    def params(self):
        """:class:`OrderedDict` with parameters that might be subject to convergence studies."""
        return {}

    @add_fig_kwargs
    def plot(self, fontsize=8, ekind="parabola", what_list=("dos", "idos", "cauchy_ppart"), **kwargs):
        r"""
        Plot t

        Args:
            fontsize: fontsize for legends and titles

        Returns: |matplotlib-Figure|
        """
        wmesh_eV = self.reader.read_value("wmesh") * abu.Ha_to_eV

        # Conventions for variable names produced by Fortran code.
        # key = strcat(ekind, "_", algo)
        # dos_vname = strcat("dos_", key)
        # idos_vname = strcat("idos_", key)
        # ppart_vname = strcat("cauchy_ppart_", key)
        def inspect_vars(prefix):
            d = {}
            for name, var in self.reader.rootgrp.variables.items():
                if name.startswith(prefix):
                    algo = name.replace(prefix, "", 1)
                    d[algo] = var[:]

            print("for prefix", prefix, "found", d.keys())
            return {k: d[k] for k in sorted(d.keys())}

        data = {}
        for what in list_strings(what_list):
            data[what] = inspect_vars(what + "_" + ekind + "_")

        # Build grid of plots.
        num_plots, ncols, nrows = len(data), 1, len(data)

        ax_list, fig, plt = get_axarray_fig_plt(None, nrows=nrows, ncols=ncols,
                                                sharex=True, sharey=False, squeeze=False)
        ax_list = ax_list.ravel()

        for iax, ((what, d), ax) in enumerate(zip(data.items(), ax_list)):
            ax.set_title("%s %s" % (ekind, what))
            ax.grid(True)
            for k, values in d.items():
                #if "_lv" in k: continue
                ax.plot(wmesh_eV, values, label=k) #, color=color)

            ax.legend(loc="best", shadow=True, fontsize=fontsize)
            if iax == len(ax_list) - 1:
                ax.set_xlabel('Energy (eV)')

        return fig

    def yield_figs(self, **kwargs):  # pragma: no cover
        """
        This function *generates* a predefined list of matplotlib figures with minimal input from the user.
        """
        for ekind in ("parabola", "flat"):
            yield self.plot(ekind=ekind, what_list=("dos", "idos"), show=False)
            yield self.plot(ekind=ekind, what_list="cauchy_ppart", show=False)

    def write_notebook(self, nbpath=None):
        """
        Write a jupyter_ notebook to ``nbpath``. If nbpath is None, a temporay file in the current
        working directory is created. Return path to the notebook.
        """
        nbformat, nbv, nb = self.get_nbformat_nbv_nb(title=None)

        nb.cells.extend([
            nbv.new_code_cell("eskw = abilab.abiopen('%s')" % self.filepath),
            nbv.new_code_cell("print(eskw)"),
        ])

        return self._write_nb_nbpath(nb, nbpath)
