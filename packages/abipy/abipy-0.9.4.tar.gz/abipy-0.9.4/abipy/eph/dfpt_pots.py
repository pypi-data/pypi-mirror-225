
import numpy as np

#from abipy.electrons.denpot import DfptPotNcFile
from abipy.tools.numtools import transpose_last3dims
from abipy.iotools import xsf


from abipy.electrons.denpot import _NcFileWithField


class DfptPotNcFile(_NcFileWithField):
    """
    POT file produced by the DFPT part containing the
    first order derivative of the KS potential in real space.

    .. rubric:: Inheritance Diagram
    .. inheritance-diagram:: DfptPotNcFile
    """
    field_name = "first_order_potential"


class DfptQPotsAnalyzer(object):

    def __init__(self, potname_gamma, potnames_qdir):

        self.potfiles_qdir, qpts, pertcases = [], [], []
        for i, path in enumerate(potnames_qdir):
            ncfile = DfptPotNcFile.from_file(path)
            hdr = ncfile.hdr
            #print(ncfile)
            print("qptn:", hdr.qptn, "pertcase:", hdr.pertcase)
            self.potfiles_qdir.append(ncfile)
            pertcases.append(hdr.pertcase)
            qpts.append(hdr.qptn)

            if i == 0:
                nspden = hdr.nspden
                ngfft = ncfile.reader.read_ngfft3()
                print("ngggt", ngfft)
                structure = ncfile.reader.read_structure()
            #print(ncfile.vks1)

        # Consistency check.
        #for

        # Rearrange qpoints if they are not already ordered.

        # Build [nq, ] array with the potentials
        # number_of_components, number_of_grid_points_vector3, number_of_grid_points_vector2,
        # number_of_grid_points_vector1, real_or_complex_first_order_potential

        for i, ncfile in enumerate(self.potfiles_qdir):
            rc = ncfile.reader.read_dimvalue("real_or_complex_first_order_potential")
            var = ncfile.reader.read_variable("first_order_potential")

            print("var.shape:", var.shape)
            if rc == 1:
                arr = var[:] + 0j
            elif rc == 2:
                arr = var[..., 0] + 1j * var[..., 1]
            else:
                raise ValueError("Invalid real_or_complex_first_order_potential: %d" % rc)
            arr = np.reshape(arr, -1)

            if i == 0:
                s = arr.shape + (len(self.potfiles_qdir), )
                print("arr.shape:", arr.shape, "s:", s)
                values = np.empty(s, dtype=arr.dtype)

            values[:, i] = arr

        print(values.dtype, values.shape)

        # Compute q --> 0 limit by linear extrapolation.
        qlens = structure.reciprocal_lattice.reciprocal_lattice.norm(qpts)
        print(qlens)

        #from scipy.interpolate import InterpolatedUnivariateSpline
        #f = InterpolatedUnivariateSpline(x, y, w=None, bbox=[None, None], k=3, ext=0, check_finite=False)

        from scipy.interpolate import interp1d
        #f = interp1d(x, y, kind='linear', axis=-1, copy=True, bounds_error=None, fill_value=nan, assume_sorted=False)
        f = interp1d(qlens, values, kind='linear', axis=-1, fill_value='extrapolate')
                     #copy=True, bounds_error=None, fill_value=nan, assume_sorted=False)

        extrap_values = f(0)
        print(extrap_values.shape)

        ispden = 0
        for i in range(len(qlens) + 1):
            if i == len(qlens):
                datar = extrap_values
            else:
                datar = values[:, i]
            filename = "foo%d.xsf" % i
            datar.shape = (nspden,) + tuple(ngfft)
            with open(filename, mode="wt") as fh:
                xsf.xsf_write_structure(fh, structure)
                xsf.xsf_write_data(fh, structure, datar[ispden], add_replicas=True, cplx_mode="abs")

        self.potfile_gamma = DfptPotNcFile.from_file(potname_gamma)
        ncfile = self.potfile_gamma
        rc = ncfile.reader.read_dimvalue("real_or_complex_first_order_potential")
        var = ncfile.reader.read_variable("first_order_potential")
        datar = var[:] + 0j
        filename = "foo_gamma.xsf"
        with open(filename, mode="wt") as fh:
            xsf.xsf_write_structure(fh, structure)
            xsf.xsf_write_data(fh, structure, datar[ispden], add_replicas=True, cplx_mode="abs")


class DfptInterpAnalyzer(object):

    def __init__(self, dfpt_pot_filepath, v1qg_nolr_filepath, v1vq_withlr_filepath):
        ispden = 0
        with DfptPotNcFile.from_file(dfpt_pot_filepath) as ncfile:
            r = ncfile.reader
            structure = r.read_structure()
            hdr = ncfile.hdr
            pertcase_c = hdr.pertcase - 1
            idir = pertcase_c % 3
            ipert = (pertcase_c - idir) // 3
            print("q-point:", hdr.qptn, "Fortran pertcase:", hdr.pertcase, "C idir:", idir, "C ipert:", ipert)

            # On netcdf file, we have array of shape.
            # (number_of_components, number_of_grid_points_vector3, number_of_grid_points_vector2,
            #   number_of_grid_points_vector1, real_or_complex_first_order_potential)
            rc = r.read_dimvalue("real_or_complex_first_order_potential")
            var = r.read_variable("first_order_potential")
            #print("var.shape:", var.shape)
            if rc == 1:
                datar = var[ispden, ...] + 0j
            elif rc == 2:
                datar = var[ispden, ..., 0] + 1j * var[ispden, ..., 1]
            else:
                raise ValueError("Invalid real_or_complex_first_order_potential: %d" % rc)

        def xsf_write(filepath, datar):
            with open(filepath, mode="wt") as fh:
                xsf.xsf_write_structure(fh, structure)
                cplx_mode = "re"
                #cplx_mode = "im"
                #cplx_mode = "abs"
                xsf.xsf_write_data(fh, structure, datar, cplx_mode=cplx_mode)

        self.dfpt_pot = transpose_last3dims(datar)
        xsf_write("dfpt.xsf", self.dfpt_pot)

        from abipy.eph.v1qavg import V1qAvgFile
        d = {}

        for path, key in zip([v1qg_nolr_filepath, v1vq_withlr_filepath], ["nolr", "withlr"]):
            with V1qAvgFile(path) as ncfile:
                r = ncfile.reader
                ngfft = r.read_value("ngfft")
                d[key] = {}
                for var_name in ("v1r_interpolated", "v1r_lrmodel"):
                    # nctkarr_t("v1r_interpolated", "dp", "two, nfft, nspden, natom3")
                    var = r.read_variable(var_name)
                    datar = var[pertcase_c, ispden, :, 0] + 1j * var[pertcase_c, ispden, :, 1]
                    # Because we are reading Fortran data (z,y,x) and xsf_write_data expects (..., x, y, z)
                    datar = transpose_last3dims(datar)
                    datar = np.reshape(datar, ngfft)
                    d[key][var_name] = datar
                    assert np.all(datar.shape == self.dfpt_pot.shape)

                    path = key + "_" + var_name + ".xsf"
                    xsf_write(path, datar)

        other = d["withlr"]["v1r_interpolated"]
        datar = self.dfpt_pot - other
        print("DFT AVG Re", np.average(self.dfpt_pot.real), ", DFT AVG Im", np.average(self.dfpt_pot.imag))
        print("INTERP AVG Re", np.average(other.real), ", INTERP AVG Im", np.average(other.imag))
        print("diff wrt DFPT with LR model", np.sum(np.abs(datar)) / datar.size)
        xsf_write("dfpt_minus_withlr.xsf", datar)

        other = d["nolr"]["v1r_interpolated"]
        datar = self.dfpt_pot - other
        print("DFT AVG Re", np.average(self.dfpt_pot.real), ", DFT AVG Im", np.average(self.dfpt_pot.imag))
        print("NOLR INTERP AVG Re", np.average(other.real), ", NOLR INTERP AVG Im", np.average(other.imag))
        print("diff wrt DFPT without LR model", np.sum(np.abs(datar)) / datar.size)
        xsf_write("dfpt_minus_nolr.xsf", datar)

        datar = d["withlr"]["v1r_interpolated"] - d["nolr"]["v1r_interpolated"]
        xsf_write("interp_lrnolr_diff.xsf", datar)


if __name__ == "__main__":
    import sys
    #potname_gamma, potnames_qdir = sys.argv[1], sys.argv[2:]
    #ana = DfptQPotsAnalyzer(potname_gamma, potnames_qdir)

    dfpt_pot_filepath, v1qg_nolr_filepath, v1vq_withlr_filepath = sys.argv[1:]
    ana = DfptInterpAnalyzer(dfpt_pot_filepath, v1qg_nolr_filepath, v1vq_withlr_filepath)
