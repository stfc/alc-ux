import ipywidgets as ipw 
import aiidalab_widgets_base as awb
from IPython.display import display, Image
from datetime import datetime 
from functools import partial


from .resources import ComputationalResourcesWizardStep
from .structure import StructureWizardStep, StructureStepModel
from .workflow import MethodWizardStep, ChemShellWorkflowModel
from .utils import getAppDir, openLinkInNewTab


class MainApp:
    def __init__(self, process=None):
        self.process = process 
        self.view = MainAppView()
        display(self.view)

    def load(self) -> None:
        return 

class MainAppView(ipw.VBox):
    def __init__(self):

        logoImg = Image(
            filename = getAppDir() / "images/alc-100.png",
            width = 300,
        )
        logo = ipw.Output(layout={"margin": "auto"})
        with logo:
            display(logoImg)
        logo.add_class("logo")

        subtitle = ipw.HTML(
            """
            <h2 id='subtitle'>Welcome to the Ada Lovelace Center AiiDAlab App</h2>
            """
        )

        quickAccess = QuickAccessButtons()

        header = ipw.VBox(
            children=[
                logo, subtitle,
            ],
            layout={"margin": "auto"},
        )

        footer = ipw.HTML(f"""
            <footer>
                Copyright (c) {datetime.now().year} Ada Lovelace Centre (STFC) <br>       
            </footer>
    
            """,
            layout={"align-content": "right"})

        self.main = WizardWidget()

        super().__init__(
            layout={},
            children=[
                header,
                quickAccess,
                self.main,
                footer
            ],
        )

class WizardWidget(ipw.VBox):
    def __init__(self, **kwargs):

        # Create the models to hold the state of each step 
        self.structureModel = StructureStepModel() 
        self.workflowModel = ChemShellWorkflowModel() 

        self.structureStep = StructureWizardStep(self.structureModel)
        self.workflowStep = MethodWizardStep(self.workflowModel)
        self.compResourceStep = ComputationalResourcesWizardStep()

        self._wizard_app_widget = awb.WizardAppWidget(
            steps=[
                ("Select Structure", self.structureStep),
                ("Select Workflow", self.workflowStep),
                ("Configure Resources", self.compResourceStep),
            ]
        )

        self._wizard_app_widget.observe(
            self.onStepChange, "selected_index",
        )

        # Hide the header 
        self._wizard_app_widget.children[0].layout.display = "none"

        super().__init__(
            children=[self._wizard_app_widget], 
            **kwargs,
        )
        
        self._wizard_app_widget.selected_index = None 

        return 
    
    @property
    def steps(self):
        return self._wizard_app_widget.steps
    
    def onStepChange(self, change):
        if (step_index := change["new"]) is not None:
            step = self.steps[step_index][1]
            step.render()
        return 

    
class QuickAccessButtons(ipw.HBox):
    def __init__(self, **kwargs):
        self.newCalcLink = ipw.Button(
            description="New Calculation", 
            disabled=False, 
            button_style="success", 
            tooltip="Start a new calculation", 
            icon="plus",
        )
        self.newCalcLink.on_click(partial(openLinkInNewTab, "main.ipynb"))

        self.historyLink = ipw.Button(
            description="History",
            disabled=False,
            button_style="primary",
            tooltip="View Calculation History",
            icon="history",
        )
        self.historyLink.on_click(partial(openLinkInNewTab, "history.ipynb"))

        self.setupResourcesLink = ipw.Button(
            description="Setup Resources", 
            disabled=False, 
            button_style="primary",
            tooltip="Configure Computational Resources",
            icon="cogs",
            # on_click=partial(onLinkClick, getAppDir() / "../home/code_setup.ipynb"),
        )
        self.setupResourcesLink.on_click(partial(openLinkInNewTab, "../home/code_setup.ipynb"))

        self.docsLink = ipw.Button(
            description="Documentation", 
            disabled=False, 
            button_style="info", 
            tooltip="Open Documentation", 
            icon="book",
        )
        self.docsLink.on_click(partial(openLinkInNewTab, "https://github.com/stfc/alc-ux"))

        children=[
            self.newCalcLink,
            self.historyLink,
            self.setupResourcesLink,
            self.docsLink,
        ]
        super().__init__(children=children, layout={'margin': 'auto'}, **kwargs)
        return 