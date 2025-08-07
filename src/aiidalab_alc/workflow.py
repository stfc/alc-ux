import ipywidgets as ipw 
import traitlets as tl 
import aiidalab_widgets_base as awb 
from aiida.orm import Dict 


# from .utils import getChemShellParams
# aiida_chemshell requires python>=3.10 but default docker images use python=3.9 


class ChemShellWorkflowModel(tl.HasTraits):

    theoryOptions = tl.List(["QM", "MM", "QM/MM"], allow_none=False)
    taskOptions = tl.List(["Single Point", "Geometry Optimisation"], allow_none=False)

    theory = tl.Unicode("QM", allow_none=False)
    task = tl.Unicode("Single Point", allow_none=False)
    
    taskParams = tl.Dict({}, allow_none=False)

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

        return     
    
    def render(self):
        if self.rendered:
            return 
        
        self.header = ipw.HTML(
            """
            <h3> ChemShell Workflow Setup </h3>
            """,
            layout={"margin": "auto"}
        )
        self.guide = ipw.HTML(
            self.model.defaultGuide,
        )
        
        self.taskOptionsW = ChemShellTaskWizardStep(self.model)
        self.theoryOptionsW = ChemShellTheoryWizardStep(self.model)
        self.steps = ipw.Accordion(
            children=[self.taskOptionsW, self.theoryOptionsW], selected_index=None
        )
        self.steps.set_title(0, "Step 2.1: Task Setup")
        self.steps.set_title(1, "Step 2.2: Theory Setup")
        
        submitBtn = ipw.Button(
            description="Submit Options",
            disbled=False,
            button_style="success",
            tooltip="Submit the workflow configuration",
            icon="check",
            layout={"margin": "auto", "width": "80%"}
        )
        submitBtn.on_click(self.submitOptions)

        self.children = [
            self.header,
            self.guide,
            self.steps,
            submitBtn
        ]
        self.rendered = True 
        return 
    
    def submitOptions(self, _):
        self.model.task = self.model.taskOptions[self.taskOptionsW.tabs.selected_index]
        return 
    

class ChemShellTaskWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    def __init__(self, model: ChemShellWorkflowModel, **kwargs):
        super().__init__(children=[], **kwargs)
        self.model = model 
        self.rendered = False 

        self.tabs = ipw.Tab()
        self.spTab = None 
        self.opTab = None 

        self.tabs.set_title(0, "Single Point")
        self.tabs.set_title(1, "Geometry Optimisation")

        self.spTab = ChemShellSinglePointTab()
        self.opTab = ChemShellOptimisationTab()
        self.tabs.children = [
            self.spTab, self.opTab
        ]
        self.tabs.selected_index = 0 
        self.children = [self.tabs]
        return 
    
    # def render(self):
    #     if self.rendered:
    #         return 
    #     self.rendered = True
        
    #     return  

        

class ChemShellSinglePointTab(ipw.VBox):
    def __init__(self, **kwargs):
        # opts = getChemShellParams("sp")
        opts = ("gradients", "hessian")
        self.widgets = {}
        for opt in opts:
            self.widgets[opt] = ipw.Checkbox(value=False, description=opt.capitalize(), disabled=False)
        super().__init__(children=list(self.widgets.values()), **kwargs)
        return 


class ChemShellOptimisationTab(ipw.VBox):
    def __init__(self, **kwargs):
        opts = ("maxcycle", "maxene", "coordinates", "algorithm", "trust_radius", "maxstep", "tolerance", "neb", "nimages", "nebk", "dimer", "delta", "tsrelative")
        self.widgets = {} 
        for opt in opts:
            self.widgets[opt] = ipw.Text(value="", description=opt.capitalize(), disabled=False)
        super().__init__(children=list(self.widgets.values()), **kwargs)
        return 
    
class ChemShellTheoryWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    def __init__(self, model, **kwargs):
        super().__init__(children=[], **kwargs)
        return 