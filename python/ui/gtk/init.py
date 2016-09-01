import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from ui.gtk.new_craft_dialog import NewCraftDialog

def show_initial_window():
    window = NewCraftDialog()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()

def start_application():
    show_initial_window()
    Gtk.main()
