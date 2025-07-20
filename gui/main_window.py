import json
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QListWidget,
    QTextEdit, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Board Simulator (alpha)")
        self.resize(1000, 600)

        self.load_data()
        self.init_ui()

    def load_data(self):
        """Wczytuje dane z JSON."""
        with open(os.path.join("data", "boards.json"), encoding="utf-8") as f:
            self.boards = json.load(f)

        with open(os.path.join("data", "components.json"), encoding="utf-8") as f:
            self.components = json.load(f)

    def init_ui(self):
        """Tworzy layout GUI."""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout(main_widget)

        # Lewy panel — listy wyboru
        left_panel = QVBoxLayout()
        self.board_list = QListWidget()
        self.board_list.addItems([b["name"] for b in self.boards])
        self.board_list.currentRowChanged.connect(self.display_board)

        self.comp_list = QListWidget()
        self.comp_list.addItems([c["name"] for c in self.components])
        self.comp_list.currentRowChanged.connect(self.display_component)

        left_panel.addWidget(QLabel("📋 Boards"))
        left_panel.addWidget(self.board_list)
        left_panel.addWidget(QLabel("📋 Components"))
        left_panel.addWidget(self.comp_list)

        # Prawy panel — obraz + opis
        right_panel = QVBoxLayout()

        self.image_label = QLabel("Select a board or component")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedHeight(300)

        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)

        right_panel.addWidget(self.image_label)
        right_panel.addWidget(self.info_text)

        layout.addLayout(left_panel, 1)
        layout.addLayout(right_panel, 3)

        # Ustaw domyślne
        if self.boards:
            self.board_list.setCurrentRow(0)
        if self.components:
            self.comp_list.setCurrentRow(0)

    def display_board(self, index):
        """Pokazuje dane wybranej płytki."""
        if index < 0:
            return
        board = self.boards[index]
        self.show_info(board, item_type="board")

    def display_component(self, index):
        """Pokazuje dane wybranego komponentu."""
        if index < 0:
            return
        comp = self.components[index]
        self.show_info(comp, item_type="component")

    def show_info(self, item, item_type):
        """
        Wyświetla dane (obrazek + opis) dla płytki lub komponentu.
        Jeśli komponent zawiera dodatkowe 'connections', też je pokaż.
        """
        # Ustaw obrazek
        if item_type == "board":
            image_path = item.get("image")
        else:
            # dla komponentów preferuj wiring_image
            image_path = item.get("wiring_image") or item.get("image")

        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaledToHeight(
                300, Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("No image")

        # Przygotuj tekst
        text = f"### {item['name']}\n\n{item['description']}\n\nNotes: {item.get('notes', '')}"

        # Dodaj wiring info jeśli istnieje
        if "connections" in item and item["connections"]:
            text += f"\n\n---\n\n🔗 Connections:\n{item['connections']}"

        self.info_text.setText(text)
