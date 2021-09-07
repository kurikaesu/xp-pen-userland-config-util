import json
import os
import signal

import gi
import psutil
from gi.repository import Gtk

from artist_22r_pro import Artist22RPro

gi.require_version("Gtk", "3.0")


class ConfigurationWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Configuration")
        self.default_padding_px = 10

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
        self.artist_22r_pro = Artist22RPro()

        if "XP-Pen" in self.jsonConfig:
            if "2331" in self.jsonConfig["XP-Pen"]:
                self.artist_22r_pro.generate_layout(self.jsonConfig, self.vert_box)

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
