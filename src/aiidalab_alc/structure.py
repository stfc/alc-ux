"""Defines the model and view components for the structure setup stage."""

import aiidalab_widgets_base as awb
import ipywidgets as ipw
import traitlets as tl
from aiida.orm import StructureData


class StructureStepModel(tl.HasTraits):
    """
    Model for structure selection and manipulation.

    A model to define and store required information from the structure
    step in the app's configuration wizard.
    """

    structure = tl.Instance(StructureData, allow_none=True)
    structure_file = tl.Unicode("", allow_none=True)

    @property
    def has_structure(self) -> bool:
        """True if a StructureData object has been attached to the model."""
        return self.structure is not None

    @property
    def has_file(self) -> bool:
        """True if a raw structure file object has been attached to the model."""
        return self.structure_file != ""

    @property
    def is_periodic(self) -> bool:
        """True if the attached StructureData object is a periodic structure."""
        if self.hasStructure:
            return any(self.structure.pbc)
        return False


class StructureWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    """
    Wizard for structure selection and manipulation.

    A step in a wizard based process widget which allows a user to
    configure a chemical structure to be used in their workflow.
    """

    def __init__(self, model: StructureStepModel, **kwargs):
        """
        StructureWizardStep constructor.

        Parameters
        ----------
        model : StructureStepModel
            A model controlling the data required for the structure step.
        **kwargs :
            Keyword arguments passed to the parent class's constructor.
        """
        super().__init__(children=[], **kwargs)
        self.rendered = False
        self.model = model

        self.info = ipw.HTML(
            """
                <p>
                    Load in a structure to start the workflow. The
                    structure can either be in AiiDA StructureData
                    format, or as a raw input file if the
                    file format is not directly supported by AiiDA
                    (e.g. ChemShell .pun files).
                </p>
            """
        )

        self.tabs = ipw.Tab()
        self.tabs.set_title(0, "AiiDA Structure")
        self.tabs.set_title(1, "Input File")

        self.structure_manager = awb.StructureManagerWidget(
            importers=[
                awb.StructureUploadWidget(title="From computer"),
                awb.StructureBrowserWidget(
                    title="AiiDA database", query_types=(StructureData,)
                ),
                awb.SmilesWidget(title="SMILES"),
                awb.StructureExamplesWidget(
                    title="From Examples",
                    examples=[],
                ),
            ],
            editors=[
                awb.BasicStructureEditor(title="Basic Editor"),
                awb.BasicCellEditor(title="Basic Cell Editor"),
            ],
            node_class="StructureData",
            storable=False,
        )
        ipw.dlink((self.structure_manager, "structure_node"), (self.model, "structure"))

        self.file_input_widget = ipw.VBox()
        self.file_input_btn = ipw.FileUpload(
            accept="",
            multiple=False,
            description="Upload Structure File",
        )
        self.file_handle = ipw.Text(
            value="",
            placeholder="",
            description="Structure File",
            disabled=True,
            layout={"width": "80%"},
        )
        self.file_input_widget.children = [
            self.file_handle,
            self.file_input_btn,
        ]

        self.tabs.children = [
            self.structure_manager,
            self.file_input_widget,
        ]

        return

    def render(self):
        """Render the wizard's contents if not already rendered."""
        if self.rendered:
            return

        submit_btn = ipw.Button(
            description="Submit Structure",
            disabled=False,
            button_style="success",
            tooltip="Submit the structure to the workflow",
            icon="check",
            layout={"margin": "auto", "width": "80%"},
        )
        submit_btn.on_click(self.submit_structure)

        self.children = [
            self.info,
            self.tabs,
            submit_btn,
        ]
        self.rendered = True
        return

    def submit_structure(self, _):
        """Store the current structure in the AiiDA database."""
        self.structureManager.store_structure()
        return
