import requests
import terminatorlib.plugin as plugin
from gi.repository import Gtk, Gdk
from terminatorlib.config import ConfigBase
from terminatorlib.translation import _
from terminatorlib.util import get_config_dir, err, dbg, gerr

AVAILABLE = ['Lara']
   

class Lara(plugin.Plugin):

    capabilities = ['terminal_menu']
    config_base = ConfigBase()
    selected_theme = "Some" #selected theme data
    selected_theme_label = "Some"
    previous_selected_theme_label = Gtk.Label("Some")
    colors = {
        "available": "#3f953a",
        "installed": "#DE4D60",
        "selected" : "#fc2"
    }
    def callback(self, menuitems, menu, terminal):
        """Add our item to the menu"""
        self.terminal = terminal
        item = Gtk.ImageMenuItem(Gtk.STOCK_FIND)
        item.connect('activate', self.configure)
        item.set_label("Lara")
        item.set_sensitive(True)
        menuitems.append(item)

    def configure(self, widget, data = None):
       
        ui = {}

        win = Gtk.Window()
        win.set_border_width(10)
        win.set_default_size(700, 400)

        win.set_titlebar(self.make_headerbar(ui))

        # Fill thmmes containers
        self.profiles = self.terminal.config.list_profiles()

        response = requests.get("https://git.io/fxtUa")

        if response.status_code != 200:
            gerr(_("Failed to get list of available themes"))
            return

        dark_themes = self.make_themes_container(ui, filter(lambda x: x['type'] == 'dark', response.json()["themes"]))
        light_themes = self.make_themes_container(ui, filter(lambda x: x['type'] == 'light', response.json()["themes"]))
       
        main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        main_container.set_homogeneous(False)
        win.add(main_container)

        ui["stack"].add_titled(dark_themes, "check", "Dark themes")
        ui["stack"].add_titled(light_themes, "label", "Light themes")

        # Box to center stack horizontally
      

        # searchContainer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.CENTER)
        # search_entry = Gtk.SearchEntry(max_width_chars=45)
        # search_entry.connect("search-changed", self.on_search_changed, ui)
        # search_entry.show()
        # searchContainer.add(search_entry)
        # ui["search_entry"] = search_entry

        # for i in range(220):

        #     main_container.pack_start(Gtk.Button("test"), True, True, 1)
      
       # main_container.pack_start(searchContainer, False, False, 1)
        main_container.pack_start(ui["stack"], True, True, 1)

        win.show_all()

    def make_headerbar(self, ui):
        
        header = Gtk.HeaderBar()
        header.props.show_close_button = True
       # header.set_subtitle(self.selected_theme_label)
        button_install = Gtk.Button(_("Install"))
        button_uninstall = Gtk.Button(_("Remove"))
        button_install.set_sensitive(False)
        button_uninstall.set_sensitive(False)
        button_uninstall.connect("clicked", self.on_uninstall, ui) 
        button_install.connect("clicked", self.on_install, ui) 

        ui["button_install"] = button_install
        ui["button_uninstall"] = button_uninstall

        header.pack_end(button_install)
        header.pack_end(button_uninstall)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(500)
        stack.set_hhomogeneous(True)    

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        stackBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        stackBox.set_homogeneous(False)
        stackBox.pack_start(stack_switcher, True, False, 0)

        header.set_custom_title(stackBox)
        
        ui["header"] = header
        ui["stack"] = stack
        return header

    def make_themes_container(self, ui, themes):
      
        themes_scrolled = Gtk.ScrolledWindow()
        themes_scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        themes_flowbox = Gtk.FlowBox()
        themes_flowbox.set_valign(Gtk.Align.START)
        
        themes_flowbox.set_min_children_per_line(3)
        themes_flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        themes_scrolled.add(themes_flowbox)

        for theme in themes:
            card = self.create_theme_card(theme, ui)   
            themes_flowbox.add(card)

        return themes_scrolled


    def on_search_changed(self, widget, ui):
        print ui["search_entry"].get_text()
        ui["items_container"].set_filter_func(self.filter_themes, ui["search_entry"].get_text())

    def filter_themes(self, widget, target):
       # self.dump(widget)
        # if target == "la":
        #     return True
        # return False
        print widget.name


    def on_uninstall(self, button, ui):
 
        target = self.selected_theme["name"]

        # If selected theme is active, sets terminal profile to default before unistalling
        if self.terminal.get_profile() == target:
            widget = self.terminal.get_vte()
            self.terminal.force_set_profile(widget, 'default')

        self.terminal.config.del_profile(target)
        self.terminal.config.save()
        self.profiles = self.terminal.config.list_profiles()

        #'Install' button available again
        self.on_selection_changed(button, ui, self.selected_theme, self.selected_theme_label)

    def on_install(self, button, ui):
      
        target = self.selected_theme
        widget = self.terminal.get_vte()
        theme_name = target["name"]
        self.terminal.config.add_profile(theme_name) 
        for k, v in target.items():
            if k != 'background_image' and k != 'name' and k != 'type':
                self.config_base.set_item(k, v, theme_name)

        self.terminal.force_set_profile(widget, theme_name)
        self.terminal.config.save()
        self.profiles = self.terminal.config.list_profiles()
        # To change install/remove button state
        self.on_selection_changed(button, ui, self.selected_theme, self.selected_theme_label)

    
    def on_selection_changed(self, button, ui, theme, label):

        target = theme["name"]

        ui["header"].set_subtitle(target + " Selected")
        ui["button_uninstall"].set_sensitive(target in self.profiles)
        ui["button_install"].set_sensitive(target not in self.profiles)

        # Sets avaailability colors for the previous selected theme
        if  self.previous_selected_theme_label.get_text() not in self.profiles:
            self.previous_selected_theme_label.modify_fg(0, color = Gdk.color_parse(self.colors["available"])) 
        else:
            self.previous_selected_theme_label.modify_fg(0, color = Gdk.color_parse(self.colors["installed"])) 
            
        self.selected_theme = theme
        self.selected_theme_label = label

        # Check if some theme have been selected
        if self.selected_theme_label != "Some" :
            self.selected_theme_label.modify_fg(0, color = Gdk.color_parse(self.colors["selected"]))  
            self.previous_selected_theme_label = self.selected_theme_label  


    def create_theme_card(self, theme, ui):

        theme_card = Gtk.Button()
        label = Gtk.Label(theme["name"])
        grid = Gtk.VBox(spacing=2)
        
        theme_pallete = self.create_theme_palette(theme)

        grid.pack_start (theme_pallete, True, True,0)
        grid.pack_start (label, True,True,0)
    
        if theme["name"] in self.profiles:
            label.modify_fg(0, color = Gdk.color_parse(self.colors["installed"])) 
        else:
            label.modify_fg(0, color = Gdk.color_parse(self.colors["available"])) 
       
        theme_card.connect("clicked", self.on_selection_changed, ui, theme, label) 
        theme_card.add(grid)
        
        return theme_card


    def create_theme_palette(self, data):

        theme_pallete_grid = Gtk.VBox()

        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_min_children_per_line(4)
        flowbox.set_max_children_per_line(4)
        flowbox.set_selection_mode(Gtk.SelectionMode.NONE)

        area = Gtk.DrawingArea()
        area.set_size_request(170, 40)

        if data.has_key('background_color'):
            theme_pallete_grid.modify_bg(0, color = Gdk.color_parse(data['background_color'])) 
            
        for color in data['palette'].split(":")[0:8]:
            btn = Gtk.ColorButton()
            btn.set_color(color = Gdk.color_parse(color)) 
            flowbox.add(btn)

        theme_pallete_grid.pack_start (area, True, True,0)
        theme_pallete_grid.pack_start (flowbox, True,True,0)

        return theme_pallete_grid

