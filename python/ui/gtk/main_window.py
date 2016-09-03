from gi.repository import Gtk, Gio

import recipes
import ui.gtk.new_craft_dialog

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self):
        super(MainWindow, self).__init__(title="Minecraft Resource Calculator")

        # Window properties
        self.set_wmclass("Minecraft Resource Calculator", "Minecraft Resource Calculator")
        self.set_default_size(476, 362)
        self.connect("delete-event", Gtk.main_quit)

        # Window actions
        action = Gio.SimpleAction.new("close", None)
        action.connect("activate", self.action_close)
        self.add_action(action)

        # Header Bar
        self.header = Gtk.HeaderBar(title="Minecraft Resource Calculator")
        self.header.set_show_close_button(True)

        # New craft header button
        header_button = Gtk.Button()
        header_button_icon = Gio.ThemedIcon(name="document-new-symbolic")
        header_button_image = Gtk.Image.new_from_gicon(header_button_icon, Gtk.IconSize.BUTTON)
        header_button.add(header_button_image)
        header_button.connect("clicked", self.new_craft_button_clicked)
        self.header.pack_start(header_button)

        # Header menu
        header_menu = Gio.Menu()
        header_menu.append("Edit recipe...", "win.edit_recipe")
        header_menu.append("Close", "win.close")

        # Header menu button
        header_button = Gtk.MenuButton()
        header_button.set_popover(Gtk.Popover.new_from_model(header_button, header_menu))
        header_button_icon = Gio.ThemedIcon(name="open-menu-symbolic")
        header_button_image = Gtk.Image.new_from_gicon(header_button_icon, Gtk.IconSize.BUTTON)
        header_button.add(header_button_image)
        self.header.pack_end(header_button)

        self.set_titlebar(self.header)

        # Root box layout
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(box)

        # Tree View

        steps_scroll = Gtk.ScrolledWindow()

        self.steps_store = Gtk.TreeStore(str, str)
        self.steps_tree_view = Gtk.TreeView(self.steps_store)
        column = Gtk.TreeViewColumn("Item Name", Gtk.CellRendererText(), text=0)
        column.set_expand(True)
        self.steps_tree_view.append_column(column)
        column = Gtk.TreeViewColumn("Quantity", Gtk.CellRendererText(), text=1)
        column.set_expand(False)
        self.steps_tree_view.append_column(column)

        steps_scroll.add(self.steps_tree_view)
        box.pack_start(steps_scroll, True, True, 0)

    def set_craft_item(self, item_name, quantity):
        self.header.set_subtitle("{} x{}".format(item_name, quantity))

        self.steps_store.clear()

        required_items, excess = recipes.craft(item_name, quantity, [], {})
        steps = recipes.organize_items_to_steps(required_items)

        for s in range(0, len(steps)):
            step = steps[s]
            step_name = None
            if s == 0:
                step_name = "Raw Materials"
            else:
                step_name = "Crafting Step {}".format(s)

            step_item = self.steps_store.append(None, [step_name, None])

            for material, material_quantity in step.items():
                material_item = self.steps_store.append(step_item, [material, str(material_quantity)])

                if s != 0:
                    ingredients, craft_excess = recipes.craft(material, material_quantity, [], {}, 0, True)
                    for ingredient, ingredient_quantity in ingredients[1].items():
                        self.steps_store.append(material_item, [ingredient, str(ingredient_quantity)])

            self.steps_tree_view.expand_row(Gtk.TreePath.new_from_indices([s]), False)

    def new_craft_button_clicked(self, btn):
        new_craft_dialog = ui.gtk.new_craft_dialog.NewCraftDialog(self)
        new_craft_dialog.show_all()

    def action_close(self, action, param):
        self.close()
