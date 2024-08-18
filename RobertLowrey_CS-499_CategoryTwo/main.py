# Developer: Robert Lowrey - 07/27/2024 Version 2.0
# CS - 499 Computer Science Capstone

# The intent for this artifact requires the user sign in via a login window while hiding the travel
# destinations until they log in with the correct username and password. If either the username or password is
# incorrect,an error window will be displayed. Once the user logs in, the login window will disappear and the travel
# destinations window will be visible.

# Another enhancement is a new feature of a search bar, which allows the user to search for keywords in either the
# picture or description. When the user types in a keyword and clicks the "Search Destinations" button, the application
# will undergo a linear search and show destinations that contain the key word searched.

# The Big-O notation with the linear search is best case O(1), while the average case is O(n).


# Importing the Tkinter library.
import tkinter as tk

# Importing sections of Tkinter library to handle different functionalities.
from tkinter import Canvas, Label, messagebox, Scrollbar

# Importing sections from the Pillow library to handle the different images.
from PIL import ImageTk, Image


# Defining a class named Login.
class Login(tk.Toplevel):
    def __init__(self, master):  # Defining a master __init__ function.
        super().__init__(master)  # Initialize the tk.Toplevel portion of the login window.
        self.title('Login to view destinations!')  # Setting the window label to say "Login to view destinations!".
        self.geometry('350x150')  # Setting the window to width of 350 pixels and height of 150 pixels.
        self.configure(background='#d3d3d3')  # Configuring the background to the light gray color.

        self.master = master  # Creating an instance of an external object.

        # Username label for user input, and setting surrounding padding to 5 pixels.
        tk.Label(self, text='Username:', background='#d3d3d3').pack(pady=5)  # Background color to match the page.
        self.username_entry = tk.Entry(self)  # Getting users input for the username.
        self.username_entry.pack(pady=2)  # Setting the padding between the prompt and input box.

        # Password label for user input and setting surrounding padding to 5 pixels.
        tk.Label(self, text='Password:', background='#d3d3d3').pack(pady=5)  # Background color of text to match page.

        # Getting users input for the password, and displaying an asterisk for each character typed.
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack(pady=2)  # Setting the padding between the prompt and input box.

        # Creating button named "Login".
        self.login = tk.Button(self, text='Login', command=self.authenticate)  # Calling the authenticate function.
        self.login.pack(pady=5)  # Setting the login button padding to 5 pixels.

        self.protocol('WM_CLOSE_WINDOW', self.on_close)  # Handle window close event.

    # Defining a function to authenticate user.
    def authenticate(self):
        username = self.username_entry.get()  # Getting username from the username input.
        password = self.password_entry.get()  # Getting password from the password input.

        # If username and password are correct, take this branch and display the travel destinations.
        if username == 'CS499' and password == 'SNHU2024':

            self.master.main_display()  # Creating an instance of the main_display function.

            self.destroy()  # Calling destroy to close open files to prevent leaks.

        # If username is not correct, display error window.
        else:
            messagebox.showerror('Login Error', 'Invalid username or password! Please try again!')

    def on_close(self):
        self.master.quit()  # Exit the application if login window is closed.
        self.destroy()  # Calling destroy to close open files to prevent leaks.


# Creating a class that will hold the window size, create a canvas, load images, and descriptions.
class PageLayout(tk.Tk):
    def __init__(self, images, descriptions):  # Defining an inherited __init__ function.

        super().__init__()  # Call to the super class.

        self.canvas = None  # Initializing the instance of canvas to none.
        self.search_entry = None  # Initializing the instance of search_entry to none.
        self.search_frame = None  # Initializing the instance of search_frame to none.
        self.search_variable = None  # Initializing the instance of search_variable to none.
        self.selected_row = None  # Initializing the instance of selected_row to none.

        self.title('Top Travel Destinations')  # Setting window title to "Top Travel Destinations".

        self.geometry('500x900')  # Sets the width to 500 pixels and height to 900 pixels of the output window.

        self.configure(background='#d3d3d3')  # Setting the background color to light gray.

        self.images = images  # Initializing instance of images.
        self.descriptions = descriptions  # Initializing an instance of descriptions.

        self.filter_descriptions = descriptions  # Initializing a filtered instance with the list of descriptions.

        self.filter_images = images  # Initializing the filtered instance of images.

        # Set up the main window layout.
        self.main_layout()

        self.wm_withdraw()  # Hiding the main window until the user is logged in with the correct username and password.

        # Creating the login window.
        self.login_window = Login(self)  # Creating an instance of the login window.
        self.wait_window(self.login_window)  # Pausing the travel destinations window until the login window is closed.

    def main_layout(self):
        self.selected_row = None  # Setting the initial row selection to none.

        # Creating the visible search bar.
        self.search_variable = tk.StringVar()
        self.search_frame = tk.Frame(self, background='#d3d3d3')  # Setting search color bar to match page color.
        self.search_frame.pack(pady=10, fill=tk.X)

        # Creating search bar with prompt.
        search_label = tk.Label(self.search_frame, text='Search for keywords:', background='#d3d3d3')
        search_label.pack(side=tk.LEFT, padx=5)  # Positioning prompt on the left side of search text box.

        # Creates an input field for the users text, and links the variable for binding with the widget.
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_variable)

        # Setting input text box to left side of search button.
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        #  Setting name of search button for user to press.
        search_button = tk.Button(self.search_frame, text='Search Destinations', command=self.search_method)
        search_button.pack(side=tk.RIGHT, padx=5)  # Setting search button on the right side of page.

        # Setting the scroll bar configuration to vertical and on the right side of the page.
        scrollbar = Scrollbar(self)
        scrollbar.pack_configure(side=tk.RIGHT, fill=tk.Y)

        # Creating the canvas to hold the images.
        self.canvas = Canvas(self, yscrollcommand=scrollbar.set, background='#d3d3d3')  # Setting background to gray.
        self.canvas.pack_configure(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Configuring the scroll bar on the y-axis.
        scrollbar.configure(command=self.canvas.yview)

        # Create a frame within the canvas to hold images and descriptions.
        self.frame = tk.Frame(self.canvas, background='#d3d3d3')
        self.canvas.create_window((5, 5), window=self.frame, anchor=tk.N)  # Creating a frame for the picture.

        # Load images into the canvas.
        self.load_images()

        # Updating the scroll functionality of the window.
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))  # Set the bounding box to everything in canvas.

        self.binding_mouse_wheel()  # Calling the bind_mouse_wheel function.

        # Call the close_image_files function using the wm protocol to close image files to prevent memory leaks.
        self.wm_protocol('WM_CLOSE_WINDOW', self.close_image_files)

    def main_display(self):
        self.deiconify()  # Show the main application window.
        self.load_images()  # Calling the load_images function to display images.

    # Defining a load_images function.
    def load_images(self):

        self.frame.destroy()  # Clear pre-existing frame contents.
        self.frame = tk.Frame(self.canvas, background='#d3d3d3')  # Set background color of frame to light gray.
        self.canvas.create_window((5, 5), window=self.frame, anchor=tk.N)  # Create frame for picture displayed.

        # Iterate through the image and description lists, and enumerate the pairs of each.
        for i, (images_path, description) in enumerate(zip(self.filter_images, self.filter_descriptions)):

            # Optimize the loading of the information on page.
            try:  # Try statement to open the images and descriptions.

                img = Image.open(images_path)  # Load images.
                img = img.resize((200, 150))  # Resizing the images.
                img = ImageTk.PhotoImage(img)  # Converting image to a Tkinter compatible object.

                # Creating labels for the travel destination pictures.
                # Setting image background color to gray.
                imagelabel = Label(self.frame, image=img, background='#d3d3d3')
                imagelabel.image = img  # Keeping a reference of image.
                imagelabel.grid(row=i, ipadx=15, ipady=15, sticky='NESW')  # Positioning the image within the grid.

                # Setting the button to the left click from the user using lambda.
                imagelabel.bind('<Button-1>', lambda event, r=i: self.row_click(r))

                # Creating label for description and setting the background color to match page color.
                label = Label(self.frame, text=description, wraplength=200, background='#d3d3d3')

                # Handling the click of the description label by user.
                label.bind('<Button-1>', lambda event, r=i: self.row_click(r))

                # Positioning the description label in grid.
                label.grid(row=i, column=2, ipadx=5, ipady=2)

                # Configure the specific properties of each row within the frame.
                self.frame.grid_rowconfigure(i)

            # If exception occurs, print to console to let user know something did not load right in the images file.
            except(IOError, FileNotFoundError):
                print('Image files not properly loaded into application {images}: {e}.')

    # Defining function to search for image and/or description using the search bar functionality.
    def search_method(self):
        # Retrieves and returns string keyword regardless of capitalization within the text.
        query = self.search_variable.get().lower()

        self.filter_images = []  # Initialize/clear filter for images.
        self.filter_descriptions = []  # Initialize/clear filter for descriptions.

        # Optimizing code for enhanced efficiency and minimize redundancy of iteration.
        # Implementing a linear search algorithm to search the users input with the images and descriptions.
        for imageFiles, descriptions in zip(self.images, self.descriptions):
            if query in descriptions.lower():  # If keyword in query was found.
                self.filter_images.append(imageFiles)  # Append image to filtered list.
                self.filter_descriptions.append(descriptions)  # Append description to filtered list.

        # Load images that match the searched query.
        self.load_images()

    # Defining a function to handle if the user clicks on a description or picture.
    def row_click(self, row):

        # Setting the row to the original background color of light gray.
        if self.selected_row is not None and self.selected_row != row:
            for widget in self.frame.grid_slaves(self.selected_row):  # Select row.
                widget.configure(background='#d3d3d3')  # Configure background to gray.

        # Highlight the row that is clicked by the user.
        if self.selected_row == row:
            self.selected_row = None  # Unselect if row is clicked a second time.

        else:
            for widget in self.frame.grid_slaves(row=row):  # Iterate through the rows to check selection.
                widget.configure(background='#ffffff')  # Change background color to white if row is selected.
            self.selected_row = row

    # Defining function to close image files after use preventing memory leaks.
    def close_image_files(self):
        self.destroy()  # Close any open image files to prevent leaks.

    # Function to bind mouse wheel functionality.
    def binding_mouse_wheel(self):
        self.canvas.bind_all('<MouseWheel>', self.mouse_wheel_event_handler)  # Binding mouse wheel for scroll movement.

        # Defining function to handle scroll movement.
    def mouse_wheel_event_handler(self, event):
        if event.num == 4 or event.delta > 0:  # If user scrolls up, scroll up one unit.
            self.canvas.yview_scroll(-1, 'units')
        elif event.num == 5 or event.delta < 0:  # If user scrolls down, scroll down one unit.
            self.canvas.yview_scroll(1, 'units')


if __name__ == '__main__':  # Checking to see if the program is being run on Python.

    # Getting images to display by the names and the order of the images.
    imageFiles = ['Images/CocoCay.jpg', 'Images/Colosseum_in_Rome.jpg', 'Images/Fiji.jpg', 'Images/Germany.jpg',
                  'Images/Hawaii.jpg', 'Images/MexicoCity.jpg', 'Images/Bali.jpg', 'Images/Santorini_Greece.jpg',
                  'Images/Paris.jpg', 'Images/Sydney_Australia.jpg', 'Images/Taj_Mahal.jpg'
                  ]

    # Descriptions of each image.
    descriptions = [
        # Picture one description- CocoCay.
        'CocoCay, Berry Islands - Spend a day on the beach and inside Thrill Water park! '
        'The best time to visit CocoCay is late November to mid-April '
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
        'The best time to visit Germany is late spring through early autumn.',

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

    app = PageLayout(imageFiles, descriptions)  # Initializing the application.
    app.mainloop()  # Event listener to have the window behave accordingly.
