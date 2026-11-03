import sys

from PySide6.QtWidgets import QApplication, QMessageBox, QDialog

from VaultDesk.Data.repository import VaultRepository
from VaultDesk.UI.main_window import MainWindow
from VaultDesk.UI.style import STYLE
from VaultDesk.UI.unlock_dialog import UnlockDialog


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)

    repository = VaultRepository()
    first_start = not repository.is_initialized()

    while True:
        dialog = UnlockDialog(first_start=first_start)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            repository.close()
            return 0

        if first_start:
            repository.initialize(dialog.password)
            break

        if repository.unlock(dialog.password):
            break

        QMessageBox.warning(
            None,
            "Fehler",
            "Master-Passwort ist falsch."
        )

    window = MainWindow(repository)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
