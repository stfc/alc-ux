import ipywidgets as ipw 

def get_start_widget(appbase, jupbase, notebase):
    return ipw.HTML(f"""
        <div class="app-container">
            <a class="logo" href="{appbase}/main.ipynb" target="_blank">
            <img src="{appbase}/images/alc-100.webp" alt="ALC AiiDAlab App Logo" />
            </a>
        </div>
        """)