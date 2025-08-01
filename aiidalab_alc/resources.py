import ipywidgets as ipw
import traitlets as tl 
import aiidalab_widgets_base as awb 

class ComputationalResourcesModel(tl.HasTraits):
    
    defaultGuide = """
        <p> 
            Configure the remote computational resources for the workflow.
        </p>
    """

class ComputationalResourcesWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    def __init__(self, **kwargs):
        super().__init__(children=[], **kwargs)
        self.model = ComputationalResourcesModel()
        self.rendered = False 

        self.header = ipw.HTML(
            """
            <h3> Computational Resources Setup </h3>
            """,
            layout={"margin": "auto"}
        ) 

        self.guide = ipw.HTML(
            self.model.defaultGuide,
        )


    def render(self):
        if self.rendered:
            return 
        self.children = [
            self.header, 
            self.guide,
        ]
        self.rendered = True 
        return 

