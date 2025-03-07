from beaker_kernel.lib.app import BeakerApp


class BeakerFireApp(BeakerApp):
    slug = "beaker-fire"
    name = "Beaker Fire"

    pages = {
        'chat': {
            "title": "Beaker Fire chat",
            "default": True,
        },
        "notebook": {
            "title": "Beaker Fire notebook",
        },
        "dev": {
            "title": "Beaker Fire dev interface",
        }
    }
    default_context = {
        "slug": "beaker_fire",
        "payload": {},
        "single_context": True,
    }

    assets = {
        "header_logo": {
            "src": "beaker-fire.png",
            "alt": "Beaker Fire logo"
        },
        "body_logo": {
            "src": "beaker-fire.png",
            "alt": "Beaker Fire logo"
        }
    }

    template_bundle = {
        "short_title": " Beaker Fire",
        "chat_welcome_html": """<div style="display: flex; flex-direction: row; align-items: center; gap: 20px;">
          <img src="{asset:body_logo:src}" alt="Beaker Fire Logo" height="100px">
          <p>Hi! I'm Beaker, your AI assistant for wildfire analysis. I have access to a 
          wide range of data and am ready to assist you analyze wildfire risk and impact.</p>
        </div>"""
    }