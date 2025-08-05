import ipywidgets as ipw 
from functools import partial

# from aiidalab_alc.main import QuickAccessButtons

def get_start_widget(appbase, jupbase, notebase):
    logo = ipw.HTML(f"""
        <div class="app-container">
            <a class="logo" href="{appbase}/main.ipynb" target="_blank">
            <img src="{appbase}/images/alc-100.webp" alt="ALC AiiDAlab App Logo" />
            </a>
        </div>
        """
    )
    return ipw.VBox(
        children=[
            logo, QuickAccessButtons(),
        ]
    ) 

# This is a duplicate from main.py, but the import doesn't work here???
class QuickAccessButtons(ipw.HBox):
    def __init__(self, **kwargs):

        # This is a duplicate from utils.py
        def openLinkInNewTab(path: str, _ = None) -> None:
            jsCode = f"window.open('{path}', '_blank');"
            from IPython.display import Javascript, display 
            display(Javascript(jsCode))
            return 
        
        self.newCalcLink = ipw.Button(
            description="New Calculation", 
            disabled=False, 
            button_style="success", 
            tooltip="Start a new calculation", 
            icon="plus",
        )
        self.newCalcLink.on_click(partial(openLinkInNewTab, "main.ipynb"))

        self.historyLink = ipw.Button(
            description="History",
            disabled=False,
            button_style="primary",
            tooltip="View Calculation History",
            icon="history",
        )
        self.historyLink.on_click(partial(openLinkInNewTab, "history.ipynb"))

        self.setupResourcesLink = ipw.Button(
            description="Setup Resources", 
            disabled=False, 
            button_style="primary",
            tooltip="Configure Computational Resources",
            icon="cogs",
        )
        self.setupResourcesLink.on_click(partial(openLinkInNewTab, "../home/code_setup.ipynb"))

        self.docsLink = ipw.Button(
            description="Documentation", 
            disabled=False, 
            button_style="info", 
            tooltip="Open Documentation", 
            icon="book",
        )
        self.docsLink.on_click(partial(openLinkInNewTab, "https://github.com/stfc/alc-ux"))

        children=[
            self.newCalcLink,
            self.historyLink,
            self.setupResourcesLink,
            self.docsLink,
        ]
        super().__init__(children=children, layout={'margin': 'auto'}, **kwargs)
        return 