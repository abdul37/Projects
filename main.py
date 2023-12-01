from tkinter import *  # import almost everything from the tkinter module

from tkinter import font  # sometimes you have to specifically import a module from a package, even if you used * to import the package before


# import the page classes from their respective files so you can later instantiate them in the main file class
from create_first_page import Page1
from create_second_page import Page2
from create_third_page import Page3

import json  # import the json module so you can load the data from the json file

# when you inherit from the Frame class, you're creating a widget, that being the frame
# the frame is the parent of the widgets that are placed on it
# the parameter parent is the frame that the widgets will be placed on
# the main parent is the root window, which is the window that the frame is placed on
# the root window is the parent of the frame, and the frame is the parent of the widgets
# the widgets are the children of the frame, and the frame is the child of the root window
# after creating the root, you place it inside the init of the App class, then use that value to instantiate
# self.parent, which is the root window, then that value is passed into the init of the Page1 class
# you use super in the App class because you're inheriting from the Frame class, and you want to call the
# init of the Frame class, which is the parent class, and you want to pass in the root window as the parameter

# NOTE: Lambda functions are often used in this program and in Python allow you to create anonymous functions i.e., functions without a name.
# They are used when you need a small, throwaway function that you don't intend to use elsewhere in your code.
# You can have anything in a lambda function that you can have in a normal function, as long as it's an expression
# that returns a value. This includes operations on different types of variables, like numbers, strings, lists, etc.
# EG: concatenate = lambda x, y: x + y ---> in use print(concatenate("Hello, ", "World!"))  # Output: Hello, World!


class App(Frame):  # create the main file class, inheriting from the Frame class
    def __init__(self, parent):  # create the init method, which is the constructor, and pass in the parent parameter
        super().__init__(parent)  # call the init of the parent class, which is the Frame class, and pass in the parent parameter

        # initialize page variables
        self.page1 = None
        self.page2 = None
        self.page3 = None
        self.parent = parent

        # NOTE: THERE IS A DIFFERENCE BETWEEN THE CURRENT AND LAST ITEM FOCUSED ON
        # this initializes a variable that will be used to keep track of the current item focused on
        # by default, the program will focus on the last item focused on, so this variable will allow you to manipulate the current item focused on
        self.pg1_current_item_focused_on = None
        self.pg2_current_item_focused_on = None
        self.pg3_current_item_focused_on = None

        # initialize the list of pages
        self.pages = []

        # initialize the first page index
        self.current_page_index = 0

        # initialize the background color
        self.background = "gray15"

        # placeholder prevents the app image icon from being trashed by the garbage collector by storing a reference to it
        self.smaller_icon_image = None

        # create the app title
        self.parent.title("Employee Schedule Maker")

        # remove default bindings so they don't interfere with the custom bindings
        self.parent.unbind_class("Entry", "<Tab>")  # will be used for navigation
        self.parent.unbind_class("Entry", "<Shift-Tab>")
        self.parent.unbind_class("MacButton", "<Tab>")  # NOTE: WILL UNBIND FROM BOTH BUTTON AND MACBUTTON JUST IN CASE
        self.parent.unbind_class("MacButton", "<Shift-Tab>")
        self.parent.unbind_class("Entry", "<Up>")  # will be used for navigation
        self.parent.unbind_class("Entry", "<Down>")
        self.parent.unbind_class("MacButton", "<Up>")
        self.parent.unbind_class("MacButton", "<Down>")
        self.parent.unbind_class("Button", "<Up>")  # will be used for navigation
        self.parent.unbind_class("Button", "<Down>")
        self.parent.unbind_class("Button", "<Tab>")
        self.parent.unbind_class("Button", "<Shift-Tab>")
        self.parent.unbind_class("Entry", "<Command-z>")  # will be used for undo
        self.parent.unbind_class("Entry", "<Command-Z>")
        self.parent.unbind_class("MacButton", "<Command-z>")  # NOTE NOTE NOTE NOTE NOTE: THIS HAD TWO > SIGNS ON THE LEFT SIDE BEFORE, I REMOVED IT, CHECK IF THAT CAUSES ANY PROBLEMS
        self.parent.unbind_class("MacButton", "<Command-Z>")
        self.parent.unbind_class("Button", "<Command-z>")
        self.parent.unbind_class("Button", "<Command-Z>")
        self.parent.bind("<Command-z>", lambda e: "break")  # e stands for event, and the break prevents the default binding from happening
        # used this break because the default command-z binding was overriding the command-z custom bindings

        # NOTE: DO NOT USE GEOMETRY, IT GETS IN THE WAY OF THE WINDOW AUTOMATICALLY ADJUSTING ITS SIZE BASED ON YOUR WIDGETS
        # eg: don't use config(width=500,height=500)

        # call the create pages method
        self.create_pages()

    def load_data(self, file_path):  # method to load the data from the json file
        try:  # try to open the json file
            with open(file_path, "r") as file:  # open the json file, set it as the file variable
                data = json.load(file)  # load the data from the json file into the data variable
            return data  # return the data variable
        except FileNotFoundError:  # if the json file is not found
            print("No file found")  # print "No file found"
            return None  # then return None

    # method that creates the pages2
    def create_pages(self):
        # create the pages
        self.page1 = Page1(
            parent=self.parent,
            move_forward=self.move_forward,  # first page will only have a move forward button
            main_file_instance=self,  # pass in the main file instance so you can access its attributes and methods
        )

        self.page2 = Page2(
            self.parent,
            move_forward=self.move_forward,  # second page will have both a move forward and move backward button
            move_backward=self.move_back,
            page1_instance=self.page1,
            main_file_instance=self,
        )
        self.page3 = Page3(
            self.parent,
            move_backward=self.move_back,  # third page will only have a move backward button
            main_file_instance=self,
        )

        # place the grids of the pages on the frame of the parent
        self.page1.grid(row=0, column=0, sticky="nsew")
        self.page2.grid(row=0, column=0, sticky="nsew")
        self.page3.grid(row=0, column=0, sticky="nsew")

        # add the pages to the list of pages
        self.pages.append(self.page1)
        self.pages.append(self.page2)
        self.pages.append(self.page3)

        # raise the first page to the top since when you placed their grids on the parent frame starting from the first page, the first page is at the bottom
        self.page1.tkraise()

        # methods for respective parent bindings will be called when moving between pages, you call the first page here because the first page is the first page that will be raised
        # when the program starts
        self.page1_parent_bindings()

        # adjust the window size to accommodate the widgets on the first page, otherwise it will accommodate the widgets on the all the pages
        self.adjust_window_size()

        # set the focus to the name entry on the first page when the program first starts
        # the focus set must be after the page is raised, not before, otherwise it won't work
        self.page1.name_entry.focus_set()

    # create a method that adjusts the window size to accommodate the widgets on the current page when moving between pages
    def adjust_window_size(self):
        # NOTE: YOU MUST USE UPDATE_IDLETASKS BEFORE YOU CAN GET THE WIDGET'S WIDTH AND HEIGHT
        # because some tasks are not always automatically updated, so you have to manually update them
        self.parent.update_idletasks()

        # get the current page
        current_page = self.pages[self.current_page_index]

        # adjust the window size to accommodate the widgets on the current page
        self.parent.geometry(f"{current_page.winfo_reqwidth()}x{current_page.winfo_reqheight()}")

        # update the window just in case
        self.parent.update_idletasks()

    # method that moves forward to the next page
    def move_forward(self, event):
        # Check if current_page_index is less than total pages minus 1(cause index starts at 0)
        if self.current_page_index < len(self.pages) - 1:
            data = self.load_data("employee_time_project_data_file.json")  # load the data from the json file
            self.page2.update_data(data)  # update the data on the two pages that have widgets displaying data, page1 is not one of them
            self.page3.update_data(data)

            self.current_page_index += 1  # increment the current page index
            self.switch_page()  # call the switch page method

    # method that moves backward to the previous page
    def move_back(self, event):
        # Check if current_page_index is more than 0 to prevent going into negative numbers and getting an error
        if self.current_page_index > 0:
            data = self.load_data("employee_time_project_data_file.json")  # load the data from the json file
            self.page2.update_data(data)  # update the data on the two pages that have widgets displaying data, page1 is not one of them
            self.page3.update_data(data)

            self.current_page_index -= 1  # decrement the current page index
            self.switch_page()  # call the switch page method

    # method that switches between pages
    def switch_page(self):
        # remove all pages from the parent frame
        for page in self.pages:
            page.grid_remove()

        # get the current page
        current_page = self.pages[self.current_page_index]
        current_page.grid()  # place the current page on the parent frame
        self.adjust_window_size()  # adjust the window size to accommodate the widgets on the current page

        self.unbind_all_parent_bindings()  # unbind all parent bindings before setting new ones to preventing overlapping bindings

        if self.current_page_index == 0:
            self.page1_parent_bindings()  # set the parent bindings for the first page if the current page index is 0
            if self.pg1_current_item_focused_on and  self.widget_exists(self.pg1_current_item_focused_on):  # check if the last item focused on exists
                self.pg1_current_item_focused_on.focus_set()  # keeps track of last item focused on from page1 so when the user moves back to page1,
            # the focus is set to the last item focused on
            # for page one, you won't need an if statement to first check if the last focused on widget exists because the first page doesnt
            # have any widgets that can be deleted

        elif self.current_page_index == 1:
            self.page2_parent_bindings()  # set the parent bindings for the second page if the current page index is 1

            # create condition that checks if the last item focused on was a data widget that was deleted
            if self.pg2_current_item_focused_on and self.widget_exists(self.pg2_current_item_focused_on) and self.pg2_current_item_focused_on not in self.page2.list_of_all_widgets:
                self.pg2_current_item_focused_on.focus_set()  # if it wasnt deleted, set the focus to the last item focused on
            else:
                self.page2.back_button.focus_set()  # if it was deleted, set the focus to the back button

        else:
            self.page3_parent_bindings()  # set the parent bindings for the third page if the current page index is 2
            if self.pg3_current_item_focused_on and self.widget_exists(self.pg3_current_item_focused_on):
                self.pg3_current_item_focused_on.focus_set()
            else:
                self.page3.back_button.focus_set()  # if it doesn't exist, set the focus to the back button

        current_page.tkraise()  # Raise the current page to top

        # set the individual page's current_page_index to the main file's current_page_index so they all keep those values in sync
        # since some methods in the respective pages use the current_page_index to determine if they should run or not, eg: for button bindings
        self.page1.current_page_index = self.current_page_index
        self.page2.current_page_index = self.current_page_index
        self.page3.current_page_index = self.current_page_index
        self.parent.update()  # update the parent frame after switching pages to make sure everything is up to date
        return "break"  # prevents event propagation, you don't want any events to propogate to unwanted handlers, eg: the default bindings

    # method that sets the parent bindings for the first page
    def page1_parent_bindings(self):
        # NOTE keep in mind that you're binding the parent frame, "self.parent", to the methods of the respective pages "self.page1.on_down_key"
        self.parent.bind("<Tab>", lambda event: self.page1.on_down_key(event=event))
        self.parent.bind("<Shift-Tab>", lambda event: self.page1.on_up_key(event=event))
        self.parent.bind("<Up>", lambda event: self.page1.on_up_key(event=event))
        self.parent.bind("<Down>", lambda event: self.page1.on_down_key(event=event))
        self.parent.bind("<Command-z>", lambda event: self.page1.undo_action(event=event))
        self.parent.bind("<Command-Z>", lambda event: self.page1.redo_action(event=event))
        self.parent.bind("<Command-y>", lambda event: self.page1.redo_action(event=event))
        self.parent.bind("<Command-Y>", lambda event: self.page1.redo_action(event=event))
        self.parent.bind("<Command-D>", lambda event: self.page1.activate_clearing_of_inputs(event=event))
        self.parent.bind("<Command-s>", lambda event: self.page1.start_post_save_processes(event=event))
        self.parent.bind("<Command-n>", lambda event: self.page1.when_next_button_triggered(event=event))

    def page2_parent_bindings(self):  # method that sets the parent bindings for the second page
        self.parent.bind("<Tab>", lambda event: self.page2.on_down_key(event=event))
        self.parent.bind("<Shift-Tab>", lambda event: self.page2.on_up_key(event=event))
        self.parent.bind("<Up>", lambda event: self.page2.on_up_key(event=event))
        self.parent.bind("<Down>", lambda event: self.page2.on_down_key(event=event))
        self.parent.bind("<Command-b>", lambda event: self.move_back(event=event))
        self.parent.bind("<Command-n>", lambda event: self.move_forward(event=event))
        self.parent.bind("<Command-e>", lambda event: self.page2.edit_button_click(event=event))
        self.parent.bind("<Command-d>", lambda event: self.page2.delete_button_click(event))

    def page3_parent_bindings(self):  # method that sets the parent bindings for the third page
        self.parent.bind("<Tab>", lambda event: self.page3.on_down_key(event=event))
        self.parent.bind("<Shift-Tab>", lambda event: self.page3.on_up_key(event=event))
        self.parent.bind("<Up>", lambda event: self.page3.on_up_key(event=event))
        self.parent.bind("<Down>", lambda event: self.page3.on_down_key(event=event))
        self.parent.bind("<Command-b>", lambda event: self.move_back(event=event))
        self.parent.bind("<Command-n>", lambda event: self.move_forward(event=event))
        self.parent.bind("<Command-z>", lambda event: self.page3.undo_action(event=event))
        self.parent.bind("<Command-Z>", lambda event: self.page3.redo_action(event=event))
        self.parent.bind("<Command-y>", lambda event: self.page3.redo_action(event=event))
        self.parent.bind("<Command-Y>", lambda event: self.page3.redo_action(event=event))
        self.parent.bind("<Command-s>", lambda event: self.page3.send_schedule_to_employees_button_clicked(event=event))

    def unbind_all_parent_bindings(
        self,
    ):  # method that unbinds all parent bindings when switching pages, allowing for new bindings to be set respective to the current page
        self.parent.unbind("<Tab>")
        self.parent.unbind("<Shift-Tab>")
        self.parent.unbind("<Up>")
        self.parent.unbind("<Down>")
        self.parent.unbind("<Command-b>")
        self.parent.unbind("<Command-n>")
        self.parent.unbind("<Command-e>")
        self.parent.unbind("<Command-d>")
        self.parent.unbind("<Command-z>")
        self.parent.unbind("<Command-Z>")
        self.parent.unbind("<Command-y>")
        self.parent.unbind("<Command-Y>")
        self.parent.unbind("<Command-s>")
        self.parent.unbind("<Command-D>")



    def widget_exists(self, widget): # method that checks if a widget exists
        return widget.winfo_exists()  # Attempt to access a standard attribute of the widget


root = Tk()  # create the root window
app = App(root)  # instantiate the App class
root.mainloop()  # run the mainloop of the root window
