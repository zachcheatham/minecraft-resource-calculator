from PyQt5.QtCore import Qt, QItemSelectionModel, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QHeaderView

import recipes
from ui.qt.designer.recipe_list_dialog import Ui_recipeListDialog
from ui.qt.recipe_dialog import RecipeDialog


class RecipeListDialog(QDialog, Ui_recipeListDialog):
    def __init__(self, parent=None):
        super(RecipeListDialog, self).__init__(parent)

        self.previously_selected = None
        self.recipes_version = -1

        self.setWindowFlags(self.windowFlags() & (~Qt.WindowContextHelpButtonHint))
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)

        self.searchTextBox.textEdited.connect(self.search_changed)
        self.editButton.clicked.connect(self.edit_button_clicked)
        self.deleteButton.clicked.connect(self.delete_button_clicked)

        self.model = QStandardItemModel()
        self.filter_model = QSortFilterProxyModel()
        self.filter_model.setSourceModel(self.model)
        self.filter_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.model.setHorizontalHeaderLabels(["", ""])
        self.recipesList.setAllColumnsShowFocus(True)
        self.recipesList.setExpandsOnDoubleClick(False)
        self.recipesList.setRootIsDecorated(False)
        self.recipesList.setSortingEnabled(False)
        self.recipesList.setHeaderHidden(True)
        self.recipesList.setModel(self.filter_model)
        self.recipesList.selectionModel().selectionChanged.connect(self.selection_changed)
        self.recipesList.activated.connect(self.edit_item)
        header = self.recipesList.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.refresh_list()

    def refresh_list(self):
        reselect_index = None

        for i in range(0, self.model.rowCount()):
            self.model.takeRow(0)

        for item, data in sorted(recipes.recipes.items()):
            item_name = QStandardItem(item)
            item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)

            if data is None:
                raw_material = QStandardItem("Raw")
            else:
                raw_material = QStandardItem("")
            raw_material.setFlags(raw_material.flags() & ~Qt.ItemIsEditable)

            self.model.appendRow([item_name, raw_material])

            if item == self.previously_selected:
                reselect_index = self.model.rowCount() - 1

        if reselect_index is not None:
            index = self.model.index(reselect_index, 0)
            self.recipesList.selectionModel().select(index, QItemSelectionModel.Rows | QItemSelectionModel.Select | QItemSelectionModel.Current)
            self.recipesList.scrollTo(index)

        self.recipes_version = recipes.get_last_edit()
        self.previously_selected = None

    def selection_changed(self):
        self.editButton.setEnabled(True)
        self.deleteButton.setEnabled(True)

    def delete_button_clicked(self):
        row = self.recipesList.selectedIndexes()[0].row()
        index = self.model.index(row, 0)
        recipes.remove_recipe(self.model.data(index))
        self.recipes_version = recipes.get_last_edit()

        self.model.takeRow(row)
        if self.model.rowCount() == 0:
            self.editButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def edit_button_clicked(self):
        self.edit_item(self.recipesList.selectedIndexes()[0])

    def edit_item(self, index):
        name_index = self.filter_model.index(index.row(), 0)
        item_name = self.filter_model.data(name_index)
        self.previously_selected = item_name

        recipe_dialog = RecipeDialog(item_name, self, True)
        recipe_dialog.finished.connect(self.recipe_dialog_finished)
        recipe_dialog.show()

    def search_changed(self, text):
        self.filter_model.setFilterFixedString(text)

    def recipe_dialog_finished(self):
        if self.recipes_version != recipes.get_last_edit():
            self.refresh_list()
