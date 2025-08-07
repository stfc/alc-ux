import ipywidgets as ipw
import aiidalab_widgets_base as awb
import traitlets as tl 

from aiida.orm import StructureData

class StructureStepModel(tl.HasTraits):
    structure = tl.Instance(StructureData, allow_none=True)
    structureFile = tl.Unicode("", allow_none=True)

    @property
    def hasStructure(self):
        return self.structure is not None 

    @property
    def hasStructureFile(self):
        return self.structureFile != "" 
    
    @property 
    def isPeriodic(self):
        if self.hasStructure:
            return any(self.structure.pbc)
        return False 


class StructureWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    def __init__(self, model: StructureStepModel, **kwargs):
        super().__init__(children=[], **kwargs)
        self.rendered = False 
        self.model = model 

        self.info = ipw.HTML(
            """
                <p>
                    Load in a structure to start the workflow. The structure can either be in AiiDA StructureData format, or as a raw input file if the 
                    file format is not directly supported by AiiDA (e.g. ChemShell .pun files).
                </p>
            """
        )

        self.tabs = ipw.Tab()
        self.tabs.set_title(0, "AiiDA Structure")
        self.tabs.set_title(1, "Input File") 

        self.structureManager = awb.StructureManagerWidget(
            importers=[
                awb.StructureUploadWidget(title="From computer"),
                awb.StructureBrowserWidget(title="AiiDA database", query_types=(StructureData,)),
                awb.SmilesWidget(title="SMILES"), 
                awb.StructureExamplesWidget(
                    title="From Examples",
                    examples=[
                        # ("Silicon oxide", "../miscellaneous/structures/SiO2.xyz"),
                        # ("Silicon", "../miscellaneous/structures/Si.xyz"),
                    ],
                ),
            ],
            editors=[
                awb.BasicStructureEditor(title="Basic Editor"),
                awb.BasicCellEditor(title="Basic Cell Editor"),
            ],
            node_class="StructureData",
            storable=False,
        )
        ipw.dlink(
            (self.structureManager, "structure_node"),
            (self.model, "structure")
        )

        self.fileInputW = ipw.VBox()
        self.fileInputBtn = ipw.FileUpload(
            accept="", 
            multiple=False,
            description="Upload Structure File",
        )
        self.fileInputHandle = ipw.Text(
            value="",
            placeholder="",
            description="Structure File",
            disabled=True,
            layout={"width": "80%"},
        )
        self.fileInputW.children = [
            self.fileInputHandle,
            self.fileInputBtn, 
        ]

        

        self.tabs.children = [
            self.structureManager, 
            self.fileInputW,
        ]

        return 
    
    def render(self):
        if self.rendered:
            return 
        
        submitBtn = ipw.Button(
            description="Submit Structure",
            disbled=False,
            button_style="success",
            tooltip="Submit the structure to the workflow",
            icon="check",
            layout={"margin": "auto", "width": "80%"}
        )
        submitBtn.on_click(self.submitStructure)

        self.children = [
            self.info, 
            self.tabs,
            submitBtn,
        ]
        self.rendered = True 
        return 
    
    def submitStructure(self, _):
        self.structureManager.store_structure()
        return 