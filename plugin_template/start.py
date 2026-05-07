"""Defines the main AiiDAlab app's start banner."""

import ipywidgets as ipw

from aiidalab_alc.common.navigation import QuickAccessButtons


def get_start_widget(appbase, jupbase, notebase):
    """Get the AiiDAlab app's start banner."""
    logo = ipw.HTML(
        f"""
        <div class="app-container">
            <a class="logo" href="{appbase}/main.ipynb" target="_blank">
            <img src="{appbase}/images/alc.svg" alt="ALC AiiDAlab App Logo" />
            </a>
        </div>
        """
    )
    return ipw.VBox(
        children=[
            logo,
            QuickAccessButtons(),
        ]
    )
