"""Defines the main AiiDAlab application page."""

from datetime import datetime

import aiidalab_widgets_base as awb
import ipywidgets as ipw
from IPython.display import Image, display

from aiidalab_alc.navigation import QuickAccessButtons
from aiidalab_alc.process import MainAppModel
from aiidalab_alc.resources import (
    ComputationalResourcesWizardStep,
)
from aiidalab_alc.structure import StructureWizardStep
from aiidalab_alc.utils import get_app_dir
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
        logo_img = Image(
            filename=get_app_dir() / "images/alc-100.png",
            width=300,
        )
        logo = ipw.Output(layout={"margin": "auto"})
        with logo:
            display(logo_img)
        logo.add_class("logo")

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
        self.structureStep = StructureWizardStep(model.structureModel)
        self.workflowStep = MethodWizardStep(model.workflowModel)
        self.compResourceStep = ComputationalResourcesWizardStep(model.resourceModel)

        self._wizard_app_widget = awb.WizardAppWidget(
            steps=[
                ("Select Structure", self.structureStep),
                ("Configure Workflow", self.workflowStep),
                ("Configure Computational Resources", self.compResourceStep),
            ]
        )

        self._wizard_app_widget.observe(
            self.on_step_change,
            "selected_index",
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
        """Alias to the wizard's steps list."""
        return self._wizard_app_widget.steps

    def on_step_change(self, change):
        """Switch between wizard steps when selected by the user."""
        if (step_index := change["new"]) is not None:
            step = self.steps[step_index][1]
            step.render()
        return
