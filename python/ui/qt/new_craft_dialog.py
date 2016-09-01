from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

import recipes
import ui.qt.window_manager
from ui.qt.designer.new_craft_dialog import Ui_newCraftDialog
from ui.qt.recipe_dialog import RecipeDialog
from ui.qt.main_window import MainWindow

class NewCraftDialog(QDialog, Ui_newCraftDialog):
    def __init__(self, parent=None):
        super(NewCraftDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & (~Qt.WindowContextHelpButtonHint))
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)

        self.itemNameLineEdit.textEdited.connect(self.item_name_line_edit_edited)
        self.calculateButton.clicked.connect(self.calculate_button_clicked)
        self.closeButton.clicked.connect(self.close_button_clicked)

    def open_craft(self):
        craft_window = self.parentWidget()
        if craft_window == None:
            craft_window = MainWindow()
            craft_window.show()
            ui.qt.window_manager.retain(craft_window)

        craft_window.set_craft_item(self.itemNameLineEdit.text(), self.quantitySpinBox.value())
        self.close()

    def item_name_line_edit_edited(self, text):
        if len(self.itemNameLineEdit.text()) > 0:
            self.calculateButton.setEnabled(True)
        else:
            self.calculateButton.setEnabled(False)

    def calculate_button_clicked(self):
        item_name = self.itemNameLineEdit.text()
        if recipes.have_missing(item_name):
            # Get the user's input on recipes
            recipeDialog = RecipeDialog(item_name, self)
            recipeDialog.finished.connect(self.recipe_dialog_finished)
            recipeDialog.show()
        else:
            self.open_craft()

    def recipe_dialog_finished(self, result):
        item_name = self.itemNameLineEdit.text()
        if not recipes.have_missing(item_name):
            self.open_craft()

    def close_button_clicked(self):
        self.close()
