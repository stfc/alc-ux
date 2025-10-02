"""Defines the main AiiDAlab application page."""

from datetime import datetime

import aiidalab_widgets_base as awb
import ipywidgets as ipw
from IPython.display import display

from aiidalab_alc.navigation import QuickAccessButtons
from aiidalab_alc.process import MainAppModel
from aiidalab_alc.resources import (
    ComputationalResourcesWizardStep,
)
from aiidalab_alc.results import ResultsWizardStep
from aiidalab_alc.structure import StructureWizardStep
from aiidalab_alc.workflow import MethodWizardStep


class MainApp:
    """The main AiiDAlab application class."""

    def __init__(self):
        """MainApp constructor."""
        self.model = MainAppModel()
        self.view = MainAppView(self.model)
        display(self.view)

    # def load(self) -> None:
    #     return


class MainAppView(ipw.VBox):
    """The main app view."""

    def __init__(self, model: MainAppModel, **kwargs):
        """MainAppView constructor."""
        logo = ipw.HTML(
            """
            <div class="app-container logo" style="width: 300px;">
                <img src="./images/alc.svg" alt="ALC AiiDAlab App Logo" />
            </div>
            """,
            layout={"margin": "auto"},
        )

        subtitle = ipw.HTML(
            """
            <h2 id='subtitle'>Welcome to the Ada Lovelace Center AiiDAlab App</h2>
            """
        )

        nav_btns = QuickAccessButtons()

        header = ipw.VBox(
            children=[
                logo,
                subtitle,
            ],
            layout={"margin": "auto"},
        )

        footer = ipw.HTML(
            f"""
            <footer>
                Copyright (c) {datetime.now().year} Ada Lovelace Centre
                (STFC) <br>
            </footer>
            """,
            layout={"align-content": "right"},
        )

        self.main = WizardWidget(model)

        super().__init__(
            layout={}, children=[header, nav_btns, self.main, footer], **kwargs
        )


class WizardWidget(ipw.VBox):
    """An ipywidgets based widget to hold the main application construct wizard."""

    def __init__(self, model: MainAppModel, **kwargs):
        """
        WizardWidget constructor.

        Parameters
        ----------
        **kwargs :
            Keyword arguments passed to the `ipywidgets.VBox.__init__()`.
        """
        self.structureStep = StructureWizardStep(model.structure_model)
        self.workflowStep = MethodWizardStep(model.workflow_model)
        self.compResourceStep = ComputationalResourcesWizardStep(model.resource_model)
        self.results_step = ResultsWizardStep(model.results_model)

        self._wizard_app_widget = awb.WizardAppWidget(
            steps=[
                ("Select Structure", self.structureStep),
                ("Configure Workflow", self.workflowStep),
                ("Configure Computational Resources", self.compResourceStep),
                ("Results", self.results_step),
            ]
        )

        self._wizard_app_widget.observe(
            self.on_step_change,
            "selected_index",
        )

        self.results_step.disabled = True
        self._model = model
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
        """Alias to the wizard's steps list."""
        return self._wizard_app_widget.steps

    def on_step_change(self, change):
        """Switch between wizard steps when selected by the user."""
        if (step_index := change["new"]) is not None:
            step = self.steps[step_index][1]
            step.render()
        return
