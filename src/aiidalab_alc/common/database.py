"""Module for components relating to AiiDA database management."""

import datetime

import ipywidgets as ipw
import traitlets as tl
from aiida.orm import (
    CalcFunctionNode,
    CalcJobNode,
    Data,
    Node,
    QueryBuilder,
    WorkChainNode,
)


class AiiDADatabaseWidget(ipw.VBox, tl.HasTraits):
    """Widget for AiiDA database querying."""

    data_object = tl.Instance(Data, allow_none=True)

    def __init__(self, title: str = "", query: list = None):
        if query is None:
            query = []
        self.title = title
        self.query_type = tuple(query)

        qbuilder = QueryBuilder().append((CalcJobNode, WorkChainNode), project="label")

        self.drop_down = ipw.Dropdown(
            options=sorted({"All"}.union({i[0] for i in qbuilder.iterall() if i[0]})),
            value="All",
            description="Process Label",
            disabled=True,
            style={"description_width": "120px"},
            layout={"width": "50%"},
        )
        self.drop_down.observe(self.search, names="value")

        # Disable process labels selection if we are not looking for the calculated
        # structures.
        def disable_drop_down(change):
            self.drop_down.disabled = not change["new"] == "calculated"

        # Select structures kind.
        self.mode = ipw.RadioButtons(
            options=["all", "uploaded", "calculated"], layout={"width": "25%"}
        )
        self.mode.observe(self.search, names="value")
        self.mode.observe(disable_drop_down, names="value")

        # Date range.
        # Note: there is Date picker widget, but it currently does not work in Safari:
        # https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#Date-picker
        date_text = ipw.HTML(value="<p>Select the date range:</p>")
        self.start_date_widget = ipw.Text(
            value="", description="From: ", style={"description_width": "120px"}
        )
        self.end_date_widget = ipw.Text(value="", description="To: ")

        # Search button.
        btn_search = ipw.Button(
            description="Search",
            button_style="info",
            layout={"width": "initial", "margin": "2px 0 0 2em"},
        )
        btn_search.on_click(self.search)

        age_selection = ipw.VBox(
            [
                date_text,
                ipw.HBox([self.start_date_widget, self.end_date_widget, btn_search]),
            ],
            layout={"border": "1px solid #fafafa", "padding": "1em"},
        )

        h_line = ipw.HTML("<hr>")
        box = ipw.VBox([age_selection, h_line, ipw.HBox([self.mode, self.drop_down])])

        self.results = ipw.Dropdown(layout={"width": "900px"})
        self.results.observe(self._on_select_structure, names="value")
        self.search()
        super().__init__([box, h_line, self.results])

    def search(self, _=None) -> None:
        """Search structures in the AiiDA database."""
        qbuild = QueryBuilder()

        # If the date range is valid, use it for the search
        try:
            start_date = datetime.datetime.strptime(
                self.start_date_widget.value, "%Y-%m-%d"
            )
            end_date = datetime.datetime.strptime(
                self.end_date_widget.value, "%Y-%m-%d"
            ) + datetime.timedelta(hours=24)

        # Otherwise revert to the standard (i.e. last 7 days)
        except ValueError:
            start_date = datetime.datetime.now() - datetime.timedelta(days=7)
            end_date = datetime.datetime.now() + datetime.timedelta(hours=24)

            self.start_date_widget.value = start_date.strftime("%Y-%m-%d")
            self.end_date_widget.value = end_date.strftime("%Y-%m-%d")

        filters = {}
        filters["ctime"] = {"and": [{">": start_date}, {"<=": end_date}]}

        if self.mode.value == "uploaded":
            qbuild2 = (
                QueryBuilder()
                .append(self.query_type, project=["id"], tag="structures")
                .append(Node, with_outgoing="structures")
            )
            processed_nodes = [n[0] for n in qbuild2.all()]
            if processed_nodes:
                filters["id"] = {"!in": processed_nodes}
            qbuild.append(self.query_type, filters=filters)

        elif self.mode.value == "calculated":
            if self.drop_down.value == "All":
                qbuild.append((CalcJobNode, WorkChainNode), tag="calcjobworkchain")
            else:
                qbuild.append(
                    (CalcJobNode, WorkChainNode),
                    filters={"label": self.drop_down.value},
                    tag="calcjobworkchain",
                )
            qbuild.append(
                self.query_type,
                with_incoming="calcjobworkchain",
                filters=filters,
            )

        elif self.mode.value == "edited":
            qbuild.append(CalcFunctionNode)
            qbuild.append(
                self.query_type,
                with_incoming=CalcFunctionNode,
                filters=filters,
            )

        elif self.mode.value == "all":
            qbuild.append(self.query_type, filters=filters)

        qbuild.order_by({self.query_type: {"ctime": "desc"}})
        matches = {n[0] for n in qbuild.iterall()}
        matches = sorted(matches, reverse=True, key=lambda n: n.ctime)

        options = [(f"Select a Structure ({len(matches)} found)", False)]
        for mch in matches:
            label = f"PK: {mch.pk}"
            label += " | " + mch.ctime.strftime("%Y-%m-%d %H:%M")
            label += " | " + mch.base.extras.get("formula", "")
            label += " | " + mch.node_type.split(".")[-2]
            label += " | " + mch.label
            label += " | " + mch.description
            options.append((label, mch))

        self.results.options = options
        return

    def _on_select_structure(self, _) -> None:
        self.data_object = self.results.value or None
        return

    def disable(self, val: bool) -> None:
        """Disable the widget."""
        self.results.disabled = True
        # self.
        return
