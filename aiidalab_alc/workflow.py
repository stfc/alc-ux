import ipywidgets as ipw 
import traitlets as tl 
import aiidalab_widgets_base as awb 

class ChemShellWorkflowModel(tl.HasTraits):

    theoryOptions = tl.List(["QM", "MM", "QM/MM"], allow_none=False)
    taskOptions = tl.List(["Single Point", "Geometry Optimisation"], allow_none=False)

    theory = tl.Unicode("QM", allow_none=False)
    task = tl.Unicode("Single Point", allow_none=False)

    defaultGuide = """
        <p>
            ChemShell is a powerful tool for interfacing with both Quantum Mechanical and Molecular 
            Mechanics codes to perform calculations. At its core you need to define a task and a theory 
            (either QM, MM or hybrid QM/MM based). 
        </p>
    """

class MethodWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    def __init__(self, model: ChemShellWorkflowModel, **kwargs):
        super().__init__(children=[], **kwargs)
        self.model = model
        self.rendered = False 

        self.header = ipw.HTML(
            """
            <h3> ChemShell Worflow Setup </h3>
            """,
            layout={"margin": "auto"}
        )
        self.guide = ipw.HTML(
            self.model.defaultGuide,
        )
        
        self.theoryOpt = ipw.ToggleButtons()
        ipw.dlink(
            (self.model, "theoryOptions"),
            (self.theoryOpt, "options"),
        )
        ipw.link(
            (self.model, "theory"),
            (self.theoryOpt, "value"),
        )

        self.taskOpt = ipw.ToggleButtons() 
        ipw.dlink(
            (self.model, "taskOptions"),
            (self.taskOpt, "options"),
        )
        ipw.link(
            (self.model, "task"),
            (self.taskOpt, "value"),
        )


        return     
    
    def render(self):
        if self.rendered:
            return 
        
        self.children = [
            self.header,
            self.guide,
            self.taskOpt, 
            self.theoryOpt,    
        ]
        self.rendered = True 
        return 
    

