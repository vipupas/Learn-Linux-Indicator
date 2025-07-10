#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk, AppIndicator3, GObject, Notify
import threading
import time
import requests
import json
import os

class ESP32Indicator:
    def __init__(self):
        self.esp32_ip = "192.168.197.75"  # Change this to your ESP32 IP
        self.update_interval = 1 # seconds
        
        # Initialize notification
        Notify.init("ESP32 BMP180 Monitor")
        
        # Create indicator
        self.indicator = AppIndicator3.Indicator.new(
            "esp32-bmp180-indicator",
            "weather-few-clouds",  # Default icon
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        
        # Initialize data
        self.temperature = "N/A"
        self.pressure = "N/A"
        self.altitude = "N/A"
        self.last_update = "Never"
        self.connection_status = "Disconnected"
        
        # Start data fetching thread
        self.running = True
        self.update_thread = threading.Thread(target=self.update_data_loop)
        self.update_thread.daemon = True
        self.update_thread.start()
        
        # Initial data fetch
        self.fetch_data()
    
    def create_menu(self):
        menu = Gtk.Menu()
        
        # Temperature item
        self.temp_item = Gtk.MenuItem(label="Temperature: N/A")
        self.temp_item.set_sensitive(False)
        menu.append(self.temp_item)
        
        # Pressure item
        self.pressure_item = Gtk.MenuItem(label="Pressure: N/A")
        self.pressure_item.set_sensitive(False)
        menu.append(self.pressure_item)
        
        # Altitude item
        self.altitude_item = Gtk.MenuItem(label="Altitude: N/A")
        self.altitude_item.set_sensitive(False)
        menu.append(self.altitude_item)
        
        # Separator
        menu.append(Gtk.SeparatorMenuItem())
        
        # Status item
        self.status_item = Gtk.MenuItem(label="Status: Disconnected")
        self.status_item.set_sensitive(False)
        menu.append(self.status_item)
        
        # Last update item
        self.update_item = Gtk.MenuItem(label="Last Update: Never")
        self.update_item.set_sensitive(False)
        menu.append(self.update_item)
        
        # Separator
        menu.append(Gtk.SeparatorMenuItem())
        
        # Refresh item
        refresh_item = Gtk.MenuItem(label="Refresh Now")
        refresh_item.connect("activate", self.refresh_data)
        menu.append(refresh_item)
        
        # Settings item
        settings_item = Gtk.MenuItem(label="Settings")
        settings_item.connect("activate", self.show_settings)
        menu.append(settings_item)
        
        # Separator
        menu.append(Gtk.SeparatorMenuItem())
        
        # Quit item
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.quit_application)
        menu.append(quit_item)
        
        menu.show_all()
        return menu
    
    def fetch_data(self):
        try:
            response = requests.get(f"http://{self.esp32_ip}/data", timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                self.temperature = f"{data['temperature']:.1f}°C"
                self.pressure = f"{data['pressure']:.1f} hPa"
                self.altitude = f"{data['altitude']:.1f} m"
                self.connection_status = "Connected"
                self.last_update = time.strftime("%H:%M:%S")
                
                # Update indicator label
                self.indicator.set_label(f"{self.temperature}", "")
                
                # Update menu items
                GObject.idle_add(self.update_menu_items)
                
                return True
            else:
                self.connection_status = "HTTP Error"
                GObject.idle_add(self.update_menu_items)
                return False
                
        except requests.exceptions.RequestException as e:
            self.connection_status = "Connection Failed"
            GObject.idle_add(self.update_menu_items)
            return False
    
    def update_menu_items(self):
        self.temp_item.set_label(f"Temperature: {self.temperature}")
        self.pressure_item.set_label(f"Pressure: {self.pressure}")
        self.altitude_item.set_label(f"Altitude: {self.altitude}")
        self.status_item.set_label(f"Status: {self.connection_status}")
        self.update_item.set_label(f"Last Update: {self.last_update}")
        
        # Update icon based on connection status
        if self.connection_status == "Connected":
            self.indicator.set_icon("weather-few-clouds")
        else:
            self.indicator.set_icon("weather-severe-alert")
    
    def update_data_loop(self):
        while self.running:
            self.fetch_data()
            time.sleep(self.update_interval)
    
    def refresh_data(self, widget):
        threading.Thread(target=self.fetch_data).start()
    
    def show_settings(self, widget):
        dialog = Gtk.Dialog(
            title="ESP32 BMP180 Settings",
            parent=None,
            flags=0,
            buttons=(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OK, Gtk.ResponseType.OK
            )
        )
        
        dialog.set_default_size(300, 150)
        
        # Content area
        content_area = dialog.get_content_area()
        
        # IP address input
        ip_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        ip_label = Gtk.Label(label="ESP32 IP:")
        ip_entry = Gtk.Entry()
        ip_entry.set_text(self.esp32_ip)
        ip_box.pack_start(ip_label, False, False, 0)
        ip_box.pack_start(ip_entry, True, True, 0)
        
        # Update interval input
        interval_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        interval_label = Gtk.Label(label="Update Interval (s):")
        interval_entry = Gtk.Entry()
        interval_entry.set_text(str(self.update_interval))
        interval_box.pack_start(interval_label, False, False, 0)
        interval_box.pack_start(interval_entry, True, True, 0)
        
        content_area.pack_start(ip_box, False, False, 10)
        content_area.pack_start(interval_box, False, False, 10)
        
        dialog.show_all()
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.esp32_ip = ip_entry.get_text()
            try:
                self.update_interval = int(interval_entry.get_text())
            except ValueError:
                pass
            
            # Send notification
            notification = Notify.Notification.new(
                "Settings Updated",
                f"ESP32 IP: {self.esp32_ip}\nUpdate Interval: {self.update_interval}s",
                "dialog-information"
            )
            notification.show()
        
        dialog.destroy()
    
    def quit_application(self, widget):
        self.running = False
        Notify.uninit()
        Gtk.main_quit()

def main():
    indicator = ESP32Indicator()
    
    # Handle Ctrl+C gracefully
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    try:
        Gtk.main()
    except KeyboardInterrupt:
        indicator.quit_application(None)

if __name__ == "__main__":
    main()