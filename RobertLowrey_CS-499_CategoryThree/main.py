# Developer: Robert Lowrey - 08/1/2024 Version 3.0
# CS - 499 Computer Science Capstone

# The enhancement for this artifact implements a MongoDB Compass NoSQL database to store the username
# and password that the user chooses to log into the system.

# Also, there is an addition of a new file named databaseConfiguration.py that maintains the connection to the
# MongoDB Compass database called TravelDestinationDatabase with a collection name of userInfo.

# If the user has never logged into the application they are able to create an account by clicking the
# "Create Account" button. Once this button is clicked, it will display another window that allows the user to
# create a username and password to be stored within the database. The user is required to enter the password twice to
# confirm spelling and capitalization of the password they desire.

# The user is to select their role  within the application. This will enable differentiation of users and
# administrators. The administrators are able to remove users from the system, while users can only view the
# travel destinations after logging into the system.

# Once the account creation is complete, the password will be stored as a salted hash inside the database to add an
# extra layer of security to the application.


# Importing the Tkinter library.
import tkinter as tk

# Importing sections of Tkinter library to handle different functionalities.
from tkinter import Canvas, Label, messagebox, Scrollbar

# Importing sections from the Pillow library to handle the different images.
from PIL import ImageTk, Image

# Importing the get_collection method from the databaseConfiguration.py file.
from databaseConfiguration import get_collection

# Importing the Bcrypt library for salted hashes of the passwords stored in database.
import bcrypt


# Defining class for users who selected role of Admin.
class Admin(tk.Toplevel):
    def __init__(self, master):  # Defining a master __init__ function.
        super().__init__(master)  # Initialize the tk.Toplevel portion of the Admin window.
        self.title('Admin')  # Setting the Admin window label to say "Admin".

        # Setting the size of the window to have a width of 400 pixels and height of 400 pixels.
        self.geometry('400x400')
        self.configure(background='#d3d3d3')  # Setting the background to light gray to match the other windows.

        # Creating a window for managing users with title "Admin Window".
        tk.Label(self, text='Admin Window ', font=('Arial', 16), background='#d3d3d3').pack(pady=10)

        # Creating a box to list usernames for Admins.
        self.user_listbox = tk.Listbox(self, width=50, height=15)
        self.user_listbox.pack(pady=10)

        # Loading users to display in the list.
        self.load_users()

        # Creating button to enable Admin to delete user from the selected username.
        tk.Button(self, text='Delete User', command=self.delete_user).pack(pady=5)

        # Creating button to exit the Admin Window.
        tk.Button(self, text='Exit', command=self.destroy).pack(pady=5)

        # Call the close_files function using the wm protocol to close window to prevent memory leaks.
        self.protocol('WM_CLOSE_WINDOW', self.on_close)

    # Defining method to load users into the list box for Admin to view.
    def load_users(self):
        # Load all users from the database.
        collection = get_collection()  # Creating an instance of the get_collection() method.

        users = collection.find()  # Getting user documents from the MongoDB collection.

        self.user_listbox.delete(0, tk.END)  # Clear existing items within list.

        for user in users:  # Iterate through usernames.
            self.user_listbox.insert(tk.END, user['username'])  # Insert and display usernames in listbox.

    # Defining method to delete users that are selected within Admin window.
    def delete_user(self):
        # Retrieving selected username from MongoDB.
        selected_user = self.user_listbox.get(tk.ACTIVE)

        if not selected_user:  # If no user is selected take this branch.

            # Show warning if no username is selected for deletion.
            messagebox.showwarning('Error!', 'Please select a username to delete!')
            return

        collection = get_collection()  # Creating an instance of the get_collection() method.

        # Delete a single document containing the selected username in the MongoDB collection.
        result = collection.delete_one({'username': selected_user})

        if result.deleted_count > 0:  # Checking if the document was deleted.
            self.user_listbox.delete(tk.ACTIVE)  # Deleting the item that was selected in the listbox.

            # Displaying a message if the deletion of the account was successful.
            messagebox.showinfo('Success', f'User "{selected_user}" deleted successfully.')
        else:
            # Display error message that the user couldn't be deleted.
            messagebox.showerror('Error', 'Could not delete user!')

    # Defining a method to close files.
    def on_close(self):
        self.destroy()  # Closing files to prevent memory leaks.


# Defining a class to register users with the NoSQL database.
class Register(tk.Toplevel):
    def __init__(self, master):  # Defining a master __init__ function.
        super().__init__(master)  # Initialize the tk.Toplevel portion of the registration window.

        self.role_var = None  # Initializing role_var to none.
        self.title('Create Your Account!')  # Setting the registration window label to say "Create Your Account!".

        # Setting the size of the window to have a width of 350 pixels and height of 300 pixels.
        self.geometry('350x300')

        self.configure(background='#d3d3d3')  # Setting the background to light gray to match the other windows.

        # Setting the prompt for user to input username they want to save.
        tk.Label(self, text='Enter Username:', background='#d3d3d3').pack(pady=5)
        self.username_entry = tk.Entry(self)  # Getting the username input from the user to store in the database.
        self.username_entry.pack(pady=2)

        # Setting the prompt for user to input password with background color to match window color.
        tk.Label(self, text='Enter Password:', background='#d3d3d3').pack(pady=5)

        # Getting users input for the password, and displaying an asterisk for each character typed.
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack(pady=2)

        # Setting the prompt for user to re-input password to ensure capitalization and spelling is correct.
        tk.Label(self, text='Re-enter Password:', background='#d3d3d3').pack(pady=5)

        # Getting users input for the password, and displaying an asterisk for each character typed.
        self.confirm_password_entry = tk.Entry(self, show='*')
        self.confirm_password_entry.pack(pady=2)

        self.create_role()  # Creating call instance of the create_role function.

        # Creating a button,that when clicked, it will create a username and password for the user to log in with.
        tk.Button(self, text='Create Account', command=self.create_account).pack(pady=10)

        # Call the close_files function using the wm protocol to close window to prevent memory leaks.
        self.protocol('WM_CLOSE_WINDOW', self.close_window)

    # Method to create role in the Database.
    def create_role(self):
        # Creating a prompt for user to select their role.
        tk.Label(self, text='Select Role:', background='#d3d3d3').pack(pady=5)

        self.role_var = tk.StringVar(value='user')  # Setting default role to user.

        roles = ['User', 'Admin']  # Role options to choose from.

        for role in roles:  # Iterate through roles.

            tk.Radiobutton(self, text=role.capitalize(), variable=self.role_var, value=role,
                           background='#d3d3d3').pack()  # Creating radio button for each role to choose from.

    # Defining a method to create account for user.
    def create_account(self):

        # Gets the users input for username field.
        username = self.username_entry.get().strip()  # Using strip to remove unnecessary white space.

        # Gets the users input for password.
        password = self.password_entry.get().strip()  # Using strip to remove unnecessary white space.

        # Getting the raw password entry to confirm password.
        confirm_password = self.confirm_password_entry.get().strip()  # Using strip to remove unnecessary white space.

        role = self.role_var.get()  # Retrieving current value of role.

        if username == '':  # Input validation of username entry from user.
            # Display error message if username field is empty.
            messagebox.showerror('Error!', 'Username field can not be empty!')
            return

        if password == '':  # Input validation of password entry from user.
            # Display error message if password field is empty.
            messagebox.showerror('Error!', 'Password field can not be empty!')
            return

        # Validating that the password entered does match the stored password within the database.
        if password != confirm_password:
            # Display error message if passwords do not match.
            messagebox.showerror('Error!', 'Passwords entered do not match! Please Try Again!')
            return

        collection = get_collection()  # Creating an instance of the get_collection() method.

        if collection.find_one({'username': username}):  # Find username entered within database.

            # Display error message if username already exists within the database.
            messagebox.showerror('Error! Username already exists, please choose another!')
            return

        # Generate hashed password, then salt the password to store in database.
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert username, password, and role set by user into the database.
        collection.insert_one({'username': username, 'password': hashed_password, 'role': role})

        # Display success message to let user know that the account was created successfully.
        messagebox.showinfo('Success', 'Account created! Please Login!')

        self.destroy()  # After username and password are inserted into database, close window.

    # Defining method to close window after account is created.
    def close_window(self):
        self.destroy()  # Destroy window after user account is created.


# Defining a class named Login.
class Login(tk.Toplevel):
    def __init__(self, master):  # Defining a master __init__ function.

        super().__init__(master)  # Initialize the tk.Toplevel portion of the login window.

        self.title('Login to view destinations!')  # Setting the window label to say "Login to view destinations!".

        self.geometry('350x200')  # Setting the window to width of 350 pixels and height of 200 pixels.

        self.configure(background='#d3d3d3')  # Configuring the background to the light gray color.

        self.master = master  # Creating an instance of an external object.

        # Username label for user input and setting surrounding padding to 5 pixels.
        tk.Label(self, text='Username:', background='#d3d3d3').pack(pady=5)  # Background color to match page.

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

        # Creating button named "Create Account", and calling the open_register function.
        new_user = tk.Button(self, text='Create Account', command=self.open_register_class)
        new_user.pack(pady=2)  # Setting the padding between the login button and the Create Account button.

        # Call the close_files function using the wm protocol to close window to prevent memory leaks.
        self.protocol('WM_CLOSE_WINDOW', self.on_close)

    # Defining a method called authenticate to ensure authentication of the user.
    def authenticate(self):
        username = self.username_entry.get()  # Getting username from the username input.
        password = self.password_entry.get()  # Getting password from the password input.

        collection = get_collection()  # Creating an instance of the get_collection method called collection.

        user = collection.find_one({'username': username})  # Finding username within the database to ensure it matches.

        # If username and password match what is stored within the database, this branch is taken.
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            self.destroy()  # Close login window.

            # Pass the user's role to the main display.
            self.master.main_display(user['role'])  # If role is admin, it will show an option for an Admin button.

        # If username and/or password do not match, this branch is taken.
        else:
            # Error message will be displayed that either the username or password does not match what is stored
            # within the database.
            messagebox.showerror('Login Error!', 'Invalid username or password! Please try again!')

    # Defining a method to open the register class.
    def open_register_class(self):
        Register(self)  # Creating an instance of the Register class.

    # Defining a method to close window after authentication occurs.
    def on_close(self):
        self.master.quit()  # Exit the application if login window is closed.
        self.destroy()  # Calling destroy to close open files to prevent leaks.


# Creating a class that will hold the window size, create a canvas, load images, and descriptions.
class PageLayout(tk.Tk):
    def __init__(self, images, descriptions):  # Defining an inherited __init__ function.

        super().__init__()  # Call to the super class.

        self.user_role = None  # Initializing the instance of role to none.
        self.canvas = None  # Initializing the instance of canvas to none.
        self.search_entry = None  # Initializing the instance of search_entry to none.
        self.search_frame = None  # Initializing the instance of search_frame to none.
        self.search_variable = None  # Initializing the instance of search_variable to none.
        self.selected_row = None  # Initializing the instance of selected_row to none.

        self.user_role = self.user_role  # Setting the default role to 'User'.

        self.title('Top Travel Destinations')  # Setting window title to Top Travel Destinations.

        self.geometry('600x900')  # Sets the output window width to 600 pixels and height to 900 pixels.

        self.configure(background='#d3d3d3')  # Setting the background color to light gray.

        self.images = images  # Initializing instance of images.
        self.descriptions = descriptions  # Initializing an instance of descriptions.

        self.filter_descriptions = descriptions  # Initializing a filtered instance with the list of descriptions.

        self.filter_images = images  # Initializing the filtered instance of images.

        # Set up the main app layout.
        self.main_layout()

        self.wm_withdraw()  # Hiding the main window until the user is logged in with the correct username and password.

        # Creating the login window.
        self.login_window = Login(self)  # Creating an instance of the login window.
        self.wait_window(self.login_window)  # Pausing the travel destinations window until the login window is closed.

    # Defining a method called main_layout to handle the main application window.
    def main_layout(self):
        self.selected_row = None  # Setting the initial row selection to none.

        # Creating the visible search bar.
        self.search_variable = tk.StringVar()
        self.search_frame = tk.Frame(self, background='#d3d3d3')  # Setting search color bar to match page color.
        self.search_frame.pack(pady=10, fill=tk.X)

        # Creating search bar with prompt.
        search_label = tk.Label(self.search_frame, text='Search for keywords:', background='#d3d3d3')
        search_label.pack(side=tk.LEFT, padx=5)  # Positioning prompt on the left side of input text box.

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

        self.canvas.create_window((5, 5), window=self.frame, anchor=tk.N)  # Creating a frame to hold the picture.

        # Load images into the canvas.
        self.load_images()

        # Updating the scroll functionality of the window.
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))  # Set the bounding box to everything in canvas.

        self.binding_mouse_wheel()  # Calling the binding_mouse_wheel functionality.

        # Call the close_image_files function using the wm protocol to close image files to prevent memory leaks.
        self.wm_protocol('WM_CLOSE_WINDOW', self.close_image_files)

        if self.user_role == 'Admin':  # If user role is 'Admin' this branch is taken.

            # Creating button that only Admins can see and interact with.
            admin_button = tk.Button(self.search_frame, text='Admin Window', command=self.admin_panel)
            admin_button.pack(side=tk.RIGHT, padx=10)

    def main_display(self, role):
        self.deiconify()  # Show the main application window.
        self.load_images()  # Calling the load_images function to display images.

        self.ui_based_on_role(role)  # Configure page layout based on users selected role.

    # Defining a method to handle role if Admin is chosen.
    def ui_based_on_role(self, role):

        if role == 'Admin':  # If Admin is selected this branch is taken.

            # Create button named Admin Window.
            admin_button = tk.Button(self, text='Admin Window', command=self.admin_panel)
            admin_button.pack(pady=15)

    # Defining a method to call Admin class.
    def admin_panel(self):
        Admin(self)  # Calling Admin Class.

    # Defining a load_images method.
    def load_images(self):

        self.frame.destroy()  # Clear pre-existing frame contents.
        self.frame = tk.Frame(self.canvas, background='#d3d3d3')  # Set background color of frame to light gray.
        self.canvas.create_window((5, 5), window=self.frame, anchor=tk.N)  # Create frame for picture displayed.

        # Iterate through the image and description lists, and enumerate the pairs of each.
        for i, (images, description) in enumerate(zip(self.filter_images, self.filter_descriptions)):

            try:  # Try to open the images and descriptions.

                img = Image.open(images)  # Load images.
                img = img.resize((200, 150))  # Resizing the images.
                img = ImageTk.PhotoImage(img)  # Converting image to a Tkinter compatible object.

                # Creating labels for the travel destination images.
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

            # If exception occurs, print to console to let user know something did not load
            # correctly in the images file.
            except(IOError, FileNotFoundError):
                print('Error! Files did not load properly! {images}: {e}.')

    # Defining method to search for image and/or description using the search bar functionality.
    def search_method(self):
        # Retrieves and returns string keyword regardless of capitalization within the text.
        query = self.search_variable.get().lower()

        self.filter_images = []  # Initialize/clear filter for images.
        self.filter_descriptions = []  # Initialize/clear filter for descriptions.

        # Optimizing code for enhanced efficiency and minimize redundancy of iteration.
        # Implementing a linear search algorithm to search the users input with the images and descriptions.
        for imageFiles, descriptions in zip(self.images, self.descriptions):

            if query in descriptions.lower():  # If keyword in query was found take this branch

                self.filter_images.append(imageFiles)  # Append image to list
                self.filter_descriptions.append(descriptions)  # Append description to list

        # Load images that match the search.
        self.load_images()

    # Defining a method to handle if the user clicks on a description or picture.
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

    # Defining method to close image files after use preventing memory leaks.
    def close_image_files(self):
        self.destroy()  # Close any open image files to prevent leaks.

    # Method to bind mouse wheel functionality.
    def binding_mouse_wheel(self):
        self.canvas.bind_all('<MouseWheel>', self.mouse_wheel_event_handler)  # Binding mouse wheel for scroll movement.

        # Defining method to handle scroll movement.
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
