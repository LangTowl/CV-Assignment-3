import os
import cv2
import numpy as np
import skimage as sk
import tkinter as tk
from PIL import ImageTk, Image

class WindowRenderer:

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

        # Add otsu button (binary classification)
        self.otsu_button_binary = tk.Button(self.root, text = "Otsu Segmentation (Binary)", command = self.otsu_threshold_binary)
        self.otsu_button_binary.grid(row = 3, column = 0, pady = 5)

        # Add otsu button (multi class)
        self.otsu_button_multi = tk.Button(self.root, text = "Otsu Segmentation (Multi-class)", command = self.otsu_threshold_multi)
        self.otsu_button_multi.grid(row = 4, column = 0, pady = 5)

        # Add blurr button
        self.blurr_button = tk.Button(self.root, text = "Blurr Segmentation", command = self.blurr_segmentation)
        self.blurr_button.grid(row = 5, column = 0, pady = 5)

        # Add mean shift button
        self.mean_shift_button = tk.Button(self.root, text = "Mean Shift Segmentation", command = self.mean_shift_segmentation)
        self.mean_shift_button.grid(row = 6, column = 0, pady = 5)

        # Add reset button
        self.reset_button = tk.Button(self.root, text = "Reset", command = self.reset)
        self.reset_button.grid(row = 3, column = 1, pady = 5)

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

    def preprocess_images(self):
        # Convert images to arrays
        image1 = np.array(self.image1)
        image2 = np.array(self.image2)
        image3 = np.array(self.image3)

        # Remove alpha channel from image 3
        image3 = image3[:,:,:3]

        # Convert to grayscale
        image1_gs = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        image2_gs = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        image3_gs = cv2.cvtColor(image3, cv2.COLOR_BGR2GRAY)

        return image1, image2, image3, image1_gs, image2_gs, image3_gs

    def otsu_threshold_binary(self):
        print("Segmenting Images...")

        # Ready images for processing
        _, _, _, image1_gs, image2_gs, image3_gs = self.preprocess_images()

        # Apply Otsu threshold
        _, image1_otsu = cv2.threshold(image1_gs, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, image2_otsu = cv2.threshold(image2_gs, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, image3_otsu = cv2.threshold(image3_gs, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Update images
        self.image1_copy = Image.fromarray(image1_otsu)
        self.image2_copy = Image.fromarray(image2_otsu)
        self.image3_copy = Image.fromarray(image3_otsu)

        print("Done.\n")

        # Redraw canvas with new images
        self.update_canvas()

    def otsu_threshold_multi(self):
        print("Segmenting Images...")

        # Ready images for processing
        _, _, _, image1_gs, image2_gs, image3_gs = self.preprocess_images()

        # Determine thresholds from images
        threshold1 = sk.filters.threshold_multiotsu(image1_gs, 5)
        threshold2 = sk.filters.threshold_multiotsu(image2_gs, 5)
        threshold3 = sk.filters.threshold_multiotsu(image3_gs, 5)

        # Load regions from images
        regions1 = np.digitize(image1_gs, bins = threshold1)
        regions2 = np.digitize(image2_gs, bins = threshold2)
        regions3 = np.digitize(image3_gs, bins = threshold3)

        # Scale the regions to use the full uint8 range (0-255)
        regions1 = regions1 * 51
        regions2 = regions2 * 51
        regions3 = regions3 * 51

        # Make regions compatible with tkinter
        regions1 = regions1.astype(np.uint8)
        regions2 = regions2.astype(np.uint8)
        regions3 = regions3.astype(np.uint8)

        # Update images
        self.image1_copy = Image.fromarray(regions1)
        self.image2_copy = Image.fromarray(regions2)
        self.image3_copy = Image.fromarray(regions3)

        print("Done.\n")

        # Redraw canvas with new images
        self.update_canvas()

    def blurr_segmentation(self):
        print("Segmenting Images...")

        # Ready images for processing
        image1, image2, image3, _, _, _ = self.preprocess_images()

        # Apply mean shift filtering
        msf1 = cv2.pyrMeanShiftFiltering(image1, 20, 40)
        msf2 = cv2.pyrMeanShiftFiltering(image2, 20, 40)
        msf3 = cv2.pyrMeanShiftFiltering(image3, 20, 40)

        # # Update images
        self.image1_copy = Image.fromarray(msf1)
        self.image2_copy = Image.fromarray(msf2)
        self.image3_copy = Image.fromarray(msf3)

        print("Done.\n")

        # Redraw canvas with new images
        self.update_canvas()

    def mean_shift_segmentation(self):
        print("Segmenting Images...")

        # Ready images for processing
        image1, image2, image3, _, _, _ = self.preprocess_images()

        # Apply mean shift filtering
        msf1 = cv2.pyrMeanShiftFiltering(image1, 20, 40)
        msf2 = cv2.pyrMeanShiftFiltering(image2, 20, 40)
        msf3 = cv2.pyrMeanShiftFiltering(image3, 20, 40)

        # Convert blurred images to greyscale
        msfb1 = cv2.cvtColor(msf1, cv2.COLOR_BGR2GRAY)
        msfb2 = cv2.cvtColor(msf2, cv2.COLOR_BGR2GRAY)
        msfb3 = cv2.cvtColor(msf3, cv2.COLOR_BGR2GRAY)

        # Compute threshold
        _, threshold1 = cv2.threshold(msfb1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, threshold2 = cv2.threshold(msfb2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, threshold3 = cv2.threshold(msfb3, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # # Update images
        self.image1_copy = Image.fromarray(threshold1)
        self.image2_copy = Image.fromarray(threshold2)
        self.image3_copy = Image.fromarray(threshold3)

        print("Done.\n")

        # Redraw canvas with new images
        self.update_canvas()

    def reset(self):
        print("Resetting Images...")

        # Reset image copys
        self.image1_copy = self.image1
        self.image2_copy = self.image2
        self.image3_copy = self.image3

        print("Done.\n")

        # Redraw canvas with default images
        self.update_canvas()