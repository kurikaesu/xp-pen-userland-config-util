import json
import os
import signal

import gi
import psutil
from gi.repository import Gtk

from .artist_22r_pro import Artist22RPro
from .artist_13_3_pro import Artist133Pro
from .artist_24_pro import Artist24Pro
from .artist_12_pro import Artist12Pro
from .deco_pro_sm import DecoProSmall
from .deco_pro_md import DecoProMedium

gi.require_version("Gtk", "3.0")


class ConfigurationWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Configuration")
        self.default_padding_px = 10
        self.current_showing_config = None

        self.vert_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.vert_box)

        self.commit_config_btn = Gtk.Button(label="Update Configuration")
        self.commit_config_btn.connect("clicked", self.on_commit_configuration)
        self.vert_box.pack_end(self.commit_config_btn, True, True, self.default_padding_px)

        self.print_config = Gtk.Button(label="Print Configuration")
        self.print_config.connect("clicked", self.on_print_configuration)
        self.vert_box.pack_end(self.print_config, True, True, self.default_padding_px / 2)

        self.jsonConfig = None

        self.parse_current_config()
        self.handlers = {"XP-Pen": {}}
        a22r_pro_handler = Artist22RPro()
        self.handlers["XP-Pen"][a22r_pro_handler.product_id()] = a22r_pro_handler
        a133_pro_handler = Artist133Pro()
        self.handlers["XP-Pen"][a133_pro_handler.product_id()] = a133_pro_handler
        a24_pro_handler = Artist24Pro()
        self.handlers["XP-Pen"][a24_pro_handler.product_id()] = a24_pro_handler
        a12_pro_handler = Artist12Pro()
        self.handlers["XP-Pen"][a12_pro_handler.product_id()] = a12_pro_handler
        deco_pro_sm_handler = DecoProSmall()
        self.handlers["XP-Pen"][deco_pro_sm_handler.product_id()] = deco_pro_sm_handler
        deco_pro_md_handler = DecoProMedium()
        self.handlers["XP-Pen"][deco_pro_md_handler.product_id()] = deco_pro_md_handler

        devices_label = Gtk.Label(label="Device: ")
        self.combo_label_box = Gtk.Box(spacing=6)
        self.combo_label_box.pack_start(devices_label, False, False, self.default_padding_px)

        config_dropbox_data = Gtk.ListStore(object, str)

        for vendor in self.jsonConfig:
            if vendor in self.handlers:
                for product in self.handlers[vendor]:
                    if product in self.jsonConfig[vendor]:
                        config_dropbox_data.append([self.handlers[vendor][product], self.handlers[vendor][product].product_name()])

        self.config_dropbox = Gtk.ComboBox.new_with_model_and_entry(config_dropbox_data)
        self.config_dropbox.set_entry_text_column(1)
        self.config_dropbox.connect("changed", self.on_config_changed)
        self.combo_label_box.pack_start(self.config_dropbox, True, True, self.default_padding_px)
        self.vert_box.pack_start(self.combo_label_box, False, False, self.default_padding_px)

    def on_config_changed(self, widget):
        tree_iter = widget.get_active_iter()
        if tree_iter is not None:
            model = widget.get_model()
            generator, name = model[tree_iter][:2]
            if self.current_showing_config is not None:
                self.current_showing_config.destroy()

            self.current_showing_config = generator.generate_layout(self.jsonConfig, self.vert_box)

        self.resize(1, 1)

    def parse_current_config(self):
        config_file = open("%s/.local/share/xp_pen_userland/driver.cfg" % os.getenv('HOME'), )
        self.jsonConfig = json.load(config_file)
        config_file.close()
        print(self.jsonConfig)

    def on_commit_configuration(self, widget):
        print("Committing config")
        config_file = open("%s/.local/share/xp_pen_userland/driver.cfg" % os.getenv('HOME'), 'w')
        json.dump(self.jsonConfig, config_file)
        config_file.close()
        process_ids = [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if
                       'xp_pen_userland' in p.info['name']]
        if len(process_ids) != 1:
            print("Could not find userland driver")
            return

        os.kill(process_ids[0]['pid'], signal.SIGHUP)

    def on_print_configuration(self, widget):
        print(self.jsonConfig)
