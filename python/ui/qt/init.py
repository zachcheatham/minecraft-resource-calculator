import sys
from PyQt5.QtWidgets import QApplication

import ui.qt.window_manager
from ui.qt.new_craft_dialog import NewCraftDialog

def show_initial_window():
    craft_dialog = NewCraftDialog()
    craft_dialog.show()
    ui.qt.window_manager.retain(craft_dialog)

def start_application():
    app = QApplication(sys.argv)
    show_initial_window()
    sys.exit(app.exec_())
