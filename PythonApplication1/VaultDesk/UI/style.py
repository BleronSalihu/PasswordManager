
STYLE = """
QWidget {
    background-color: #12151c;
    color: #edf0f7;
    font-family: 'Segoe UI';
    font-size: 13px;
}

QLabel#title {
    font-size: 28px;
    font-weight: 700;
    color: white;
}

QLabel#muted {
    color: #9da9bd;
}

QLineEdit, QSpinBox {
    background-color: #202634;
    color: white;
    border: 1px solid #364154;
    border-radius: 8px;
    padding: 9px;
    min-height: 18px;
}

QLineEdit:focus, QSpinBox:focus {
    border: 1px solid #827aff;
}

QPushButton {
    background-color: #2a3242;
    color: white;
    border: 1px solid #3b455a;
    border-radius: 8px;
    padding: 10px 15px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #39455b;
}

QPushButton#primary {
    background-color: #6964eb;
    border: none;
}

QPushButton#primary:hover {
    background-color: #817cff;
}

QPushButton#danger {
    background-color: #5a2a38;
    color: #ffd0d9;
}

QTableWidget {
    background-color: #1d2330;
    alternate-background-color: #242b3a;
    border: 1px solid #364154;
    border-radius: 8px;
    gridline-color: #333d51;
    selection-background-color: #4a4588;
}

QTableWidget::item {
    padding: 8px;
}

QHeaderView::section {
    background-color: #2b3446;
    color: #d3dded;
    border: none;
    padding: 10px;
    font-weight: bold;
}
"""

