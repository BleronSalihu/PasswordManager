
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout
)

from VaultDesk.Services.security import generate_password


class EntryDialog(QDialog):
    def __init__(self, entry=None, parent=None):
        super().__init__(parent)

        self.setWindowTitle(
            "Eintrag bearbeiten"
            if entry
            else "Eintrag hinzufügen"
        )
        self.setMinimumWidth(470)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(14)

        title = QLabel(
            "Eintrag bearbeiten"
            if entry
            else "Neuer Zugang"
        )

        title.setObjectName("title")
        layout.addWidget(title)

        form = QFormLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(
            "z. B. GitHub"
        )

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText(
            "Benutzername oder E-Mail"
        )

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText(
            "https://example.com"
        )

        form.addRow("Plattform:", self.title_input)
        form.addRow("Benutzername:", self.user_input)
        form.addRow("Passwort:", self.password_input)
        form.addRow("Website:", self.website_input)

        layout.addLayout(form)

        show = QCheckBox("Passwort anzeigen")
        show.toggled.connect(
            self.set_password_visible
        )
        layout.addWidget(show)

        generator = QHBoxLayout()

        generator.addWidget(QLabel("Länge:"))

        self.length = QSpinBox()
        self.length.setRange(8, 64)
        self.length.setValue(20)
        generator.addWidget(self.length)

        self.digits = QCheckBox("Zahlen")
        self.digits.setChecked(True)
        generator.addWidget(self.digits)

        self.symbols = QCheckBox("Sonderzeichen")
        self.symbols.setChecked(True)
        generator.addWidget(self.symbols)

        layout.addLayout(generator)

        create = QPushButton(
            "Passwort generieren"
        )
        create.clicked.connect(self.make_password)
        layout.addWidget(create)

        if entry:
            self.title_input.setText(
                entry["title"]
            )
            self.user_input.setText(
                entry["username"]
            )
            self.password_input.setText(
                entry["password"]
            )
            self.website_input.setText(
                entry["website"]
            )

        actions = QHBoxLayout()

        cancel = QPushButton("Abbrechen")
        cancel.clicked.connect(self.reject)

        save = QPushButton("Speichern")
        save.setObjectName("primary")
        save.clicked.connect(
            self.validate_and_accept
        )

        actions.addWidget(cancel)
        actions.addWidget(save)

        layout.addLayout(actions)

    def set_password_visible(self, visible):
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Normal
            if visible
            else QLineEdit.EchoMode.Password
        )

    def make_password(self):
        self.password_input.setText(
            generate_password(
                self.length.value(),
                self.digits.isChecked(),
                self.symbols.isChecked()
            )
        )

    def validate_and_accept(self):
        if not self.title_input.text().strip():
            QMessageBox.warning(
                self,
                "Fehler",
                "Bitte Plattform eingeben."
            )
            return

        if not self.password_input.text():
            QMessageBox.warning(
                self,
                "Fehler",
                "Bitte Passwort eingeben."
            )
            return

        self.accept()

    def get_data(self):
        return {
            "title": self.title_input.text().strip(),
            "username": self.user_input.text().strip(),
            "password": self.password_input.text(),
            "website": self.website_input.text().strip(),
        }

