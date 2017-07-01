from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QHeaderView

import recipes
import util
from ui.qt.designer.recipe_dialog import Ui_recipeDialog

class RecipeDialog(QDialog, Ui_recipeDialog):
    def __init__(self, item_name, parent=None, editing_recipe=False):
        super(RecipeDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & (~Qt.WindowContextHelpButtonHint))
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)

        self.ingredients_model = QStandardItemModel()
        self.ingredients_model.setHorizontalHeaderLabels(["Item Name", "Quantity"])
        self.ingredientTable.setAllColumnsShowFocus(True)
        self.ingredientTable.setExpandsOnDoubleClick(False)
        self.ingredientTable.setRootIsDecorated(False)
        self.ingredientTable.setSortingEnabled(False)
        self.ingredientTable.setHeaderHidden(False)
        self.ingredientTable.setModel(self.ingredients_model)
        self.ingredientTable.selectionModel().selectionChanged.connect(self.ingredients_selection_changed)
        header = self.ingredientTable.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        self.itemNameLineEdit.textEdited.connect(self.item_name_line_edit_edited)
        self.addButton.clicked.connect(self.add_button_clicked)
        self.removeButton.clicked.connect(self.remove_button_clicked)
        self.doneButton.clicked.connect(self.done_button_clicked)

        self.title_label_format = self.titleLabel.text()

        if editing_recipe:
            self.recipe_queue = [item_name]
        else:
            self.recipe_queue = recipes.get_missing_recipes(item_name)

        self.next_recipe()
        if editing_recipe:
            recipe_data = recipes.get_recipe(item_name)
            if recipe_data != None:
                for ingredient, quantity in recipe_data["r"].items():
                    ingredient = QStandardItem(ingredient)
                    quantity = QStandardItem(str(quantity))
                    self.ingredients_model.appendRow([ingredient, quantity])

                self.quantityProducedSpinBox.setEnabled(True)
                self.quantityProducedSpinBox.setValue(recipe_data["p"])
                self.doneButton.setText("Done")

    def item_name_in_ingredients(self, item_name):
        for i in range(0, self.ingredients_model.rowCount()):
            index = self.ingredients_model.index(i, 0)
            if item_name == self.ingredients_model.data(index):
                return True

        return False

    def next_recipe(self):
        self.item_name = self.recipe_queue[0]
        self.titleLabel.setText(self.title_label_format.format(self.item_name))
        self.itemNameLineEdit.setText("")
        self.quantitySpinBox.setValue(1)
        self.quantityProducedSpinBox.setValue(1)
        self.doneButton.setText("Raw Material")
        for i in range(0, self.ingredients_model.rowCount()):
            self.ingredients_model.takeRow(0)

    def item_name_line_edit_edited(self, text):
        if len(text) > 0 and text != self.item_name and not self.item_name_in_ingredients(text):
            self.addButton.setEnabled(True)
        else:
            self.addButton.setEnabled(False)

    def ingredients_selection_changed(self, selected, deselected):
        if selected.count() > 0:
            self.removeButton.setEnabled(True)
        else:
            self.removeButton.setEnabled(False)

    def add_button_clicked(self):
        ingredient_name = self.itemNameLineEdit.text()
        quantity = self.quantitySpinBox.value()

        ingredient = QStandardItem(ingredient_name)
        quantity = QStandardItem(str(quantity))
        self.ingredients_model.appendRow([ingredient, quantity])

        self.itemNameLineEdit.setText("")
        self.quantitySpinBox.setValue(1)
        self.addButton.setEnabled(False)
        self.itemNameLineEdit.setFocus()

        self.quantityProducedSpinBox.setEnabled(True)
        self.doneButton.setText("Done")

    def remove_button_clicked(self):
        row = self.ingredientTable.selectedIndexes()[0].row()
        self.ingredients_model.takeRow(row)

        if self.ingredients_model.rowCount() == 0:
            self.quantityProducedSpinBox.setEnabled(False)
            self.doneButton.setText("Raw Material")

    def done_button_clicked(self, text):
        # Save recipe
        ingredients = {}
        if self.ingredients_model.rowCount() > 0:
            quantity_produced = self.quantityProducedSpinBox.value()
            for i in range(0, self.ingredients_model.rowCount()):
                index1 = self.ingredients_model.index(i, 0)
                index2 = self.ingredients_model.index(i, 1)
                ingredient = self.ingredients_model.data(index1)
                quantity = int(self.ingredients_model.data(index2))
                ingredients[ingredient] = quantity
            recipes.set_recipe(self.item_name, ingredients, quantity_produced)
        else:
            recipes.set_recipe(self.item_name)

        # Remove item from queue
        self.recipe_queue.pop(0)

        # Populate queue with possible new missing recipes
        if len(ingredients) > 0:
            for ingredient, quantity in ingredients.items():
                self.recipe_queue = util.merge_lists(recipes.get_missing_recipes(ingredient), self.recipe_queue)

        # Refresh the gui
        if len(self.recipe_queue) > 0:
            self.next_recipe()
        else:
            self.close()
