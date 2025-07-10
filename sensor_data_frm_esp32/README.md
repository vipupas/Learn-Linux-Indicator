# ESP32 BMP180 Ubuntu System Tray Indicator

## Hardware Requirements

- **ESP-WROOM-32**(Microcontroller)
- **BMP180**(Temperature , Altitude , Pressure Module)

## Software Requirements

- **Arduino IDE**(with "ESP32 Dev Model" as board  manager)
- **Python3**

## Hardware Setup

### ESP32 + BMP180 Wiring:
- **VCC** → 3.3V
- **GND** → GND  
- **SDA** → GPIO 21
- **SCL** → GPIO 22

## Software Setup

### 1. ESP32 Setup

1. Install required libraries in Arduino IDE:
   - `WiFi` (built-in)
   - `WebServer` (built-in)
   - `ArduinoJson` (by Benoit Blanchon)
   - `Adafruit BMP085 Library` (by Adafruit)

2. Update the ESP32 code:
   - Replace `YOUR_WIFI_SSID` and `YOUR_WIFI_PASSWORD` with your WiFi credentials
   - Upload the code to your ESP32
   - Note the IP address shown in Serial Monitor

### 2. Ubuntu System Tray Setup

1. Install required system packages:
```bash
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1 gir1.2-notify-0.7
```

2. Install Python dependencies:
```bash
pip3 install requests
```

3. Make the Python script executable:
```bash
chmod +x esp32_indicator.py
```

4. Update the ESP32 IP address in the Python script:
   - Edit `esp32_indicator.py`
   - Change `self.esp32_ip = "192.168.1.100"` to your ESP32's IP address

### 3. Running the Application

#### Manual Run:
```bash
python3 esp32_indicator.py
```

#### Auto-start on Login:
1. Create a desktop entry:
```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/esp32-indicator.desktop << EOF
[Desktop Entry]
Type=Application
Name=ESP32 BMP180 Indicator
Exec=python3 /path/to/your/esp32_indicator.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF
```

2. Replace `/path/to/your/esp32_indicator.py` with the actual path to your script.

## Features

- **Real-time Data**: Shows temperature, pressure, and altitude
- **System Tray Integration**: Displays current temperature in the system tray
- **Auto-refresh**: Updates data every 30 seconds (configurable)
- **Manual Refresh**: Right-click menu option to refresh immediately
- **Settings Dialog**: Configure ESP32 IP and update interval
- **Connection Status**: Visual indicators for connection state
- **Notifications**: Desktop notifications for settings changes

## Usage

1. The indicator will appear in your system tray showing the current temperature
2. Right-click the indicator to access the menu with:
   - Current sensor readings
   - Connection status
   - Last update time
   - Refresh option
   - Settings
   - Quit option

## Troubleshooting

### ESP32 Issues:
- Check serial monitor for IP address
- Verify WiFi connection
- Test web interface by visiting `http://ESP32_IP/` in browser

### Ubuntu Indicator Issues:
- Ensure all system packages are installed
- Check that AppIndicator3 is available in your desktop environment
- For GNOME, you may need to install the TopIcons Plus extension

### Connection Issues:
- Verify ESP32 IP address is correct
- Check that both devices are on the same network
- Test connectivity with: `ping ESP32_IP`
- Try accessing `http://ESP32_IP/data` in browser

## Customization

- **Update Interval**: Change via settings dialog or modify `self.update_interval`
- **Icons**: Modify icon names in the code (uses system theme icons)
- **Data Format**: Customize display format in `update_menu_items()` method
- **Notifications**: Add more notification triggers as needed
