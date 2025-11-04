"""Module for handling AiiDA processes."""

import traitlets as tl
from aiida.engine import submit
from aiida.orm import Dict, load_code
from ipywidgets import dlink

from aiidalab_alc.resources import ComputationalResourcesModel
from aiidalab_alc.results import ResultsModel
from aiidalab_alc.structure import StructureStepModel
from aiidalab_alc.workflow import ChemShellWorkflowModel


class MainAppModel(tl.HasTraits):
    """The main AiiDAlab application MVC model."""

    block_results = tl.Bool(True, allow_none=False)

    def __init__(self):
        """MainAppModel constructor."""
        super().__init__()
        self.structure_model = StructureStepModel()
        self.workflow_model = ChemShellWorkflowModel()
        self.resource_model = ComputationalResourcesModel()
        self.results_model = ResultsModel()

        self.resource_model.observe(self._submit_model, "submitted")
        dlink((self, "block_results"), (self.results_model, "blocked"))

        self.process = None

        return

    def _submit_model(self, _) -> None:
        """Handle the submission of the AiiDA process."""
        if ChemShellProcess.validate_model(self):
            self.process = ChemShellProcess(self)
            self.process.submit_process()
            self.block_results = False
            self.results_model.process_uuid = self.process.node.uuid
        else:
            print("ERROR: Input Validation Failed")
        return

    def reset(self) -> None:
        """Reset the state of the model."""
        self.submitted = False


class ChemShellProcess:
    """Class to handle a ChemShell AiiDA process."""

    def __init__(self, model: MainAppModel):
        """
        ChemShellProcess constructor.

        Parameters
        ----------
        model : MainAppModel
            The main application model containing all necessary data.
        """
        self.model = model
        self.node = None
        return

    @classmethod
    def validate_model(cls, model: MainAppModel) -> bool:
        """
        Validate the main application model.

        Parameters
        ----------
        model : MainAppModel
            The main application model to validate.

        Returns
        -------
        bool
            True if the model is valid, False otherwise.
        """
        if not model.structure_model.has_structure:
            if not model.structure_model.has_file:
                print("No structure provided.")
                return False
        if model.workflow_model.use_mm:
            if not model.workflow_model.force_field:
                print("No force field provided.")
                return False
            if not model.workflow_model.qm_region:
                print("No qm_ region specified")
                return False
        # Add more validation checks as needed
        return True

    def submit_process(self):
        """Submit the AiiDA process."""
        builder = load_code(self.model.resource_model.code_label).get_builder()
        if self.model.structure_model.has_file:
            builder.structure = self.model.structure_model.structure_file
        else:
            builder.structure = self.model.structure_model.structure
        builder.qm_parameters = Dict(
            {
                "theory": self.model.workflow_model.qm_theory,
                "basis": "cc-pvtz"
                if self.model.workflow_model.basis_quality
                else "cc-pvdz",
                "method": "dft",
                "functional": "B3LYP",
            }
        )
        if self.model.workflow_model.use_mm:
            builder.mm_parameters = Dict(
                {
                    "theory": self.model.workflow_model.mm_theory,
                }
            )
            builder.force_field_file = self.model.workflow_model.force_field
            builder.qmmm_parameters = Dict(
                {
                    "qm_region": self.model.workflow_model.qm_region,
                }
            )
        builder.calculation_parameters = Dict({"gradients": True})
        builder.optimisation_parameters = Dict({})
        self.node = submit(builder)
        return
