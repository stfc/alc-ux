"""Module for defining widgets/models for viewing process progress and results."""

from typing import cast

import aiidalab_widgets_base as awb
import ipywidgets as ipw
import traitlets as tl
from aiida.common.exceptions import NotExistent
from aiida.orm import NodeLinksManager, ProcessNode, load_node


class ProcessModel(tl.HasTraits):
    """Model describing an AiiDA process."""

    process_uuid = tl.Unicode(None, allow_none=True)

    @property
    def process(self) -> ProcessNode | None:
        """Return the process node for the stored uuid."""
        if not self.process_uuid:
            return None
        try:
            return cast(ProcessNode, load_node(self.process_uuid))
        except NotExistent:
            return None

    @property
    def has_process(self) -> bool:
        """Return true if a valid process node is associated with the uuid."""
        return self.process is not None

    @property
    def inputs(self) -> NodeLinksManager | list:
        """Return the inputs for the process."""
        return self.process.inputs if self.has_process else []

    @property
    def outputs(self) -> NodeLinksManager | list:
        """Return the outputs for teh process."""
        return self.process.outputs if self.has_process else []


class ResultsModel(ProcessModel):
    """MVC results step model."""

    blocked = tl.Bool(True)


class ResultsWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    """Wizard for viewing process progress and results."""

    def __init__(self, model: ResultsModel, **kwargs):
        """
        ResultsWizardStep constructor.

        Parameters
        ----------
        model : ResultsModel
            The model controlling required data.
        **kwargs :
            Keyword arguments passed to the parent class's constructor.
        """
        self.rendered = False
        self.model = model

        self.info = ipw.HTML(
            """
            <p>
                View the progress and results of the generated ChemShell
                calculation process.
            </p>
            """
        )

        self.update_btn = ipw.Button(
            description="Refresh",
            icon="arrows-rotate",
            disabled=False,
            button_style="info",
            tooltip="Refresh process information.",
            layout={"margin": "auto", "width": "70%"},
        )
        self.update_btn.on_click(self._refresh_info)

        super().__init__(**kwargs)
        return

    def render(self) -> None:
        """Render the wizard's uninitialised content."""
        if self.rendered:
            return
        if self.model.blocked:
            msg = ipw.HTML(
                """
                <p>
                    No process has been configured...
                </p>
                """
            )
            self.children = [msg]
        else:
            self.node_tree = awb.ProcessNodesTreeWidget()
            ipw.dlink((self.model, "process_uuid"), (self.node_tree, "value"))
            self.node_view = awb.viewers.AiidaNodeViewWidget()
            ipw.dlink(
                (self.node_tree, "selected_nodes"),
                (self.node_view, "node"),
                transform=lambda nodes: nodes[0] if nodes else None,
            )

            self.children = [
                self.info,
                self.node_tree,
                self.node_view,
                self.update_btn,
            ]
            self.rendered = True
        return

    def _refresh_info(self, _) -> None:
        """Refresh the process information."""
        self.node_tree.update()
        return
