from beaker_kernel.lib.app import BeakerApp


class BeakerMineralsApp(BeakerApp):
    slug = "beaker-minerals"
    name = "Beaker Minerals"

    pages = {
        'chat': {
            "title": "Beaker Minerals chat",
            "default": True,
        },
        "notebook": {
            "title": "Beaker Minerals notebook",
        },
        "dev": {
            "title": "Beaker Minerals dev interface",
        }
    }
    default_context = {
        "slug": "beaker_minerals",
        "payload": {},
        "single_context": True,
    }

    assets = {
        "header_logo": {
            "src": "beaker-minerals.png",
            "alt": "Beaker Minerals logo"
        },
        "body_logo": {
            "src": "beaker-minerals.png",
            "alt": "Beaker Minerals logo"
        }
    }

    template_bundle = {
        "short_title": " Beaker Minerals",
        "chat_welcome_html": """<div style="display: flex; flex-direction: row; align-items: center; gap: 20px;">
          <img src="{asset:body_logo:src}" alt="Beaker Minerals Logo" height="100px">
          <p>Hi! I'm your Beaker Minerals Agent and I'm an expert in critical minerals analysis. I have access to a 
          wide range of data from USGS and more and am ready to assist you analyze supply chain risk due to mineral production and armed conflict.</p>
        </div>"""
    }