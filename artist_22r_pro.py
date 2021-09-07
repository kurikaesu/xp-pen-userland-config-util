import gi
import pynput
from gi.repository import Gtk

from pynput_to_scancode import from_scancode
from pynput_to_scancode import to_scancode


class Artist22RPro:
    def __init__(self):
        self.mapping = None
        self.content_hori_box = None
        self.left_vert_box = None
        self.right_vert_box = None
        self.default_padding_px = 5

    def product_id(self):
        return '2331'

    def generate_layout(self, json_config, container):
        self.mapping = json_config["XP-Pen"]["2331"]["mapping"]

        self.content_hori_box = Gtk.Box(spacing=6)
        self.left_vert_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.right_vert_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.content_hori_box.add(self.left_vert_box)
        self.content_hori_box.add(self.right_vert_box)
        container.pack_start(self.content_hori_box, True, True, self.default_padding_px)

        left_buttons_list = ['256', '257', '258', '259', '260', '261', '262', '263', '264', '265']
        counter = 0

        for button in left_buttons_list:
            entry_box = Gtk.Box(spacing=6)
            self.left_vert_box.add(entry_box)

            counter += 1
            entry_button = Gtk.Button(label="Button {}".format(counter))
            entry_text = Gtk.Entry()
            entry_button.entry_text = entry_text

            entry_button.connect("clicked", self.on_button_clicked)
            entry_box.pack_start(entry_button, True, True, self.default_padding_px)

            entry_text.set_editable(False)
            entry_text.user_data = button
            entry_text.set_text("+".join([str(from_scancode(c)) for c in self.mapping[button]]))
            entry_text.connect("changed", self.on_text_entry_changed)
            entry_box.pack_start(entry_text, True, True, self.default_padding_px)

        right_buttons_list = ['304', '305', '306', '307', '308', '309', '310', '311', '312', '313']
        for button in right_buttons_list:
            entry_box = Gtk.Box(spacing=6)
            self.right_vert_box.add(entry_box)

            counter += 1
            entry_button = Gtk.Button(label="Button {}".format(counter))
            entry_text = Gtk.Entry()
            entry_button.entry_text = entry_text

            entry_button.connect("clicked", self.on_button_clicked)
            entry_box.pack_start(entry_button, True, True, self.default_padding_px)

            entry_text.set_editable(False)
            entry_text.user_data = button
            entry_text.set_text("+".join([str(from_scancode(c)) for c in self.mapping[button]]))
            entry_text.connect("changed", self.on_text_entry_changed)
            entry_box.pack_start(entry_text, True, True, self.default_padding_px)

    def on_text_entry_changed(self, widget):
        widget_text = widget.get_text()
        user_data = [to_scancode(k) for k in widget_text.split('+')]
        print(user_data)
        self.mapping[widget.user_data] = user_data

    def on_button_clicked(self, widget):
        pressed_keys = {}
        keys_pressed = 0
        with pynput.keyboard.Events() as events:
            for event in events:
                if isinstance(event, pynput.keyboard.Events.Press):
                    if event.key not in pressed_keys:
                        pressed_keys[to_scancode(str(event.key).replace("'", ''))] = True
                        keys_pressed += 1
                elif isinstance(event, pynput.keyboard.Events.Release):
                    keys_pressed -= 1
                    if keys_pressed == 0:
                        break

        print(pressed_keys)
        widget.entry_text.set_text("+".join([str(from_scancode(c)) for c in pressed_keys.keys()]))
