from __future__ import annotations

"""
Tools to manage the full TPDS backend
"""
import os
import signal
import sys
from typing import Any

# While the websocket application is being used the backend has to be a
# qt application
from PySide6.QtCore import QCoreApplication, QTimer

from tpds.api import TpdsApiServer
from tpds.helper import LogFacility, ProcessingUtils
from tpds.servers import JupyterServer, UnoServer, WebSocketServer
from tpds.settings import TrustPlatformSettings
from tpds.usecase_collector import Collector


class TpdsBackend:
    """
    Manage TPDS backend services
    """

    __shared_state: dict[str, Any] = {}

    def __new__(cls, **kwargs: str) -> Any:
        # Only ever allow one global instance of the usecase collector
        instance = super().__new__(cls)
        instance.__dict__ = cls.__shared_state
        return instance

    def __init__(self) -> None:
        if not self.__shared_state:
            self._config = TrustPlatformSettings()
            self._log = LogFacility()
            self._proc = ProcessingUtils()
            self._usecases = Collector()
            self._websocket_server = None
            self._voila = []
            self._api_server = None

    def start(self) -> None:
        # Start the websocket server in a separate thread
        self._websocket_server = WebSocketServer(parent=self)

        # Start new API Server and usecase collector
        self._api_server = TpdsApiServer(ports=range(5001, 5010))
        self._api_server.start()

        self.start_uno()
        self.start_jupyter()

    def start_uno(self):
        ta_path = self._config.packages.get("trust_anchor", "")
        if os.path.exists(ta_path) and self._uno is None:
            self._uno = UnoServer()
            self._uno.start_uno(path=ta_path)

    def _check_jupyter_instances(self, path):
        for js in self._voila:
            if js._start_directory == path:
                return True
        return False

    def start_jupyter(self):
        for uc_path_info in self._usecases.get_search_paths():
            if uc_path_info.get("notebook", False):
                uc_path = uc_path_info["path"]
                if not self._check_jupyter_instances(uc_path):
                    js = JupyterServer(
                        port=self._config.settings.jupyter_port, start_directory=uc_path
                    )
                    js.start_jupyter()
                    self._voila += [js]

    def stop(self) -> None:
        if self._websocket_server:
            self._websocket_server.shutdown()

        for js in self._voila:
            js.stop_jupyter()

        if self._api_server:
            self._api_server.stop()

    def run(self) -> None:
        """
        Run until an exit signal is encountered
        """
        self.start()
        signal.sigwait([signal.SIGINT])
        self.stop()

    def is_ready(self) -> bool:
        return self._api_server and self._api_server.up()

    def api_port(self) -> int:
        return self._api_server.port


def launch_tpds_core():
    """
    Launch all backend services used by TPDS
    """
    # The websocket server and message handlers are all based on QT so they
    # require this to be run as part of a QApplication
    app = QCoreApplication(sys.argv)
    backend = TpdsBackend()
    backend.start()

    def handler(sig_id, frame):
        print("closing backend")
        backend.stop()
        app.exit(0)

    # Allow SIGINT to stop the application
    signal.signal(signal.SIGINT, handler)

    # This is to periodically run the interpreter to catch the signal
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    sys.exit(app.exec_())


__all__ = ["launch_tpds_core", "TpdsBackend"]


if __name__ == "__main__":
    launch_tpds_core()
