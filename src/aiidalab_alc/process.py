"""Module for handling AiiDA processes."""

import traitlets as tl

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
        self.process = None
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
