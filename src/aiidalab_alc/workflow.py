"""Defines the model and view components for the workflow setup stage."""

import aiidalab_widgets_base as awb
import ipywidgets as ipw
import traitlets as tl

# from .utils import getChemShellParams
# aiida_chemshell requires python>=3.10 but default docker images use python=3.9


class ChemShellWorkflowModel(tl.HasTraits):
    """The model for setting up a ChemShell workflow."""

    theory_options = tl.List(["QM", "MM", "QM/MM"], allow_none=False)
    task_options = tl.List(["Single Point", "Geometry Optimisation"], allow_none=False)

    theory = tl.Unicode("QM", allow_none=False)
    task = tl.Unicode("Single Point", allow_none=False)

    task_params = tl.Dict({}, allow_none=False)

    default_guide = """
        <p>
            ChemShell is a powerful tool for interfacing with both
            Quantum Mechanical and Molecular Mechanics codes to perform
            calculations. At its core you need to define a task and a
            theory (either QM, MM or hybrid QM/MM based).
        </p>
    """


class MethodWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    """Wizard setup for the calculation workflow."""

    def __init__(self, model: ChemShellWorkflowModel, **kwargs):
        """
        MethodWizardStep constructor.

        Parameters
        ----------
        model : ChemShellWorkflowModel
            The model that defines the data related to this step in the setup wizard.
        **kwargs :
            Keyword arguments passed to the parent class's constructor.
        """
        super().__init__(children=[], **kwargs)
        self.model = model
        self.rendered = False

        return

    def render(self):
        """Render the wizard contents if not already rendered."""
        if self.rendered:
            return

        self.header = ipw.HTML(
            """
            <h3> ChemShell Workflow Setup </h3>
            """,
            layout={"margin": "auto"},
        )
        self.guide = ipw.HTML(
            self.model.default_guide,
        )

        self.task_wizard = ChemShellTaskWizardStep(self.model)
        self.theory_wizard = ChemShellTheoryWizardStep(self.model)
        self.steps = ipw.Accordion(
            children=[self.task_wizard, self.theory_wizard], selected_index=None
        )
        self.steps.set_title(0, "Step 2.1: Task Setup")
        self.steps.set_title(1, "Step 2.2: Theory Setup")

        submit_btn = ipw.Button(
            description="Submit Options",
            disbled=False,
            button_style="success",
            tooltip="Submit the workflow configuration",
            icon="check",
            layout={"margin": "auto", "width": "80%"},
        )
        submit_btn.on_click(self.submit_options)

        self.children = [self.header, self.guide, self.steps, submit_btn]
        self.rendered = True
        return

    def submit_options(self, _):
        """Store the ChemShell parameters in the ChemShell workflow model."""
        self.model.task = self.model.task_options[self.task_wizard.tabs.selected_index]
        return


class ChemShellTaskWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    """Wizard view to setup a ChemShell workflow."""

    def __init__(self, model: ChemShellWorkflowModel, **kwargs):
        """
        ChemShellTaskWizardStep constructor.

        Parameters
        ----------
        model : ChemShellWorkflowModel
            The model that defines the data related to this step in the setup wizard.
        **kwargs :
            Keyword arguments passed to the parent class's constructor.
        """
        super().__init__(children=[], **kwargs)
        self.model = model
        self.rendered = False

        self.tabs = ipw.Tab()
        self.sp_tab = None
        self.op_tab = None

        self.tabs.set_title(0, "Single Point")
        self.tabs.set_title(1, "Geometry Optimisation")

        self.sp_tab = ChemShellSinglePointTab()
        self.op_tab = ChemShellOptimisationTab()
        self.tabs.children = [self.sp_tab, self.op_tab]
        self.tabs.selected_index = 0
        self.children = [self.tabs]
        return


class ChemShellSinglePointTab(ipw.VBox):
    """Widget to assign ChemShell's single point task's parameters."""

    def __init__(self, **kwargs):
        """
        ChemShellSinglePointTab constructor.

        Parameters
        ----------
        **kwargs :
            Keyword arguments passed to the parent class's constructor.
        """
        # opts = getChemShellParams("sp")
        opts = ("gradients", "hessian")
        self.widgets = {}
        for opt in opts:
            self.widgets[opt] = ipw.Checkbox(
                value=False, description=opt.capitalize(), disabled=False
            )
        super().__init__(children=list(self.widgets.values()), **kwargs)
        return


class ChemShellOptimisationTab(ipw.VBox):
    """Widget to assign ChemShell's optimisation task's parameters."""

    def __init__(self, **kwargs):
        """
        ChemShellOptimisationTab constructor.

        Parameters
        ----------
        **kwargs :
            Keyword arguments passed to the parent class's constructor.
        """
        opts = (
            "maxcycle",
            "maxene",
            "coordinates",
            "algorithm",
            "trust_radius",
            "maxstep",
            "tolerance",
            "neb",
            "nimages",
            "nebk",
            "dimer",
            "delta",
            "tsrelative",
        )
        self.widgets = {}
        for opt in opts:
            self.widgets[opt] = ipw.Text(
                value="", description=opt.capitalize(), disabled=False
            )
        super().__init__(children=list(self.widgets.values()), **kwargs)
        return


class ChemShellTheoryWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    """Wizard step to control the theory parameters for a ChemShell workflow."""

    def __init__(self, model, **kwargs):
        """
        ChemShellTheoryWizardStep constructor.

        Parameters
        ----------
        model : ChemShellWorkflowModel
            The model that defines the data related to this step in the setup wizard.
        **kwargs :
            Keyword arguments passed to the parent class's constructor.
        """
        super().__init__(children=[], **kwargs)
        return
