import ipywidgets as ipw
import aiidalab_widgets_base as awb

class StructureWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    def __init__(self, **kwargs):
        super().__init__(children=[], **kwargs)
        self.rendered = False 

        self.structureManager = awb.StructureManagerWidget(
            importers=[
                awb.StructureUploadWidget(title="From computer"),
                awb.StructureBrowserWidget(title="AiiDA database"),
                awb.SmilesWidget(title="SMILES"),  # requires OpenBabel!s
                awb.StructureExamplesWidget(
                    title="From Examples",
                    examples=[
                        ("Silicon oxide", "../miscellaneous/structures/SiO2.xyz"),
                        ("Silicon", "../miscellaneous/structures/Si.xyz"),
                    ],
                ),
            ],
            editors=[
                awb.BasicStructureEditor(title="Basic Editor"),
                awb.BasicCellEditor(title="Basic Cell Editor"),
            ],
        )

        return 
    
    def render(self):
        if self.rendered:
            return 
        
        self.children = [self.structureManager]
        self.rendered = True 
        return 