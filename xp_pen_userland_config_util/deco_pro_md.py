import gi
import pynput
from gi.repository import Gtk

from .pynput_to_scancode import from_scancode
from .pynput_to_scancode import to_scancode


class DecoProMedium:
    def __init__(self):
        self.mapping = None
        self.content_hori_box = None
        self.content_vert_box = None
        self.default_padding_px = 5

    def product_id(self):
        return '2308'

    def product_name(self):
        return "XP-Pen Deco Pro Medium"

    def generate_layout(self, json_config, container):
        self.mapping = json_config["XP-Pen"][self.product_id()]["mapping"]

        self.content_hori_box = Gtk.Box(spacing=6)
        self.content_vert_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.content_hori_box.add(self.content_vert_box)
        container.pack_start(self.content_hori_box, True, True, self.default_padding_px)

        buttons_list = ['256', '257', '258', '259', '260', '261', '262', '263']
        counter = 0

        for button in buttons_list:
            counter += 1
            entry_text = "+".join([str(from_scancode(c)) for c in self.mapping["buttons"][button]["1"]])
            self.create_button_and_entry_in_box(self.content_vert_box, "Button {}".format(counter), button, entry_text,
                                                self.on_text_entry_changed)

        entry_text = "+".join([str(from_scancode(c)) for c in self.mapping["dials"]['8']['-1']['1']])
        self.create_button_and_entry_in_box(self.content_vert_box, "Dial => Left", ['8', '-1'], entry_text, self.on_dial_entry_changed)

        entry_text = "+".join([str(from_scancode(c)) for c in self.mapping["dials"]['8']['1']['1']])
        self.create_button_and_entry_in_box(self.content_vert_box, "Dial => Right", ['8', '1'], entry_text,
                                            self.on_dial_entry_changed)

        entry_text = "+".join([str(from_scancode(c)) for c in self.mapping["dials"]['8']['-1']['1']])
        self.create_button_and_entry_in_box(self.content_vert_box, "Touchpad => Rotate Left", ['6', '-1'], entry_text,
                                            self.on_dial_entry_changed)

        entry_text = "+".join([str(from_scancode(c)) for c in self.mapping["dials"]['8']['1']['1']])
        self.create_button_and_entry_in_box(self.content_vert_box, "Touchpad => Rotate Right", ['6', '1'], entry_text,
                                            self.on_dial_entry_changed)

        self.content_hori_box.show_all()
        return self.content_hori_box

    def create_button_and_entry_in_box(self, parent, buttonName, userdata, entrytext, textchanged):
        entry_box = Gtk.Box(spacing=6)
        parent.add(entry_box)

        entry_button = Gtk.Button(label=buttonName)
        entry_text = Gtk.Entry()
        entry_button.entry_text = entry_text

        entry_button.connect("clicked", self.on_button_clicked)
        entry_box.pack_start(entry_button, True, True, self.default_padding_px)

        entry_text.set_editable(False)
        entry_text.user_data = userdata
        entry_text.set_text(entrytext)
        entry_text.connect("changed", textchanged)
        entry_box.pack_start(entry_text, True, True, self.default_padding_px)
        return entry_box

    def on_text_entry_changed(self, widget):
        widget_text = widget.get_text()
        user_data = [to_scancode(k) for k in widget_text.split('+')]
        print(user_data)
        self.mapping["buttons"][widget.user_data] = {"1": user_data}

    def on_dial_entry_changed(self, widget):
        widget_text = widget.get_text()
        user_data = [to_scancode(k) for k in widget_text.split('+')]
        print(user_data)
        self.mapping["dials"][widget.user_data[0]][widget.user_data[1]] = {"1": user_data}

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