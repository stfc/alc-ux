import ipywidgets as ipw 
from IPython.display import display, Image
from datetime import datetime 

from .utils import getAppDir 


class MainApp:
    def __init__(self, process=None):
        self.process = process 
        self.view = MainAppView()
        display(self.view)

    def load(self) -> None:
        return 

class MainAppView(ipw.VBox):
    def __init__(self):

        logoImg = Image(
            filename = getAppDir() / "images/alc-100.png",
            width = 300,
        )
        logo = ipw.Output(layout={"margin": "auto"})
        with logo:
            display(logoImg)
        logo.add_class("logo")

        subtitle = ipw.HTML(
            """
            <h2 id='subtitle'>Welcome to the Ada Lovelace Center AiiDAlab App</h2>
            """
        )

        header = ipw.VBox(
            children=[
                logo, subtitle,
            ],
            layout={"margin": "auto"},
        )

        footer = ipw.HTML(f"""
            <footer>
                Copyright (c) {datetime.now().year} Ada Lovelace Center (STFC) <br>       
            </footer>
    
            """,
            layout={"align-content": "right"})

        super().__init__(
            layout={},
            children=[header,footer],
        )