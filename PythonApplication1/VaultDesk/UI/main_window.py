
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QDialog
)

from VaultDesk.UI.enter_dialog import EntryDialog


class MainWindow(QMainWindow):
    def __init__(self, repository):
        super().__init__()

        self.repository = repository
        self.entries = []

        self.setWindowTitle(
            "VaultDesk - Passwortmanager"
        )
        self.resize(1060, 680)
        self.setMinimumSize(760, 480)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(18)

        header = QHBoxLayout()
        title_area = QVBoxLayout()

        title = QLabel("VaultDesk")
        title.setObjectName("title")
        title_area.addWidget(title)

        subtitle = QLabel(
            "Dein lokaler, verschlüsselter Passwort-Tresor"
        )
        subtitle.setObjectName("muted")
        title_area.addWidget(subtitle)

        header.addLayout(title_area)
        header.addStretch()

        add_button = QPushButton("+ Neuer Eintrag")
        add_button.setObjectName("primary")
        add_button.clicked.connect(self.add_entry)

        header.addWidget(add_button)
        layout.addLayout(header)

        self.search = QLineEdit()
        self.search.setPlaceholderText(
            "Einträge durchsuchen ..."
        )
        self.search.textChanged.connect(self.refresh)

        layout.addWidget(self.search)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels([
            "Plattform",
            "Benutzername",
            "Passwort",
            "Website"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().hide()

        self.table.cellDoubleClicked.connect(
            self.edit_entry
        )

        layout.addWidget(self.table)

        controls = QHBoxLayout()

        edit = QPushButton("Bearbeiten")
        edit.clicked.connect(self.edit_entry)

        copy = QPushButton("Passwort kopieren")
        copy.clicked.connect(self.copy_password)

        delete = QPushButton("Löschen")
        delete.setObjectName("danger")
        delete.clicked.connect(self.delete_entry)

        controls.addWidget(edit)
        controls.addWidget(copy)
        controls.addStretch()
        controls.addWidget(delete)

        layout.addLayout(controls)

        self.status = QLabel("")
        self.status.setObjectName("muted")

        layout.addWidget(self.status)

        self.refresh()

    def refresh(self, *_):
        self.entries = self.repository.list_entries()

        query = self.search.text().strip().casefold()

        matches = [
            entry for entry in self.entries
            if query in entry["title"].casefold()
            or query in entry["username"].casefold()
            or query in entry["website"].casefold()
        ]

        self.table.setRowCount(len(matches))

        for row, entry in enumerate(matches):
            values = [
                entry["title"],
                entry["username"],
                "••••••••••••",
                entry["website"]
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(value)

                if col == 0:
                    item.setData(
                        Qt.ItemDataRole.UserRole,
                        entry["id"]
                    )

                self.table.setItem(row, col, item)

        self.status.setText(
            f"{len(matches)} von "
            f"{len(self.entries)} Einträgen"
        )

    def selected_entry(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.information(
                self,
                "Hinweis",
                "Bitte Eintrag auswählen."
            )
            return None

        item = self.table.item(row, 0)

        if item is None:
            return None

        entry_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        return next(
            (
                entry
                for entry in self.entries
                if entry["id"] == entry_id
            ),
            None
        )

    def add_entry(self):
        dialog = EntryDialog(parent=self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.repository.save_entry(
                dialog.get_data()
            )
            self.refresh()

    def edit_entry(self, *_):
        entry = self.selected_entry()

        if entry is None:
            return

        dialog = EntryDialog(
            entry=entry,
            parent=self
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.repository.save_entry(
                dialog.get_data(),
                entry["id"]
            )
            self.refresh()

    def delete_entry(self):
        entry = self.selected_entry()

        if entry is None:
            return

        answer = QMessageBox.question(
            self,
            "Löschen",
            f"'{entry['title']}' wirklich löschen?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:
            self.repository.delete_entry(
                entry["id"]
            )
            self.refresh()

    def copy_password(self):
        entry = self.selected_entry()

        if entry is None:
            return

        clipboard = QApplication.clipboard()
        password = entry["password"]

        clipboard.setText(password)

        self.status.setText(
            "Passwort kopiert (30 Sekunden)."
        )

        def clear_if_unchanged():
            if clipboard.text() == password:
                clipboard.clear()

        QTimer.singleShot(
            30_000,
            clear_if_unchanged
        )

    def closeEvent(self, event):
        self.repository.close()
        event.accept()

