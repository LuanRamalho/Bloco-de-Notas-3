from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QTextEdit, QFileDialog, QVBoxLayout,
    QWidget, QAction, QToolBar, QFontDialog, QMessageBox, QLabel, QStatusBar, QMenuBar, QMenu
)
import sys

class NotePad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bloco de Notas")
        self.resize(800, 600)

        # Widget principal
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.character_count_label = QLabel("Caracteres: 0 (com linhas) / 0 (sem linhas)")
        self.cursor_position_label = QLabel("Linha: 1, Coluna: 1")
        self.status_bar.addWidget(self.character_count_label)
        self.status_bar.addPermanentWidget(self.cursor_position_label)

        # Criar barra de menu
        self.create_menu_bar()

        # Criar a primeira aba
        self.new_tab()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # Menu Arquivo
        file_menu = menu_bar.addMenu("Arquivo")

        new_tab_action = QAction("Nova Guia", self)
        new_tab_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_tab_action)

        open_action = QAction("Abrir", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Salvar", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        close_action = QAction("Fechar", self)
        close_action.triggered.connect(self.close_program)
        file_menu.addAction(close_action)

        # Menu Editar
        edit_menu = menu_bar.addMenu("Editar")

        edit_font_action = QAction("Editar Fonte", self)
        edit_font_action.triggered.connect(self.edit_font)
        edit_menu.addAction(edit_font_action)

        # Menu Sobre
        about_menu = menu_bar.addMenu("Sobre")

        about_action = QAction("Sobre o bloco de Notas", self)
        about_action.triggered.connect(self.show_about)
        about_menu.addAction(about_action)

    def new_tab(self):
        text_edit = QTextEdit()
        text_edit.textChanged.connect(self.update_character_count)
        text_edit.cursorPositionChanged.connect(self.update_cursor_position)
        tab_index = self.tabs.addTab(text_edit, "Nova Guia")
        self.tabs.setCurrentIndex(tab_index)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", "Arquivos de Texto (*.txt);;Todos os Arquivos (*)")
        if file_name:
            with open(file_name, "r", encoding="utf-8") as file:
                content = file.read()

            text_edit = QTextEdit()
            text_edit.setText(content)
            text_edit.textChanged.connect(self.update_character_count)
            text_edit.cursorPositionChanged.connect(self.update_cursor_position)
            tab_index = self.tabs.addTab(text_edit, file_name.split("/")[-1])
            self.tabs.setCurrentIndex(tab_index)

    def save_file(self):
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget, QTextEdit):
            file_name, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo", "", "Arquivos de Texto (*.txt);;Todos os Arquivos (*)")
            if file_name:
                with open(file_name, "w", encoding="utf-8") as file:
                    file.write(current_widget.toPlainText())

    def close_program(self):
        self.close()

    def edit_font(self):
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget, QTextEdit):
            font, ok = QFontDialog.getFont()
            if ok:
                current_widget.setFont(font)

    def show_about(self):
        QMessageBox.information(
            self,
            "Sobre",
            "Esse bloco de notas foi desenvolvido no dia 18 de janeiro de 2025 por Luan da Silva Ramalho, um jovem nerd,"
            " formado em ciência da computação pela Unicarioca, Centro Universitário Carioca, no Rio de Janeiro, que ama programação"
            ", desenvolvimento de softwares e diversas áreas em tecnologia da informação. Ele ama o que ele faz e tem a maior felicidade"
            "em desenvolver os softwares e colocar no github para compartilhar tudo que ele gosta de fazer."
        )

    def update_character_count(self):
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget, QTextEdit):
            text = current_widget.toPlainText()
            total_chars_with_lines = len(text)
            total_chars_without_lines = len(text.replace("\n", ""))
            self.character_count_label.setText(
                f"Caracteres: {total_chars_with_lines} (com linhas) / {total_chars_without_lines} (sem linhas)"
            )

    def update_cursor_position(self):
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget, QTextEdit):
            cursor = current_widget.textCursor()
            line = cursor.blockNumber() + 1
            column = cursor.columnNumber() + 1
            self.cursor_position_label.setText(f"Linha: {line}, Coluna: {column}")

def main():
    app = QApplication(sys.argv)
    notepad = NotePad()
    notepad.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
