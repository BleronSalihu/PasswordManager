
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)


class UnlockDialog(QDialog):
    def __init__(self, first_start=False, parent=None):
        super().__init__(parent)

        self.first_start = first_start
        self.password = ""

        self.setWindowTitle("VaultDesk - Zugang")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(14)

        title = QLabel(
            "Tresor einrichten"
            if first_start
            else "Tresor entsperren"
        )
        title.setObjectName("title")
        layout.addWidget(title)

        description = QLabel(
            "Lege ein Master-Passwort mit mindestens "
            "12 Zeichen fest. Ohne dieses Passwort "
            "lassen sich deine Daten nicht "
            "wiederherstellen."
            if first_start else
            "Gib dein Master-Passwort ein."
        )

        description.setObjectName("muted")
        description.setWordWrap(True)
        layout.addWidget(description)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(
            "Master-Passwort"
        )
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        layout.addWidget(self.password_input)

        self.confirm_input = None

        if first_start:
            self.confirm_input = QLineEdit()
            self.confirm_input.setPlaceholderText(
                "Master-Passwort wiederholen"
            )
            self.confirm_input.setEchoMode(
                QLineEdit.EchoMode.Password
            )
            layout.addWidget(self.confirm_input)

        submit = QPushButton(
            "Tresor erstellen"
            if first_start
            else "Entsperren"
        )

        submit.setObjectName("primary")
        submit.clicked.connect(self.submit)
        layout.addWidget(submit)

        self.password_input.returnPressed.connect(
            self.submit
        )

    def submit(self):
        value = self.password_input.text()

        if not value:
            QMessageBox.warning(
                self,
                "Fehler",
                "Bitte Passwort eingeben."
            )
            return

        if self.first_start:
            if len(value) < 12:
                QMessageBox.warning(
                    self,
                    "Fehler",
                    "Mindestens 12 Zeichen erforderlich."
                )
                return

            if value != self.confirm_input.text():
                QMessageBox.warning(
                    self,
                    "Fehler",
                    "Passwörter stimmen nicht überein."
                )
                return

        self.password = value
        self.accept()

