#!/usr/bin/env python3
import gi # This helps Python talk to the desktop parts
import os # This helps us find files, like our icon pictures
import signal # This helps our program stop nicely when we close it

# We need to tell 'gi' which versions of our building blocks we want to use.
# Gtk is for making menus and other visual parts.
gi.require_version('Gtk', '3.0')
# AyatanaAppIndicator is the special block for making the indicator icon.
gi.require_version('AyatanaAppIndicator3', '0.1')

# Now we get the actual building blocks and give them shorter names.
from gi.repository import Gtk as gtk, AyatanaAppIndicator3 as appindicator
from gi.repository import GLib # GLib helps us do things over time, like updating status

# This is the special name for our indicator. It must be unique!
APPINDICATOR_ID = 'my_status_indicator'

# This variable will hold our indicator so we can change its icon or text later.
# We make it 'None' for now, meaning it's empty.
my_indicator = None

# This variable will keep track of our current status (e.g., "happy", "sad").
current_status = "neutral"

# --- Functions: Our Special Recipes ---

# This recipe builds the menu that pops up when you click the indicator.
def build_menu():
    menu = gtk.Menu() # Start with an empty menu paper

    # --- Menu Item: Set Happy Status ---
    item_happy = gtk.MenuItem(label='Set Happy') # Create a button labeled 'Set Happy'
    # When this button is clicked, call our 'update_status' recipe with "happy".
    item_happy.connect('activate', lambda _: update_status("happy"))
    menu.append(item_happy) # Add the 'Set Happy' button to our menu

    # --- Menu Item: Set Sad Status ---
    item_sad = gtk.MenuItem(label='Set Sad') # Create a button labeled 'Set Sad'
    # When this button is clicked, call our 'update_status' recipe with "sad".
    item_sad.connect('activate', lambda _: update_status("sad"))
    menu.append(item_sad) # Add the 'Set Sad' button to our menu

    # --- Menu Item: Set Neutral Status ---
    item_neutral = gtk.MenuItem(label='Set Neutral') # Create a button labeled 'Set Neutral'
    # When this button is clicked, call our 'update_status' recipe with "neutral".
    item_neutral.connect('activate', lambda _: update_status("neutral"))
    menu.append(item_neutral) # Add the 'Set Neutral' button to our menu

    # --- Separator: A line to separate groups of items ---
    menu.append(gtk.SeparatorMenuItem()) # Add a thin line on the menu

    # --- Menu Item: Quit Application ---
    item_quit = gtk.MenuItem(label='Quit') # Create a button labeled 'Quit'
    # When this button is clicked, tell the computer to stop our program.
    item_quit.connect('activate', lambda _: gtk.main_quit())
    menu.append(item_quit) # Add the 'Quit' button to our menu

    menu.show_all() # Make sure all the buttons on our menu paper are visible
    return menu # Give back the finished menu

# This recipe updates the indicator's icon and text based on the new status.
def update_status(new_status):
    global my_indicator # We need to tell Python we are using the 'my_indicator' from outside this recipe.
    global current_status # And also 'current_status' from outside.

    current_status = new_status # Remember the new status

    icon_name = "" # This will hold the name of the icon picture
    label_text = "" # This will hold the words next to the icon

    # Decide which icon and text to use based on the status.
    if new_status == "happy":
        icon_name = "face-smile" # This is a common icon name already on your computer
        label_text = "Happy"
    elif new_status == "sad":
        icon_name = "face-sad" # Another common icon name
        label_text = "Sad"
    else: # If it's not happy or sad, it must be neutral
        icon_name = "face-neutral" # Another common icon name
        label_text = "Neutral"

    # Now, tell our indicator to change its picture and words!
    if my_indicator: # Only try to change if our indicator exists
        # Set the icon. We use a "theme name" which is a picture already known by Ubuntu.
        my_indicator.set_icon_full(icon_name, "Status: " + label_text)
        # Set the label (the words next to the icon).
        my_indicator.set_label(label_text, APPINDICATOR_ID)
        print(f"Status updated to: {label_text}") # Just to see a message in the terminal

# This is the main recipe that starts everything when our program runs.
def main():
    global my_indicator # Again, tell Python we are using the 'my_indicator' from outside.

    # Create our indicator! This is like putting our house on the top bar.
    # APPINDICATOR_ID: The unique name for our house.
    # "face-neutral": The starting picture for our house.
    # appindicator.IndicatorCategory.APPLICATION_STATUS: Tells Ubuntu what kind of house it is.
    my_indicator = appindicator.Indicator.new(
        APPINDICATOR_ID, "face-neutral", appindicator.IndicatorCategory.APPLICATION_STATUS
    )

    # Tell our indicator to be visible (active).
    my_indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

    # Connect our indicator to the menu we built earlier.
    # This is like connecting the secret door to the buttons inside.
    my_indicator.set_menu(build_menu())

    # Set the initial status when the program starts.
    update_status(current_status) # It will start as "neutral"

    # This helps our program close cleanly if you stop it from the terminal (Ctrl+C).
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # This is the most important line! It tells our program to "listen" for clicks
    # and other events, and keep running until we tell it to stop.
    gtk.main()

# This checks if our program is being run directly (not imported by another file).
if __name__ == "__main__":
    main() # If it is, start our main recipe!
