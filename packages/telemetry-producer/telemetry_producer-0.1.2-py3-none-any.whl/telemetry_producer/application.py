from .handlers import RouteHandler
from jupyter_server.extension.application import ExtensionApp
from traitlets import Bool, List

class TelemetryProducerApp(ExtensionApp):

    name = "telemetry_producer"

    activeEvents = List([]).tag(config=True)
    logNotebookContentEvents = List([]).tag(config=True)

    def initialize_settings(self):
        try:
            assert self.activeEvents, "The c.TelemetryProducerApp.activeEvents configuration setting must be set."

        except Exception as e:
            self.log.error(str(e))
            raise e

    def initialize_handlers(self):
        try:
            self.handlers.extend([(r"/telemetry-producer/(.*)", RouteHandler)])
        except Exception as e:
            self.log.error(str(e))
            raise e
