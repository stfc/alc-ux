"""Module for handling AiiDA processes."""

import traitlets as tl
from aiida.engine import submit
from aiida.orm import Dict, load_code

from aiidalab_alc.resources import ComputationalResourcesModel
from aiidalab_alc.structure import StructureStepModel
from aiidalab_alc.workflow import ChemShellWorkflowModel


class MainAppModel(tl.HasTraits):
    """The main AiiDAlab application MVC model."""

    def __init__(self):
        """MainAppModel constructor."""
        super().__init__()
        self.structureModel = StructureStepModel()
        self.workflowModel = ChemShellWorkflowModel()
        self.resourceModel = ComputationalResourcesModel()

        self.resourceModel.observe(self._submit_model, "submitted")

        self.process = None
        return

    def _submit_model(self, _) -> None:
        """Handle the submission of the AiiDA process."""
        if ChemShellProcess.validate_model(self):
            self.process = ChemShellProcess(self)
            self.process.submit_process()
            print("Submit model called")
        else:
            print("ERROR: Input Validation Failed")
        return


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
        if not model.structureModel.has_structure:
            print("No structure provided.")
            return False
        if not model.workflowModel.force_field:
            print("No force field provided.")
            return False
        # Add more validation checks as needed
        return True

    def submit_process(self):
        """Submit the AiiDA process."""
        builder = load_code(self.model.resourceModel.code_label).get_builder()
        builder.structure = self.model.structureModel.structure
        builder.qm_parameters = Dict(
            {
                "theory": self.model.workflowModel.qm_theory,
                "basis": "cc-pvtz"
                if self.model.workflowModel.basis_quality
                else "cc-pvdz",
                "method": "dft",
                "functional": "B3LYP",
            }
        )
        builder.mm_parameters = Dict(
            {
                "theory": self.model.workflowModel.mm_theory,
            }
        )
        builder.force_field_file = self.model.workflowModel.force_field
        builder.qmmm_parameters = Dict(
            {
                "qm_region": self.model.workflowModel.qm_region,
                "embedding": "mechanical",
            }
        )
        self.node = submit(builder)
        return
