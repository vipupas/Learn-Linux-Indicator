#!/usr/bin/env python3
import gi
import signal
import psutil
import os

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk, AppIndicator3, GLib, Notify

class SystemMonitorIndicator:
    def __init__(self):
        # Initialize notifications
        Notify.init("System Monitor")
        
        # Create indicator
        self.indicator = AppIndicator3.Indicator.new(
            "system-monitor",
            "utilities-system-monitor",
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        
        # State variables
        self.cpu_threshold = 80
        self.memory_threshold = 80
        self.last_warning_time = 0
        
        # Create menu
        self.create_menu()
        
        # Start monitoring timer (update every 5 seconds)
        GLib.timeout_add_seconds(5, self.update_system_info)
    
    def create_menu(self):
        menu = Gtk.Menu()
        
        # System info display items
        self.cpu_item = Gtk.MenuItem(label='CPU: Loading...')
        self.cpu_item.set_sensitive(False)
        menu.append(self.cpu_item)
        
        self.memory_item = Gtk.MenuItem(label='Memory: Loading...')
        self.memory_item.set_sensitive(False)
        menu.append(self.memory_item)
        
        self.disk_item = Gtk.MenuItem(label='Disk: Loading...')
        self.disk_item.set_sensitive(False)
        menu.append(self.disk_item)
        
        menu.append(Gtk.SeparatorMenuItem())
        
        # Actions
        item_refresh = Gtk.MenuItem(label='Refresh Now')
        item_refresh.connect('activate', self.refresh_now)
        menu.append(item_refresh)
        
        item_open_monitor = Gtk.MenuItem(label='Open System Monitor')
        item_open_monitor.connect('activate', self.open_system_monitor)
        menu.append(item_open_monitor)
        
        menu.append(Gtk.SeparatorMenuItem())
        
        # Settings submenu
        settings_item = Gtk.MenuItem(label='Settings')
        settings_menu = Gtk.Menu()
        settings_item.set_submenu(settings_menu)
        
        # CPU threshold
        cpu_threshold_item = Gtk.MenuItem(label=f'CPU Warning at {self.cpu_threshold}%')
        cpu_threshold_item.connect('activate', self.set_cpu_threshold)
        settings_menu.append(cpu_threshold_item)
        
        # Memory threshold
        memory_threshold_item = Gtk.MenuItem(label=f'Memory Warning at {self.memory_threshold}%')
        memory_threshold_item.connect('activate', self.set_memory_threshold)
        settings_menu.append(memory_threshold_item)
        
        menu.append(settings_item)
        
        menu.append(Gtk.SeparatorMenuItem())
        
        # Quit
        item_quit = Gtk.MenuItem(label='Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)
        
        menu.show_all()
        self.indicator.set_menu(menu)
    
    def update_system_info(self):
        import time
        
        # Get system info
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        
        # Update menu items
        self.cpu_item.set_label(f'CPU: {cpu_percent:.1f}%')
        self.memory_item.set_label(f'Memory: {memory_percent:.1f}%')
        self.disk_item.set_label(f'Disk: {disk_percent:.1f}%')
        
        # Check for warnings (don't spam notifications)
        current_time = time.time()
        if current_time - self.last_warning_time > 300:  # 5 minutes
            if cpu_percent > self.cpu_threshold:
                self.show_warning(f"High CPU Usage: {cpu_percent:.1f}%")
                self.last_warning_time = current_time
            elif memory_percent > self.memory_threshold:
                self.show_warning(f"High Memory Usage: {memory_percent:.1f}%")
                self.last_warning_time = current_time
        
        # Keep the timer running
        return True
    
    def show_warning(self, message):
        notification = Notify.Notification.new(
            "System Warning",
            message,
            "dialog-warning"
        )
        notification.show()
    
    def refresh_now(self, widget):
        self.update_system_info()
    
    def open_system_monitor(self, widget):
        os.system("gnome-system-monitor &")
    
    def set_cpu_threshold(self, widget):
        # In a real app, you'd show a dialog here
        print("CPU threshold setting - implement dialog")
    
    def set_memory_threshold(self, widget):
        # In a real app, you'd show a dialog here
        print("Memory threshold setting - implement dialog")
    
    def quit(self, widget):
        Gtk.main_quit()

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    indicator = SystemMonitorIndicator()
    Gtk.main()

if __name__ == "__main__":
    main()