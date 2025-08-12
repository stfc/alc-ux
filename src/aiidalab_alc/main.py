"""Defines the main AiiDAlab application page."""

from datetime import datetime
from functools import partial

import aiidalab_widgets_base as awb
import ipywidgets as ipw
from IPython.display import Image, display

from aiidalab_alc.resources import ComputationalResourcesWizardStep
from aiidalab_alc.structure import StructureStepModel, StructureWizardStep
from aiidalab_alc.utils import get_app_dir, open_link_in_new_tab
from aiidalab_alc.workflow import ChemShellWorkflowModel, MethodWizardStep


class MainApp:
    """The main AiiDAlab application class."""

    def __init__(self):
        """MainApp constructor."""
        self.view = MainAppView()
        display(self.view)

    # def load(self) -> None:
    #     return


class MainAppView(ipw.VBox):
    """The main app view."""

    def __init__(self):
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

        self.main = WizardWidget()

        super().__init__(
            layout={},
            children=[header, nav_btns, self.main, footer],
        )


class WizardWidget(ipw.VBox):
    """An ipywidgets based widget to hold the main application construct wizard."""

    def __init__(self, **kwargs):
        """
        WizardWidget constructor.

        Parameters
        ----------
        **kwargs :
            Keyword arguments passed to the `ipywidgets.VBox.__init__()`.
        """
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


class QuickAccessButtons(ipw.HBox):
    """Quick access buttons present in the apps header and start banner."""

    def __init__(self, **kwargs):
        """
        QuickAccessButtons constructor.

        Parameters
        ----------
        **kwargs :
            Keyword arguments passed to the `ipywidgets.HBox.__init__()`.
        """
        self.new_calc_link = ipw.Button(
            description="New Calculation",
            disabled=False,
            button_style="success",
            tooltip="Start a new calculation",
            icon="plus",
        )
        self.new_calc_link.on_click(
            partial(open_link_in_new_tab, "../alc-ux/main.ipynb")
        )

        self.history_link = ipw.Button(
            description="History",
            disabled=False,
            button_style="primary",
            tooltip="View Calculation History",
            icon="history",
        )
        self.history_link.on_click(
            partial(open_link_in_new_tab, "../alc-ux/history.ipynb")
        )

        self.resource_setup_link = ipw.Button(
            description="Setup Resources",
            disabled=False,
            button_style="primary",
            tooltip="Configure Computational Resources",
            icon="cogs",
            # on_click=partial(onLinkClickt get_app_dir() / "../home/code_setup.ipynb"),
        )
        self.resource_setup_link.on_click(
            partial(open_link_in_new_tab, "../home/code_setup.ipynb")
        )

        self.docs_link = ipw.Button(
            description="Documentation",
            disabled=False,
            button_style="info",
            tooltip="Open Documentation",
            icon="book",
        )
        self.docs_link.on_click(
            partial(open_link_in_new_tab, "https://github.com/stfc/alc-ux")
        )

        children = [
            self.new_calc_link,
            self.history_link,
            self.resource_setup_link,
            self.docs_link,
        ]
        super().__init__(children=children, layout={"margin": "auto"}, **kwargs)
        return
