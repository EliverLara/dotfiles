import random
from gi.repository import Gtk
import terminatorlib.plugin as plugin
from terminatorlib.config import Config
AVAILABLE = ['RandProfile']

class RandProfile(plugin.Plugin):
    capabilities = ['terminal_menu']

    def change_profile(self):
        newTheme = self.profiles[2]
        self.terminal.force_set_profile(newTheme)

    def callback(self, menuitems, menu, terminal):
        self.config = Config()
        self.terminal = terminal
        self.profiles = self.terminal.config.list_profiles()
        target = random.randrange(0, len(self.profiles))
        currentProfile = self.profiles[target]
        widget = self.terminal.get_vte()
        self.terminal.force_set_profile(widget, currentProfile)
        # item = Gtk.ImageMenuItem(Gtk.STOCK_FIND)
        # item.connect('activate', terminal.force_set_profile, currentProfile)
        # item.set_label('Random Profile')
        # item.set_sensitive(True)
        # menuitems.append(item)

