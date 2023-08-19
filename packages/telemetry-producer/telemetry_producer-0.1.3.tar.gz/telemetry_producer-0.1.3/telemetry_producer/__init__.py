try:
    from ._version import __version__
except ImportError:
    # Fallback when using the package in dev mode without installing
    # in editable mode with pip. It is highly recommended to install
    # the package from a stable release or in editable mode: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
    import warnings
    warnings.warn("Importing 'telemetry_producer' outside a proper installation.")
    __version__ = "dev"

from .application import TelemetryProducerApp

def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "telemetry-producer"
    }]

def _jupyter_server_extension_points():
    return [{
        "module": "telemetry_producer",
        "app": TelemetryProducerApp
    }]

load_jupyter_server_extension = TelemetryProducerApp.load_classic_server_extension