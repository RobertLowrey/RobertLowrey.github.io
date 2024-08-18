# Developer: Robert Lowrey - 07/21/2024 Version 1.0
# CS - 499 Computer Science Capstone

# This project was ported to Python from the original Java language.

# The intent for this application is to display eleven travel destinations.
# Each travel destination has a picture along with corresponding descriptions and discusses the best time to visit.

# The images are imported using a file called Images to ensure that all are accounted for,
# and the Images file can be closed to prevent data leaks and injection attacks with malicious intent.

# If the user clicks on a picture or description within the window, the background color of the image
# and description will change to white to indicate the row that was selected.
# If the user clicks a highlighted row, the background color will revert to the original color.

# Importing the Tkinter Python library.
import tkinter as tk
from tkinter import Canvas, Label, Scrollbar

# Sections of the Pillow library for handling the different images.
from PIL import ImageTk, Image


# Creating a class that will hold the window size, create a canvas, load images, and descriptions.
class PageLayout(tk. Tk):
    def __init__(self, images):  # Defining an inherited __init__ function.

        super().__init__()  # Call to the super class.

        self.images = images  # Initializing instance of images.
        self.title("Top Travel Destinations")  # Setting the window title to "Travel Destinations".

        self.geometry('500x900')  # Sets the width to 500 pixels and height to 900 pixels of the output window.

        self.configure(background='#d3d3d3')  # Setting the background color to light gray.

        # Setting the initial row selection to none.
        self.selected_row = None

        # Setting the scroll bar configuration to vertical and on the right side of the page.
        scrollbar = Scrollbar(self)
        scrollbar.pack_configure(side=tk.RIGHT, fill=tk.Y)

        # Creating the canvas to hold the images.
        self.canvas = Canvas(self, yscrollcommand=scrollbar.set, background='#d3d3d3')  # Setting background to gray.
        self.canvas.pack_configure(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Configuring the scroll bar on the y-axis.
        scrollbar.configure(command=self.canvas.yview)

        # Creating a frame within the canvas to hold images and descriptions.
        self.frame = tk.Frame(self.canvas, background='#d3d3d3')
        self.canvas.create_window((5, 5), window=self.frame, anchor=tk.N)  # Creating a frame for the picture.

        # calling the load_images function to place images onto the canvas.
        self.load_images()

        # Updating the scroll aspect of window.
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))  # Set the bounding box to everything in canvas.

        self.binding_mouse_wheel()  # Calling the bind_mouse_wheel function.

        # Calling cleanup function to close image files to prevent memory leaks.
        self.wm_protocol("WM_CLOSE_WINDOW", self.close_image_files)

    # Defining a load_images function.
    def load_images(self):

        # Iterate through the image and description lists, and enumerate the pairs of each.
        for i, (images, description) in enumerate(zip(imageFiles, descriptions)):

            img = Image.open(images)  # Loading the images.
            img = img.resize((200, 150))  # Resizing the images.
            img = ImageTk.PhotoImage(img)  # Converting image to a Tkinter compatible object.

            # Creating labels for the travel destination pictures.
            imagelabel = Label(self.frame, image=img,  background='#d3d3d3')  # Setting image background color to gray.
            imagelabel.image = img  # Keeping a reference of image.
            imagelabel.grid(row=i, ipadx=15, ipady=15, sticky='NESW')  # Positioning the image within the grid.

            # Setting the button to the left click from the user using lambda.
            imagelabel.bind('<Button-1>', lambda e, r=i: self.row_click(e, r))

            # Creating label for description and setting the background color to match page color.
            label = Label(self.frame, text=description, wraplength=200, background='#d3d3d3')

            # Handling the click of the description label by user.
            label.bind('<Button-1>', lambda e, r=i: self.row_click(e, r))

            # Positioning the description label in grid.
            label.grid(row=i, column=2, ipadx=5, ipady=2)

            # Configuring the specific properties of each row within the frame.
            self.frame.grid_rowconfigure(i)

    # Defining a function to handle if the user clicks on a description or picture.
    def row_click(self, event, row):

        # Set the row to the original background color of light gray.
        if self.selected_row is not None and self.selected_row != row:
            for widget in self.frame.grid_slaves(self.selected_row):  # Select row.
                widget.configure(bg='#d3d3d3')  # Configure background to gray.

        # Highlight the row that is clicked by the user.
        if self.selected_row == row:
            self.selected_row = None  # Unselect if same row is clicked a second time.

        else:
            for widget in self.frame.grid_slaves(row=row):  # Iterate through the rows to check selection.
                widget.configure(bg='#ffffff')  # Change background color to white if row is selected by user.
            self.selected_row = row

    # Close_files function to close files after use preventing memory leaks.
    def close_image_files(self):
        self.destroy()  # Close remaining open image files to prevent leaks.

    # Function to bind mouse wheel functionality.
    def binding_mouse_wheel(self):
        self.canvas.bind_all("<MouseWheel>", self.mouse_wheel_event_handler)  # Binding mouse wheel for scroll movement.

    # Defining function to handle scroll movement on mouse wheel.
    def mouse_wheel_event_handler(self, event):
        if event.num == 4 or event.delta > 0:  # Scroll up if user scrolls up.
            self.canvas.yview_scroll(-1, "units")  # Scroll up one unit.
        elif event.num == 5 or event.delta < 0:  # Scroll down if user scrolls down.
            self.canvas.yview_scroll(1, "units")  # Scroll down 1 unit.


# Getting images to display by the names and the order of the images.
imageFiles = ['Images/CocoCay.jpg', 'Images/Colosseum_in_Rome.jpg', 'Images/Fiji.jpg', 'Images/Germany.jpg',
              'Images/Hawaii.jpg', 'Images/MexicoCity.jpg', 'Images/Bali.jpg', 'Images/Santorini_Greece.jpg',
              'Images/Paris.jpg', 'Images/Sydney_Australia.jpg', 'Images/Taj_Mahal.jpg']


# Descriptions of each image.
descriptions = [
    # Picture one description- CocoCay.
    'CocoCay, Berry Islands - Spend a day on the beach and inside Thrill Water park! '
    'The best time to visit CocoCay is Late November to mid-April '
    'if you desire spring weather!',

    # Picture two description- Rome.
    'Rome, Italy - A gorgeous historic city that still holds glory! Experience the colosseum of '
    'Roman history and learn about the shows that occurred in the past! The best time to '
    'visit Rome is April to June to remain cool during the spring weather!',

    # Picture three description- Oceania.
    'Fiji, Oceania - Snorkel and scuba dive in an underwater wonderland! '
    'The best time to visit Fiji is during May through October depending on your '
    'preference of season!',

    # Picture four description- Germany.
    'Germany - Visit Berlin and experience Oktoberfest! '
    'The best time to visit Germany is Late spring through early autumn.',

    # Picture five description- USA.
    'Hawaii, United States of America - Great for snorkeling and gorgeous sunsets! '
    'The best time to visit Hawaii is April to June, and September to October.',

    # Picture six description- Mexico.
    'Mexico City, Mexico - Dive into a world of art at the Frida Kahlo Museum and sail on'
    'the Xochimilco Canals! The best time to visit Mexico City is June to August.',

    # Picture seven description- Asia.
    'Bali, Asia - Bali is known for their astonishing nature and cultural activities! '
    'The best time to visit Bali is either May,June,or September.',

    # Picture eight description- Europe.
    'Greece, Europe - Beautiful blue beaches, and amazing culture! '
    'The best time to visit Greece is April to June.',

    # Picture nine description- France.
    'Paris, France - The most romantic city, great for anniversaries and a romantic'
    'getaway! The best time to visit France is March to May.',

    # Picture ten description- Australia.
    'Sydney, Australia - Amazing architecture and great shows! '
    'The best time to visit Australia is March to May.',

    # Picture eleven description- India.
    'Taj Mahal, India - The greatest example of Mughal architecture, and '
    'great experiences! The best time to visit India is March to June.',
]


if __name__ == "__main__":  # Checking to see if the program is being run on Python.
    app = PageLayout(imageFiles)  # Initializing the application.
    app.mainloop()  # Event listener to have the window run with appropriate behavior upon scrolling.
