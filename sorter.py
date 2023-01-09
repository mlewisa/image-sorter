# written by chatGPT
# F = bad, J = good, left arrow = undo, esc = exit

import os
import shutil
import tkinter as tk
from PIL import Image, ImageTk
import natsort

# Set the path to the folder of images
path = "archive"

# Set the names of the target folders
good_folder = "good"
bad_folder = "bad"

# Get a list of all the image files in the folder
files = [f for f in os.listdir(path) if f.endswith(".jpg")]

# Sort the list of files in natural sort order
files = natsort.natsorted(files)

# Create lists to store moved images and target folders
undo_images = []
undo_folders = []

# Create the main window
root = tk.Tk()
root.title("Image Sorter")

# Set up the function that will be called when a key is pressed
def key_press(event):
    global files  # Declare the "files" variable as global
    # If the key pressed was "Esc"
    if event.keysym == "Escape":
        # Destroy the main window and exit the program
        root.destroy()
    # If the key pressed was "Left"
    elif event.keysym == "Left":
        # If there are images in the undo lists
        if undo_images and undo_folders:
            # Get the last image and target folder in the lists
            image = undo_images[-1]
            folder = undo_folders[-1]
            # Move the image back to the "archive" folder
            shutil.move(os.path.join(folder, image), os.path.join(path, image))
            # Add the image back to the list of files
            files.append(image)
            # Sort the list of files in natural sort order
            files = natsort.natsorted(files)
            # Set the image of the label to the last image in the undo lists
            set_image(image)
            # Remove the image and target folder from the undo lists
            undo_images.pop(-1)
            undo_folders.pop(-1)
             # If the key pressed was "f" or "j"
    elif event.char.lower() in ["f", "j"]:
        # Get the name of the current image file
        current_image = label.cget("text")
        # If the key pressed was "f"
        if event.char.lower() == "f":
            # Move the current image file to the "bad" folder
            shutil.move(os.path.join(path, current_image), os.path.join(bad_folder, current_image))
            # Add the current image and target folder to the undo lists
            undo_images.append(current_image)
            undo_folders.append(bad_folder)
        # If the key pressed was "j"
        elif event.char.lower() == "j":
            # Move the current image file to the "good" folder
            shutil.move(os.path.join(path, current_image), os.path.join(good_folder, current_image))
            # Add the current image and target folder to the undo lists
            undo_images.append(current_image)
            undo_folders.append(good_folder)
        # Remove the current image file from the list of files
        files.remove(current_image)
        # If there are more images left in the list
        if files:
            # Set the image of the label to the next image file in the list
            set_image(files[0])
        # If there are no more images left in the list
        else:
            # Destroy the main window
            root.destroy()

# Set up a function to display the image in the label
def set_image(image_file):
    # Open the image file and convert it to a PhotoImage object
    image = Image.open(os.path.join(path, image_file))
    image = ImageTk.PhotoImage(image)
    # Set the image of the label to the PhotoImage object
    label.config(image=image)
    label.image = image
    # Set the text of the label to the image file name
    label.config(text=image_file)
    # Set the title of the window to the image file name
    root.title(image_file)

# Create a label to display the current image file
label = tk.Label(root)
label.pack()

# Set the initial image in the label
set_image(files[0])

# Bind the key press function to the main window
root.bind("<Key>", key_press)

# Run the Tkinter event loop
root.mainloop()
