from gi.repository import Gtk, Gdk

import recipes
from ui.gtk.recipe_dialog import RecipeDialog
from ui.gtk.main_window import MainWindow

class NewCraftDialog(Gtk.Window):
    def __init__(self, parent=None):
        super(NewCraftDialog, self).__init__(title="New Craft Calculation")

        if parent != None:
            self.delete_event_handler = None
            #self.set_parent(parent)
            self.set_transient_for(parent)
            self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
            self.set_modal(True)
        else:
            self.delete_event_handler = self.connect("delete-event", Gtk.main_quit)

        self.set_wmclass("Minecraft Resource Calculator", "Minecraft Resource Calculator")
        self.set_default_size(350, -1)
        self.set_resizable(False)

        h_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        h_box.set_vexpand(True)
        h_box.set_hexpand(True)
        h_box.set_margin_top(6)
        h_box.set_margin_right(6)
        h_box.set_margin_bottom(6)
        h_box.set_margin_left(6)
        self.add(h_box)

        grid = Gtk.Grid()
        grid.set_vexpand(True)
        grid.set_hexpand(True)
        grid.set_row_spacing(6)
        grid.set_column_spacing(6)

        # Item Name
        item_name_label = Gtk.Label(label="Item Name")
        item_name_label.set_halign(Gtk.Align.END)
        grid.attach(item_name_label, 0, 0, 1, 1)
        self.item_name_entry = Gtk.Entry()
        self.item_name_entry.set_hexpand(True)
        self.item_name_entry.set_activates_default(True)
        self.item_name_entry.connect("changed", self.item_name_entry_changed)
        grid.attach(self.item_name_entry, 1, 0, 1, 1)

        # Quantity
        quantity_label = Gtk.Label(label="Quantity")
        quantity_label.set_halign(Gtk.Align.END)
        grid.attach(quantity_label, 0, 1, 1, 1)
        quantity_adjustment = Gtk.Adjustment(value=1, lower=1, upper=100000, step_increment=1)
        self.quantity_spin_button = Gtk.SpinButton(adjustment=quantity_adjustment, numeric=True)
        grid.attach(self.quantity_spin_button, 1, 1, 1, 1)

        h_box.pack_start(grid, True, True, 0)

        # Buttons
        button_box = Gtk.Box(spacing=6)
        self.calculate_button = Gtk.Button(label="Calculate")
        self.calculate_button.set_sensitive(False)
        self.calculate_button.set_can_default(True)
        self.calculate_button.get_style_context().add_class("suggested-action")
        self.calculate_button.connect("clicked", self.calculate_button_clicked)
        button_box.pack_start(self.calculate_button, True, True, 0)
        close_button = Gtk.Button(label="Close")
        close_button.connect("clicked", self.close_button_clicked)
        button_box.pack_end(close_button, True, True, 0)
        h_box.pack_end(button_box, False, False, 0)

    def open_craft(self):
        craft_window = self.get_transient_for()
        if craft_window == None:
            craft_window = MainWindow()
            craft_window.show_all()

        item_name = self.item_name_entry.get_text()
        quantity = int(self.quantity_spin_button.get_value())
        craft_window.set_craft_item(item_name, quantity)

        if self.delete_event_handler != None:
            self.disconnect(self.delete_event_handler)
        self.close()

    def item_name_entry_changed(self, editable):
        if len(self.item_name_entry.get_text()) > 0:
            self.calculate_button.set_sensitive(True)
            self.calculate_button.grab_default()
        else:
            self.calculate_button.set_sensitive(False)

    def calculate_button_clicked(self, button):
        item_name = self.item_name_entry.get_text()
        if recipes.have_missing(item_name):
            recipe_dialog = RecipeDialog(item_name, self)
            recipe_dialog.connect("hide", self.recipe_dialog_hide)
            recipe_dialog.show_all()
        else:
            self.open_craft()

    def close_button_clicked(self, button):
        self.close()

    def recipe_dialog_hide(self, widget):
        item_name = self.item_name_entry.get_text()
        if not recipes.have_missing(item_name):
            self.open_craft()
