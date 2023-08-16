from urllib.parse import urlencode, parse_qs

from PySide6 import QtCore, QtGui, QtWidgets, QtWebEngineCore, QtWebEngineWidgets


"""
login   anxious-elephant@example.com
password    Frantic-Magpie-Tame-Cow-9
"""

ClientId = "nomad_public"
RedirectUrl = "nomad.eln.data.fau.de%2Fnomad-oasis%2Fgui%2Fabout%2Finformation"
RedirectScheme = "https://"
Scopes = ["photo offline_access"]

ResponseType = "code"

Headers = {
    "client_id": ClientId,
    "redirect_uri": RedirectScheme + RedirectUrl,
    "response_type": ResponseType,
    # "scope": str.join(" ", Scopes),
    "state": "c4317329-ede9-4409-80cf-4f9d1f0e900e",
    "scope": "openid",
    "nonce": "2770f2d5-f181-4995-8530-1a39970b7532",
    "response_mode": "fragment"
}

AuthUrl = "https://nomad.eln.data.fau.de/keycloak/auth/realms/nomad/protocol/openid-connect/auth?{headers}".format(
    headers=urlencode(Headers)
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(234, 167)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 234, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLogin = QtGui.QAction(MainWindow)
        self.actionLogin.setObjectName("actionLogin")
        self.menuFile.addAction(self.actionLogin)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionLogin.setText(_translate("MainWindow", "Login"))


class RequestInterceptor(QtWebEngineCore.QWebEngineUrlRequestInterceptor):
    codeChanged = QtCore.Signal(str)

    def interceptRequest(self, info):
        if RedirectUrl == (info.requestUrl().host() + info.requestUrl().path()):
            params = parse_qs(info.requestUrl().query())
            if "code" in params.keys():
                code = params["code"][0][0]
                print("OAuth code is {code}".format(code=params["code"][0][0]))
                self.codeChanged.emit(code)


class LoginWindow(QtWebEngineWidgets.QWebEngineView):
    codeChanged = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setUrl(QtCore.QUrl(AuthUrl))
        self.loadFinished.connect(self._loadFinished)
        self.interceptor = RequestInterceptor(self)
        self.page().profile().setUrlRequestInterceptor(self.interceptor)
        self.show()

        self.interceptor.codeChanged.connect(self.codeChanged)

    @QtCore.Slot(bool)
    def _loadFinished(self, result):
        self.page().toHtml(self.callable)

    def callable(self, data):
        self.html = data


class MainMenu(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainMenu, self).__init__()
        self.setupUi(self)
        self.actionLogin.triggered.connect(self.login)

        lay = QtWidgets.QVBoxLayout(self.centralwidget)
        self.code_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        lay.addWidget(self.code_label)

    @QtCore.Slot()
    def login(self):
        self.browser = LoginWindow()
        self.browser.codeChanged.connect(self.onCodeChanged)

    @QtCore.Slot(str)
    def onCodeChanged(self, code):
        self.code_label.setText(code)
        # self.browser.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    menu = MainMenu()
    menu.show()
    sys.exit(app.exec_())