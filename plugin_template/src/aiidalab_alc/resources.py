"""Defines the model and view for the resource setup stage."""

import aiidalab_widgets_base as awb
import ipywidgets as ipw
import traitlets as tl
from aiida.orm import Code, QueryBuilder

from aiidalab_alc.utils import test_aiida_chemsh_import


class ComputationalResourcesModel(tl.HasTraits):
    """Model for the resource setup stage."""

    code_label = tl.Unicode("").tag(sync=True)
    ncpus = tl.Int(1).tag(sync=True)
    process_label = tl.Unicode("").tag(sync=True)
    process_description = tl.Unicode("").tag(sync=True)
    submitted = tl.Bool(False).tag(sync=True)

    default_guide = """
        <p>
            Configure the computational resources required to run the ChemShell
            calculation. Additionally, you can provide a label and description for
            the AiiDA process that will be created.
        </p>
    """

    def validate(self) -> bool:
        """
        Validate the model's inputs.

        Returns
        -------
        bool
            True if all inputs are valid, False otherwise.
        """
        if not self.code_label:
            print("ERROR: No code selected.")
            return False
        return True


class ComputationalResourcesWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    """Main view for the resource setup stage."""

    def __init__(self, model: ComputationalResourcesModel, **kwargs):
        """
        ComputationalResourcesWizardStep constructor.

        Parameters
        ----------
        **kwargs :
            Keyword arguments passed to the parent class's constructor.
        """
        super().__init__(children=[], **kwargs)
        self.model = model
        self.rendered = False

        self.header = ipw.HTML(
            """
            <h3> Computational Resources Setup </h3>
            """,
            layout={"margin": "auto"},
        )
        self.chemsh_installed = test_aiida_chemsh_import()
        self.chemsh_warning = ipw.HTML("", layout={"margin": "auto"})

        self.guide = ipw.HTML(
            self.model.default_guide,
        )

        self.submit_btn = ipw.Button(
            description="Submit",
            button_style="success",
            tooltip="Submit the calculation",
            icon="check",
            layout={"width": "80%", "margin": "auto"},
        )
        self.submit_btn.on_click(self._submit)

        self.children = [
            # self.header,
            self.guide,
            self.chemsh_warning if not self.chemsh_installed else ipw.HTML(""),
            ResourceSetupBox(model=self.model),
            self.submit_btn,
        ]
        return

    def render(self):
        """Render the wizard's contents if not already rendered."""
        if self.rendered:
            return
        self._refresh_widget()
        self.rendered = True
        return

    def _submit(self, _=None) -> None:
        """Handle the submission of the AiiDA process."""
        if self.model.validate():
            self.model.submitted = True
            self.submit_btn.disabled = True
            self.submit_btn.description = "Submitted"
        else:
            print("ERROR: Input Validation Failed")
        return

    def _refresh_widget(self) -> None:
        """Refresh the widget's contents."""
        self.chemsh_installed = test_aiida_chemsh_import()
        if not self.chemsh_installed:
            self.submit_btn.disabled = True
            self.chemsh_warning.value = (
                "<p style='color:red;'>"
                "The aiida-chemshell plugin is not installed. Please install it "
                "to proceed."
                "</p>"
            )
        else:
            self.chemsh_warning.value = ""
            self.submit_btn.disabled = False


class ResourceSetupBox(ipw.VBox):
    """A box widget for defining computational resources."""

    def __init__(self, model: ComputationalResourcesModel, **kwargs):
        """
        ResourceSetupBox constructor.

        Parameters
        ----------
        **kwargs :
            Keyword arguments passed to the parent class's constructor.
        """
        super().__init__(layout={"margin": "auto", "width": "80%"}, **kwargs)
        self.model = model

        self.code = ipw.Combobox(
            description="Code:",
            layout={"width": "60%"},
        )
        tl.link((self.code, "value"), (self.model, "code_label"))
        self.refresh_codes_button = ipw.Button(
            description="Refresh",
            button_style="info",
            tooltip="Refresh the list of available codes",
            icon="refresh",
            layout={"width": "20%"},
        )
        self.refresh_codes_button.on_click(self.update_codes)
        self.code_box = ipw.HBox(
            layout={"width": "100%"}, children=[self.code, self.refresh_codes_button]
        )
        self.update_codes()

        # tl.link((self.code, "value"), (self.model, "code"))

        self.ncpus_input = ipw.BoundedIntText(
            value=self.model.ncpus,
            min=1,
            max=128,
            step=1,
            description="No. CPUs:",
            disabled=False,
            layout=ipw.Layout(width="80%"),
        )
        tl.link((self.ncpus_input, "value"), (self.model, "ncpus"))

        self.label = ipw.Text(
            value=self.model.process_label,
            placeholder="Enter process label",
            description="Label:",
            disabled=False,
            layout=ipw.Layout(width="80%"),
        )
        tl.link((self.label, "value"), (self.model, "process_label"))

        self.description = ipw.Textarea(
            value=self.model.process_description,
            placeholder="Enter process description",
            description="Description:",
            disabled=False,
            layout=ipw.Layout(width="80%"),
        )
        tl.link((self.description, "value"), (self.model, "process_description"))

        self.children = [
            self.code_box,
            self.ncpus_input,
            self.label,
            self.description,
        ]

    def update_codes(self, _=None) -> None:
        """Update the list of available codes."""
        qb = QueryBuilder()
        qb.append(Code, project=["label", "id"])
        codes = qb.all()
        code_labels = [f"{label}" for label, id in codes]
        self.code.options = code_labels
        if code_labels:
            self.code.value = code_labels[0]
        return
