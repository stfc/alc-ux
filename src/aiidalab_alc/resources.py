"""Defines the model and view for the resource setup stage."""

import aiidalab_widgets_base as awb
import ipywidgets as ipw
import traitlets as tl


class ComputationalResourcesModel(tl.HasTraits):
    """Model for the resource setup stage."""

    default_guide = """
        <p>
            Configure the remote computational resources for the workflow.
        </p>
    """


class ComputationalResourcesWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    """Main view for the resource setup stage."""

    def __init__(self, **kwargs):
        """
        ComputationalResourcesWizardStep constructor.

        Parameters
        ----------
        **kwargs :
            Keyword arguments passed to the parent class's constructor.
        """
        super().__init__(children=[], **kwargs)
        self.model = ComputationalResourcesModel()
        self.rendered = False

        self.header = ipw.HTML(
            """
            <h3> Computational Resources Setup </h3>
            """,
            layout={"margin": "auto"},
        )

        self.guide = ipw.HTML(
            self.model.default_guide,
        )

    def render(self):
        """Render the wizard's contents if not already rendered."""
        if self.rendered:
            return
        self.children = [
            self.header,
            self.guide,
        ]
        self.rendered = True
        return
