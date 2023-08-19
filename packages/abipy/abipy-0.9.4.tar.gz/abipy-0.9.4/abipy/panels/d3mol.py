"""
All credits go to
https://discourse.holoviz.org/t/panel-for-chemistry-3d-candidate-for-gallery-post/2264
"""

import panel as pn
import param


class ThreeDMolViewer(param.Parameterized):
    #pdb = param.String(
    #    doc="""
    #    The value describes a PDB ID to be loaded into the viewer."""
    #)
    #href = param.String(doc="""The value is a URL to a molecular data file.""")
    #file_format = param.ObjectSelector(
    #    default="pdb",
    #    objects=["pdb", "sdf", "xyz", "mol2", "cube"],
    #    doc="""The value is the file format (default pdb; can be pdb, sdf, xyz, mol2, or cube)""",
    #)
    background_color = param.Color(default="#ffffff")
    background_alpha = param.Number(
        default=1.0,
        bounds=(0.0, 1.0),
        step=0.01,
        doc="""
        The background alpha (default opaque: 1.0).""",
    )
    select = param.String(doc="""The value is an AtomSpec selection specification.""")
    style = param.ObjectSelector(
        default="sphere",
        objects=["line", "cross", "stick", "sphere", "cartoon"],
        doc="""The value is a style specification. One of 'line', 'cross', 'stick', 'sphere' or 'cartoon'. Default is 'stick'""",
    )
    surface = param.String(doc="""A surface style specification""")
    labelres = param.String(doc="""A residue label style specification.""")
    zoomto = param.String(doc="""An AtomSpec selection specification to zoom to""")

    def __init__(self, structure, height=400, **params):
        super().__init__(**params)
        self.structure = structure
        from pymatgen.io.xyz import XYZ
        self.xyz_string = str(XYZ(structure))
        #xyz_string = structure.to(fmt="xyz")
        print(self.xyz_string)
        self.file_format="xyz"
        self.view = pn.pane.HTML(self._repr_html_(), height=height)

    def _repr_html_(self):
        data_id = "foo"
        html = f"""

<script src="https://3Dmol.org/build/3Dmol-min.js" async></script>
<div style="height: 100%; width: 100%; position: relative;" class='viewer_3Dmoljs' data-element='{data_id}'
"""

        #if self.pdb:
        #    html += f" data-pdb='{self.pdb}' "
        if self.file_format and self.file_format != "pdb":
            html += f" data-type='{self.file_format}' "
        if self.background_color:
            html += f" data-backgroundcolor='{self.background_color}' "
        if self.background_alpha:
            html += f" data-backgroundalpha='{self.background_alpha}' "
        if self.select:
            html += f" data-select='{self.select}' "
        if self.style:
            html += f" data-style='{self.style}' "
        if self.surface:
            html += f" data-surface='{self.surface}' "
        if self.labelres:
            html += f" data-labelres='{self.labelres}' "
        if self.zoomto:
            html += f" data-zoomto='{self.zoomto}' "
        #html += "></div> "
        html += f"></div> <textarea hidden id='{data_id}'> {self.xyz_string} </textarea>"
        print(html)

#        return """
#<script src="https://3Dmol.org/build/3Dmol-min.js" async></script>
#        <div style="height: 400px; width: 400px; position: relative;" class='viewer_3Dmoljs' data-pdb='1YCR' data-backgroundcolor='0xffffff'
#        data-select1='chain:A' data-style1='cartoon:color=spectrum' data-surface1='opacity:.7;color:white' data-select2='chain:B' data-style2='stick'></div>
#"""

        return html

    @param.depends(
        #"pdb",
        #"href",
        #"file_format",
        "background_color",
        "background_alpha",
        "style",
        "surface",
        "labelres",
        "zoomto",
        watch=True,
    )
    def _update_view(self, *events):
        self.view.object = self._repr_html_()


if __name__ == "__main__":
    pn.extension(sizing_mode="stretch_width")

    from abipy import abilab
    import abipy.data as abidata
    structure = abilab.Structure.from_file(abidata.cif_file("si.cif"))
    #jsmol = ThreeDMolViewer(pdb="2POR", height=600)
    jsmol = ThreeDMolViewer(structure, height=600)

    pn.template.FastListTemplate(
        title="3DMol Viewer",
        sidebar=[pn.Param(jsmol)],
        main=[jsmol.view],
    ).show()
    #).servable()
