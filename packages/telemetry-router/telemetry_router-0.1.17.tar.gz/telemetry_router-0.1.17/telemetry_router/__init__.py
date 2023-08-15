try:
    from ._version import __version__
except ImportError:
    # Fallback when using the package in dev mode without installing
    # in editable mode with pip. It is highly recommended to install
    # the package from a stable release or in editable mode: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
    import warnings
    warnings.warn("Importing 'telemetry_router' outside a proper installation.")
    __version__ = "dev"

from .application import TelemetryRouterApp

def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "telemetry-router"
    }]

def _jupyter_server_extension_points():
    return [{
        "module": "telemetry_router",
        "app": TelemetryRouterApp
    }]

load_jupyter_server_extension = TelemetryRouterApp.load_classic_server_extension
