"""Module defining the MVC for ChemShell workflow configuration."""

import aiidalab_widgets_base as awb
import ipywidgets as ipw
import traitlets as tl
from aiida.orm import SinglefileData

from aiidalab_alc.common.file_handling import FileUploadWidget


class ChemShellWorkflowModel(tl.HasTraits):
    """The model for setting up a ChemShell workflow."""

    qm_theory = tl.Unicode("NONE", allow_none=False)
    mm_theory = tl.Unicode("NONE", allow_none=True)
    qm_region = tl.List([], allow_none=True)
    basis_quality = tl.Bool(True, allow_none=False)
    force_field = tl.Instance(SinglefileData, allow_none=True)
    submitted = tl.Bool(False).tag(sync=True)
    use_mm = tl.Bool(False).tag(sync=True)

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
        ipw.dlink((self.options_widget.ff_file, "file"), (self.model, "force_field"))

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
        if self.model.use_mm:
            if not self.model.force_field:
                print("ERROR: No force field file found...")
                return
        self.submit_btn.description = "Submitted"
        self.submit_btn.disabled = True
        self.options_widget.disable(True)
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
        self.qm_basis_dropdown = ipw.Dropdown(
            options=["fast", "accurate"],
            description="Basis Quality:",
            disabled=False,
            layout={"width": "50%"},
        )
        self.qm_basis_dropdown.observe(self._update_basis_quality, "selected_index")
        self.qm_basis_dropdown.index = 1 if self.model.basis_quality else 0

        self.enable_mm_chk = ipw.Checkbox(
            value=False, description="Use QM/MM", indent=True
        )
        self.enable_mm_chk.observe(self._enable_mm_options, "value")
        ipw.dlink((self.enable_mm_chk, "value"), (self.model, "use_mm"))
        self.mm_theory_dropdown = ipw.Dropdown(
            options=self._get_mm_theory_options(),
            description="MM Theory:",
            disabled=True,
            layout={"width": "50%"},
        )
        self.qm_region_text = ipw.Text(
            value="",
            description="QM Region:",
            disabled=True,
            layout={"width": "50%"},
        )

        self.ff_file = FileUploadWidget(description="Force Field:")
        self.ff_file.disable(True)

        self.children = [
            self.qm_theory_dropdown,
            self.qm_basis_dropdown,
            self.enable_mm_chk,
            self.mm_theory_dropdown,
            self.qm_region_text,
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

    def _enable_mm_options(self, _) -> None:
        self.mm_theory_dropdown.disabled = not self.enable_mm_chk.value
        self.qm_region_text.disabled = not self.enable_mm_chk.value
        self.ff_file.disable(not self.enable_mm_chk.value)
        return

    def _update_basis_quality(self, _) -> None:
        if self.qm_basis_dropdown.selected_index == 0:
            self.model.basis_quality = False
        else:
            self.model.basis_quality = True
        return

    def render(self):
        """Render the options widget contents if not already rendered."""
        if self.rendered:
            return

        self.rendered = True
        return

    def disable(self, val: bool) -> None:
        """Disable the input fields."""
        for child in self.children:
            child.disabled = val
        self.ff_file.disable(val)
        return
