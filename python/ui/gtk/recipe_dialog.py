from gi.repository import Gtk
from gi.repository import Gdk

import recipes

class RecipeDialog(Gtk.Dialog):
    def __init__(self, item_name, parent):
        super(RecipeDialog, self).__init__(title="Recipe Input", parent=parent)

        #self.set_default_size(370, 320)

        self.set_modal(True)
        self.title_label_format = "Please tell me how to make \"{}\""

        box = self.get_content_area()
        box.set_spacing(6)
        box.set_margin_top(6)
        box.set_margin_right(6)
        #box.set_margin_bottom(6)
        box.set_margin_left(6)

        self.title_label = Gtk.Label()
        self.title_label.set_halign(Gtk.Align.START)
        box.pack_start(self.title_label, False, False, 0)

        ingredients_frame = Gtk.Frame(label="Ingredients")
        ingredients_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        ingredients_box.set_hexpand(True)
        ingredients_box.set_margin_top(6)
        ingredients_box.set_margin_right(6)
        ingredients_box.set_margin_bottom(6)
        ingredients_box.set_margin_left(6)
        ingredients_frame.add(ingredients_box)

        ingredients_input_box = Gtk.Box(spacing=6)

        item_name_label = Gtk.Label(label="Item Name")
        ingredients_input_box.pack_start(item_name_label, False, False, 0)

        self.item_name_entry = Gtk.Entry()
        self.item_name_entry.set_hexpand(True)
        self.item_name_entry.set_activates_default(True)
        self.item_name_entry.connect("changed", self.item_name_entry_changed)
        self.item_name_entry.connect("focus", self.ingredients_focus)
        ingredients_input_box.pack_start(self.item_name_entry, True, True, 0)

        quantity_label = Gtk.Label(label="Quantity")
        ingredients_input_box.pack_start(quantity_label, False, False, 0)

        quantity_adjustment = Gtk.Adjustment(value=1, lower=1, upper=100000, step_increment=1)
        self.quantity_spin_button = Gtk.SpinButton(adjustment=quantity_adjustment, numeric=True)
        self.quantity_spin_button.set_activates_default(True)
        self.quantity_spin_button.connect("focus", self.ingredients_focus)
        ingredients_input_box.pack_start(self.quantity_spin_button, False, False, 0)

        ingredients_box.pack_start(ingredients_input_box, False, False, 0)

        ingredients_button_box = Gtk.Box(spacing=6)
        self.add_button = Gtk.Button(label="Add")
        self.add_button.set_sensitive(False)
        self.add_button.set_can_default(True)
        self.add_button.connect("clicked", self.add_button_clicked)
        ingredients_button_box.pack_start(self.add_button, True, True, 0)
        self.remove_button = Gtk.Button(label="Remove")
        self.remove_button.set_sensitive(False)
        ingredients_button_box.pack_start(self.remove_button, True, True, 0)
        ingredients_box.pack_start(ingredients_button_box, False, False, 0)

        ingredients_scroll = Gtk.ScrolledWindow()

        self.ingredients_store = Gtk.ListStore(str, int)
        ingredients_tree_view = Gtk.TreeView(self.ingredients_store)
        column = Gtk.TreeViewColumn("Item Name", Gtk.CellRendererText(), text=0)
        column.set_expand(True)
        ingredients_tree_view.append_column(column)
        column = Gtk.TreeViewColumn("Quantity", Gtk.CellRendererText(), text=1)
        column.set_expand(False)
        ingredients_tree_view.append_column(column)
        ingredients_selection = ingredients_tree_view.get_selection()
        ingredients_selection.connect("changed", self.ingredients_selection_changed)

        ingredients_scroll.add(ingredients_tree_view)
        ingredients_box.pack_start(ingredients_scroll, True, True, 0)

        box.pack_start(ingredients_frame, True, True, 0)

        bottom_controls_box = Gtk.Box(spacing=6)

        quantity_produced_label = Gtk.Label("Quantity Produced")
        bottom_controls_box.pack_start(quantity_produced_label, False, False, 0)

        quantity_produced_adjustment = Gtk.Adjustment(value=1, lower=1, upper=100000, step_increment=1)
        self.quantity_produced_spin_button = Gtk.SpinButton(adjustment=quantity_produced_adjustment, numeric=True)
        self.quantity_produced_spin_button.set_sensitive(False)
        bottom_controls_box.pack_start(self.quantity_produced_spin_button, False, False, 0)

        self.done_button = Gtk.Button(label="Raw Material")
        self.done_button.get_style_context().add_class("suggested-action")
        bottom_controls_box.pack_end(self.done_button, False, False, 0)

        box.pack_start(bottom_controls_box, False, False, 0)

        self.recipe_queue = recipes.get_missing_recipes(item_name)
        self.next_recipe()

    def next_recipe(self):
        self.item_name = self.recipe_queue[0]
        self.title_label.set_label(self.title_label_format.format(self.item_name))
        self.item_name_entry.set_text("")
        self.quantity_spin_button.set_value(1)
        self.quantity_produced_spin_button.set_value(1)
        self.done_button.set_label("Raw Material")
        #TODO: Clear tree

    def item_name_entry_changed(self, editable):
        text = self.item_name_entry.get_text()
        if len(text) > 0 and text != self.item_name:
            self.add_button.set_sensitive(True)
            self.add_button.grab_default()
        else:
            self.add_button.set_sensitive(False)

    def ingredients_selection_changed(self, selection):
        pass

    def add_button_clicked(self, btn):
        ingredient_name = self.item_name_entry.get_text()
        quantity = self.quantity_spin_button.get_value()

        self.ingredients_store.append((ingredient_name, quantity))
        self.item_name_entry.set_text("")
        self.quantity_spin_button.set_value(1)
        self.add_button.set_sensitive(False)

        self.quantity_produced_spin_button.set_sensitive(True)
        self.done_button.set_label("Done")

        self.item_name_entry.grab_focus()
