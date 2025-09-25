"""Module defining the MVC for ChemShell workflow configuration."""

import aiidalab_widgets_base as awb
import ipywidgets as ipw
import traitlets as tl
from aiida.orm import SinglefileData

from aiidalab_alc.file_handling import FileUploadWidget


class ChemShellWorkflowModel(tl.HasTraits):
    """The model for setting up a ChemShell workflow."""

    qm_theory = tl.Unicode("PySCF", allow_none=False)
    mm_theory = tl.Unicode("GULP", allow_none=False)
    qm_region = tl.List([], allow_none=False)
    basis_quality = tl.Bool(True, allow_none=False)
    force_field = tl.Instance(SinglefileData, allow_none=False)
    submitted = tl.Bool(False).tag(sync=True)

    default_guide = ""


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
            <h3> ChemShell QM/MM Geometry Optimisation </h3>
            """,
            layout={"margin": "auto"},
        )
        self.guide = ipw.HTML(
            self.model.default_guide,
        )

        self.options_widget = ChemShellOptionsWidget(self.model)

        self.submit_btn = ipw.Button(
            description="Submit Options",
            disbled=False,
            button_style="success",
            tooltip="Submit the workflow configuration",
            icon="check",
            layout={"margin": "auto", "width": "60%"},
        )
        self.submit_btn.on_click(self._submit)

        self.children = [self.header, self.guide, self.options_widget, self.submit_btn]
        self.rendered = True
        return

    def _submit(self, _):
        """Store the ChemShell parameters in the ChemShell workflow model."""
        self.model.qm_theory = self.options_widget.qm_theory_dropdown.value
        self.model.mm_theory = self.options_widget.mm_theory_dropdown.value
        try:
            self.model.qm_region = [
                int(x) for x in self.options_widget.qm_region_text.value.split(",")
            ]
        except ValueError:
            self.model.qm_region.clear()
            self.options_widget.qm_region_text.value = ""
        except Exception as e:
            raise e

        if self.options_widget.ff_file.file is not None:
            self.model.force_field = self.options_widget.ff_file.get_aiida_file_object()
            self.submit_btn.description = "Submitted"
            self.submit_btn.disabled = True
        return


class ChemShellOptionsWidget(ipw.VBox):
    """Widget for selecting the ChemShell input options."""

    def __init__(self, model: ChemShellWorkflowModel, **kwargs):
        """
        ChemShellOptionsWidget constructor.

        Parameters
        ----------
        model : ChemShellWorkflowModel
            The model that defines the data related to this step in the setup wizard.
        **kwargs :
            Keyword arguments passed to the parent class's constructor.
        """
        super().__init__(**kwargs)
        self.model = model
        self.rendered = False

        self.qm_theory_dropdown = ipw.Dropdown(
            options=self._get_qm_theory_options(),
            description="QM Theory:",
            disabled=False,
            layout={"width": "50%"},
        )

        self.mm_theory_dropdown = ipw.Dropdown(
            options=self._get_mm_theory_options(),
            description="MM Theory:",
            disabled=False,
            layout={"width": "50%"},
        )
        self.qm_region_text = ipw.Text(
            value="",
            description="QM Region:",
            disabled=False,
            layout={"width": "50%"},
        )
        self.basis_quality = ipw.Checkbox(
            value=True,
            description="Use high quality basis set (slower):",
            disbled=False,
            layout={"width": "50%"},
        )
        tl.link((self.basis_quality, "value"), (self.model, "basis_quality"))

        self.ff_file = FileUploadWidget(description="Force Field:")

        self.children = [
            self.qm_theory_dropdown,
            self.mm_theory_dropdown,
            self.qm_region_text,
            self.basis_quality,
            self.ff_file,
        ]

        # self.layout = Layout(margin="auto")

        return

    def _get_qm_theory_options(self) -> list[str]:
        """Get the available QM theory options."""
        try:
            from aiida_chemshell.utils import ChemShellQMTheory

            return list(ChemShellQMTheory.__members__.keys())
        except ImportError:
            return []
        except Exception as e:
            raise e

    def _get_mm_theory_options(self) -> list[str]:
        """Get the available MM theory options."""
        try:
            from aiida_chemshell.utils import ChemShellMMTheory

            return list(ChemShellMMTheory.__members__.keys())
        except ImportError:
            return []
        except Exception as e:
            raise e

    def render(self):
        """Render the options widget contents if not already rendered."""
        if self.rendered:
            return

        self.rendered = True
        return
