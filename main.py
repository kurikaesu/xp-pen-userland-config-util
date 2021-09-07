import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from configuration_window import ConfigurationWindow

if __name__ == '__main__':
    win = ConfigurationWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
