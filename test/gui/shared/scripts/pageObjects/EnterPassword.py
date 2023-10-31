import names
import squish
from helpers.WebUIHelper import authorize_via_webui
from helpers.ConfigHelper import get_config
from pageObjects.AccountConnectionWizard import AccountConnectionWizard


class EnterPassword:
    LOGIN_DIALOG = {
        "name": "LoginRequiredDialog",
        "type": "OCC::LoginRequiredDialog",
        "visible": 1,
    }
    USERNAME_BOX = {
        "name": "usernameLineEdit",
        "type": "QLineEdit",
        "visible": 1,
        "window": LOGIN_DIALOG,
    }
    PASSWORD_BOX = {
        "name": "passwordLineEdit",
        "type": "QLineEdit",
        "visible": 1,
        "window": LOGIN_DIALOG,
    }
    LOGIN_BUTTON = {
        "text": "Log in",
        "type": "QPushButton",
        "unnamed": 1,
        "visible": 1,
        "window": LOGIN_DIALOG,
    }
    COPY_URL_TO_CLIPBOARD_BUTTON = {
        "name": "copyUrlToClipboardButton",
        "type": "QPushButton",
        "visible": 1,
        "window": LOGIN_DIALOG,
    }

    def __init__(self, occurrence=1):
        if occurrence > 1:
            self.LOGIN_DIALOG.update({"occurrence": occurrence})

    def get_username(self):
        return str(squish.waitForObjectExists(self.USERNAME_BOX).text)

    def enterPassword(self, password):
        squish.waitForObjectExists(
            self.PASSWORD_BOX, get_config('maxSyncTimeout') * 1000
        )
        squish.type(
            squish.waitForObject(self.PASSWORD_BOX),
            password,
        )
        squish.clickButton(squish.waitForObjectExists(self.LOGIN_BUTTON))

    def oidcReLogin(self, username, password):
        # wait 500ms for copy button to fully load
        squish.snooze(1 / 2)
        squish.clickButton(squish.waitForObject(self.COPY_URL_TO_CLIPBOARD_BUTTON))
        authorize_via_webui(username, password)

    def reLogin(self, username, password):
        if get_config('ocis'):
            self.oidcReLogin(username, password)
        else:
            self.enterPassword(password)

    def loginAfterSetup(self, username, password):
        if get_config('ocis'):
            AccountConnectionWizard.acceptCertificate()
            self.oidcReLogin(username, password)
        else:
            self.enterPassword(password)
