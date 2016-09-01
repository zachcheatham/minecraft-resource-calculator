from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QHeaderView

import recipes
import ui.qt.new_craft_dialog
from ui.qt.designer.main_window import Ui_mainWindow

class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)

        self.steps_model = QStandardItemModel()
        self.steps_model.setHorizontalHeaderLabels(["Item Name", "Quantity"])

        self.stepsTreeView.setSortingEnabled(False)
        self.stepsTreeView.setHeaderHidden(False)
        self.stepsTreeView.setAlternatingRowColors(True)
        self.stepsTreeView.setModel(self.steps_model)

        header = self.stepsTreeView.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Interactive)

        self.actionNew_Craft.triggered.connect(self.action_new_craft)
        self.actionQuit.triggered.connect(self.action_quit)
        self.actionEditRecipe.triggered.connect(self.action_edit_recipe)
        self.actionExpand_All.triggered.connect(self.action_expand_all)
        self.actionAbout.triggered.connect(self.action_about)

    def set_craft_item(self, item_name, quantity):
        self.setWindowTitle("Minecraft Resource Calculator: {} x{}".format(item_name, quantity))

        for i in range(0, self.steps_model.rowCount()):
            self.steps_model.takeRow(0)

        required_items, excess = recipes.craft(item_name, quantity, [], {})
        steps = recipes.organize_items_to_steps(required_items)

        self.statusbar.showMessage("Crafting simulated in {} step(s).".format(len(steps) - 1))

        for s in range(0, len(steps)):
            step = steps[s]
            step_name = None
            if s == 0:
                step_name = "Raw Materials"
            else:
                step_name = "Crafting Step {}".format(s)

            step_item = QStandardItem(step_name)
            step_item.setFlags(step_item.flags() & ~Qt.ItemIsEditable)

            for material, material_quantity in step.items():
                material_item = QStandardItem(material)
                material_item.setFlags(material_item.flags() & ~Qt.ItemIsEditable)
                quantity_item = QStandardItem(str(material_quantity))
                quantity_item.setFlags(quantity_item.flags() & ~Qt.ItemIsEditable)
                step_item.appendRow([material_item, quantity_item])

                if recipes.get_recipe(material) != None:
                    ingredients, craft_excess = recipes.craft(material, material_quantity, [], {}, 0, True)
                    for ingredient, ingredient_quantity in ingredients[1].items():
                        ingredient_item = QStandardItem(ingredient)
                        ingredient_item.setFlags(ingredient_item.flags() & ~Qt.ItemIsEditable)
                        ingredient_quantiy_item = QStandardItem(str(ingredient_quantity))
                        ingredient_quantiy_item.setFlags(ingredient_quantiy_item.flags() & ~Qt.ItemIsEditable)
                        material_item.appendRow([ingredient_item, ingredient_quantiy_item])

            self.steps_model.appendRow(step_item)
            self.stepsTreeView.setExpanded(self.steps_model.indexFromItem(step_item), True)

        if len(excess) > 0:
            excess_item = QStandardItem("Excess Material")
            for material, material_quantity in excess.items():
                material_item = QStandardItem(material)
                quantity_item = QStandardItem(str(material_quantity))
                excess_item.appendRow([material_item, quantity_item])
            self.steps_model.appendRow(excess_item)

    def action_new_craft(self, checked):
        new_craft_dialog = ui.qt.new_craft_dialog.NewCraftDialog(self)
        new_craft_dialog.show()

    def action_quit(self, checked):
        self.close()

    def action_edit_recipe(self, checked):
        pass

    def action_expand_all(self, checked):
        self.stepsTreeView.expandAll()

    def action_about(self, checked):
        pass
