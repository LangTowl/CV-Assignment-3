import os
import tkinter as tk
from PIL import ImageTk, Image

class RenderWindow:

    # Create RenderWindow object
    def __init__(self, image1, image2, image3,):
        # Debug
        print("New RenderWindow setup starting...\n")

        # Initialize and configure main window
        self.root = tk.Tk()
        self.root.title("Assignment 3 -> Lang Towl")

        # Validate path to images
        print("Path to image1 exists." if os.path.exists(image1) else "Path to image1 does not exist.")
        print("Path to image2 exists." if os.path.exists(image2) else "Path to image2 does not exist.")
        print("Path to image3 exists.\n" if os.path.exists(image3) else "Path to image3 does not exist.\n")

        # Collect images from passed path
        self.image1 = Image.open(image1)
        self.image1_copy = Image.open(image1)

        self.image2 = Image.open(image2)
        self.image2_copy = Image.open(image2)

        self.image3 = Image.open(image3)
        self.image3_copy = Image.open(image3)

        # Make tkinter compatible copy
        self.image1_tk = ImageTk.PhotoImage(self.image1)
        self.image1_copy_tk = ImageTk.PhotoImage(self.image1_copy)

        self.image2_tk = ImageTk.PhotoImage(self.image2)
        self.image2_copy_tk = ImageTk.PhotoImage(self.image2_copy)

        self.image3_tk = ImageTk.PhotoImage(self.image3)
        self.image3_copy_tk = ImageTk.PhotoImage(self.image3_copy)

        # Add execution button
        self.execute_button = tk.Button(self.root, text = "Run Segmentation", command = self.segment_image)
        self.execute_button.grid(row = 3, column = 0, pady = 10)

        # Add reset button
        self.reset_button = tk.Button(self.root, text = "Reset", command = self.reset)
        self.reset_button.grid(row = 3, column = 1, pady = 10)

        # Render canvas
        self.update_canvas()

        # Debug
        print("RenderWindow setup finished...\nApplication Running...\n")

        # Start main event loop
        self.root.mainloop()


    # Update images in canvas
    def update_canvas(self):
        print("Updating Canvas...")

        # Reformat PIL images to tkinter compatible format
        self.image1_tk = ImageTk.PhotoImage(self.image1)
        self.image1_copy_tk = ImageTk.PhotoImage(self.image1_copy)

        self.image2_tk = ImageTk.PhotoImage(self.image2)
        self.image2_copy_tk = ImageTk.PhotoImage(self.image2_copy)

        self.image3_tk = ImageTk.PhotoImage(self.image3)
        self.image3_copy_tk = ImageTk.PhotoImage(self.image3_copy)


        # Add images to canvas
        tk.Label(self.root, image = self.image1_tk).grid(row = 0, column = 0)
        tk.Label(self.root, image = self.image1_copy_tk).grid(row = 0, column = 1)

        tk.Label(self.root, image = self.image2_tk).grid(row = 1, column = 0)
        tk.Label(self.root, image=self.image2_copy_tk).grid(row = 1, column = 1)

        tk.Label(self.root, image = self.image3_tk).grid(row = 2, column = 0)
        tk.Label(self.root, image = self.image3_copy_tk).grid(row = 2, column = 1)

        print("Canvas Update Finished...\n")

    def segment_image(self):
        print("Segmenting Images...")

    def reset(self):
        print("Resetting Images...")