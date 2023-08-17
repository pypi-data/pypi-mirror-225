import json

import jsonschema
from PySide6 import QtNetwork, QtWebSockets

from tpds.helper import LogFacility

from .msg_handler import Messages


def _default_logger(msg):
    pass


class WebSocketConnection:
    """
    Handles events and state of a websocket connection
    """

    def __init__(
        self,
        connection: QtWebSockets.QWebSocket,
        messages=None,
        logger=_default_logger,
        parent=None,
    ):
        self._socket = connection
        self._messages = messages
        self._log = logger
        self._parent = parent

        self._socket.textMessageReceived.connect(self.processTextMessage)
        self._socket.textFrameReceived.connect(self.processTextFrame)
        self._socket.binaryMessageReceived.connect(self.processBinaryMessage)
        self._socket.disconnected.connect(self.socketDisconnected)
        self._log("websocket accepted new client")

    def processTextFrame(self, frame, is_last_frame):
        self._log("websocket processTextFrame")

    def processTextMessage(self, message):
        self._log("websocket text Message: {}".format(message))
        instance = json.loads(message)
        try:
            jsonschema.validate(instance, Messages.msg_schema)
        except ValueError:
            self._log("websocket - malformed message: {}".format(message))
            self._log("websocket - ignoring this message")
        response = self._messages.decode(json.loads(message))
        # Sends response to received message
        self._log(f"send message back: {response}")
        self._socket.sendTextMessage(response)

    def processBinaryMessage(self, message):
        self._log("websocket binary message:", message)
        if self.clientConnection:
            self.clientConnection.sendBinaryMessage(message)

    def socketDisconnected(self):
        self._log("websocket disconnected")
        self.close()
        if self._parent:
            self._parent.closeConnection(self)

    def close(self):
        try:
            self._socket.deleteLater()
        except:  # noqa E722
            pass


class WebSocketServer(QtWebSockets.QWebSocketServer):
    """
    A websocket server which connects the tpds application with the usecases
    """

    def __init__(self, port=1302, parent=None):
        super(WebSocketServer, self).__init__(
            "tpds websocket server", QtWebSockets.QWebSocketServer.NonSecureMode, None
        )
        self._clients = []
        self._messages = Messages(parent)
        self._log = LogFacility()
        self._log.log("websocket server name: {}".format(self.serverName()))
        if self.listen(QtNetwork.QHostAddress.LocalHost, port):
            self._log.log(
                "Listening: {}:{}:{}".format(
                    self.serverName(), self.serverAddress().toString(), str(self.serverPort())
                )
            )
        else:
            self._log.log("websocket listen error")
        self.acceptError.connect(self.onAcceptError)
        self.newConnection.connect(self.onNewConnection)
        self._log.log("websocket is Listening: {}".format(self.isListening()))

    def onAcceptError(self, accept_error):
        self._log.log("websocket accept Error: {}".format(accept_error))

    def onNewConnection(self):
        self._log.log("websocket new connection")
        new_connection = WebSocketConnection(
            self.nextPendingConnection(), messages=self._messages, logger=self._log.log, parent=self
        )
        self._clients.append(new_connection)

    def closeConnection(self, connection):
        self._log.log("websocket removing closed connection")
        if connection in self._clients:
            self._clients.remove(connection)

    def shutdown(self):
        for x in self._clients:
            x.close()
        self.close()
