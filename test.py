#!/usr/bin/env python3
import gi, os, signal
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator

APPINDICATOR_ID = 'myappindicator'

def build_menu():
    menu = gtk.Menu()
    item_quit = gtk.MenuItem(label='Quit')
    item_quit.connect('activate', lambda _: gtk.main_quit())
    menu.append(item_quit)
    menu.show_all()
    return menu

def main():
    icon = os.path.abspath('bird_2.png')  # or use a theme name
    indicator = appindicator.Indicator.new(
        APPINDICATOR_ID, icon, appindicator.IndicatorCategory.SYSTEM_SERVICES
    )
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_icon(icon)
    indicator.set_menu(build_menu())

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    gtk.main()

if __name__ == "__main__":
    main()
