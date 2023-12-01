from tkinter import *  # import almost everything from the tkinter module
from tkinter import font  # specify that you want to import the font module from tkinter
import json  # import the json module

from widget_creation.label_creator import CreateLabels  # import the CreateLabels class from the label_creator module
from widget_creation.button_creator import CreateButtons  # import the CreateButtons class from the button_creator module
from widget_creation.entry_creator import CreateEntries  # import the CreateEntries class from the entry_creator module

from self_made_pop_up_creation import SelfMadePopUp  # import the SelfMadePopUp class from the self_made_pop_up_creation module

START_TIME = "start_time"  # create a constant variable for the start time
END_TIME = "end_time"  # create a constant variable for the end time

from twilio.rest import Client  # import the Client class from the twilio.rest module so employers can send the final schedule to their employees via text message

# NOTE: Your Twilio account SID and authentication token, will be different from mine, so make sure you change them to your own,
# you should also put tokens like this in virtual environments for privacy

ACCOUNT_SID = ""  # your ID for your Twilio account (pretty much your username)
AUTH_TOKEN = ""  # your authentication token for your Twilio account(pretty much your password)
TWILIO_PHONE_NUMBER = "+"  # Format: '+1234567890', the employers phone number that they got from Twilio


class Page3(Frame):  # create a Page3 class that inherits from the Frame class
    def __init__(
        self,  # initialize the Page3 class and its attributes
        parent,  # pass in the parent parameter
        move_backward,  # pass in the move_backward parameter
        main_file_instance,  # pass in the main_file_instance parameter
    ):
        super().__init__(parent)  # call the __init__ method of the Frame class, passing in the parent parameter

        self.schedule_was_sent = False  # initialize a schedule_was_sent variable to False, this will be used to check if the schedule was sent to the employees

        self.move_backward_method = move_backward  # initialize a move_backward_method variable to the move_backward parameter, this will be used to move the user to the previous page

        self.main_file_instance = main_file_instance  # initialize a main_file_instance variable to the main_file_instance parameter, this will be used to access the attributes of the MainFile class

        self.instance_of_page3 = self  # initialize an instance_of_page3 variable to the instance of the Page3 class, this will be used to access the attributes of the Page3 class

        self.current_page_index = self.main_file_instance.current_page_index  # initialize a current_page_index variable to the current_page_index attribute of the MainFile class to keep track of what page the user is on

        self.list_of_all_widgets = []  # List of widgets that will be used to navigate through the program using the up and down keys and the tab and shift tab keys

        self.bg_color = "gray20"  # initialize a bg_color variable to "gray20", this will be used to set the background color of the widgets

        self.button_bg_color = "gray75"  # initialize a button_bg_color variable to "gray75", this will be used to set the background color of the buttons

        self.schedule_to_send_dict = {}  # initialize a schedule_to_send_dict variable to an empty dictionary, this will be used to store the schedule that will be sent to the employees

        self.parent = parent  # initialize a parent variable to the parent parameter, this will be used to access the attributes of the parent window

        self.screen_width = self.parent.winfo_screenwidth()  # use the winfo_screenwidth method of the parent window to get the width of the screen, set it to the screen_width attribute of the Page3 class

        self.screen_height = self.parent.winfo_screenheight()  # use the winfo_screenheight method of the parent window to get the height of the screen, set it to the screen_height attribute of the Page3 class

        self.calculate_parameters()  # call the calculate_parameters method to calculate the parameters that will affect the font and size of the widgets

        self.frame = Frame(self)  # create a frame on the Page3 class, set it to the frame attribute of the Page3 class, this frame will be placed on the parent window

        self.page3_row0_frame = Frame(self.frame)  # create a frame that will hold the widgets of the first row of the Page3 class, place this frame on the frame attribute of the Page3 class
        self.page3_row1_frame = Frame(self.frame)  # create a frame that will hold the widgets of the second row of the Page3 class, place this frame on the frame attribute of the Page3 class
        self.page3_row2_frame = Frame(self.frame)  # create a frame that will hold the widgets of the third row of the Page3 class, place this frame on the frame attribute of the Page3 class

        self.data_frame = Frame(self.frame)  # create a frame that will hold the data widgets of the Page3 class, place this frame on the frame attribute of the Page3 class

        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # place the frame on the parent window
        self.page3_row0_frame.grid(row=0, column=0, sticky=NSEW, columnspan=8, pady=5)  # place the page3_row0_frame on the frame of the Page3 class
        self.page3_row1_frame.grid(row=1, column=0, sticky=NSEW, columnspan=8, pady=5)  # place the page3_row1_frame on the frame of the Page3 class
        self.page3_row2_frame.grid(row=2, column=0, sticky=NSEW, columnspan=8, pady=5)  # place the page3_row2_frame on the frame of the Page3 class
        self.data_frame.grid(row=3, column=0, sticky=NSEW, columnspan=8)  # place the data_frame on the frame of the Page3 class

        self.employee_name_labels = []  # initialize an employee_name_labels variable to an empty list, this will be used to store the employee name labels
        self.employee_schedule_entry = None  # initialize an employee_schedule_entry variable to None, this will be used to create a entry widget that will display the schedule of the employees
        self.employee_entries = []  # initialize an employee_entries variable to an empty list, this will be used to store the employee entries

        self.dates_list = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

        self.undo_stack = []  # initialize an undo_stack variable to an empty list, this will be used to store the data that will be used to undo the last action
        self.redo_stack = []  # initialize an redo_stack variable to an empty list, this will be used to store the data that will be used to redo the last action
        self.last_widget_or_widgets_modified = None  # initialize a last_widget_or_widgets_modified variable to None, this will be used to store the last widget or widgets that were modified

        self.click_to_off_setting = None  # initialize a click_to_off_setting boolean variable to None, this will be used to store the setting of the click to off feature

        # initialize a json_data variable to the data that will be loaded from the employee_time_project_data_file.json file
        # NOTE: some methods use this variable to create some of the widgets so this line of code must be before the create_widgets method below
        self.json_data = self.load_data("employee_time_project_data_file.json")

        self.create_widgets()  # call the create_widgets method to create the widgets of the Page3 class

        self.frame.update_idletasks()  # SOMETIMES YOU NEED TO UPDATE THE IDLE TASKS BEFORE YOU CAN GET THE HEIGHT OF THE FRAME OR OTHER INFO, so it's good to update them here and there

    def button_bindings(self):  # method to bind the buttons of the Page3 class to certain methods
        # first add all the buttons to the list of all widgets so you can iterate through them later
        self.list_of_all_widgets.append(self.back_button)
        self.list_of_all_widgets.append(self.remove_am_pm_info_button)
        self.list_of_all_widgets.append(self.remove_zeros_button)
        self.list_of_all_widgets.append(self.undo_button)
        self.list_of_all_widgets.append(self.redo_button)
        self.list_of_all_widgets.append(self.reset_all_data_button)
        self.list_of_all_widgets.append(self.enable_click_to_off_button)
        self.list_of_all_widgets.append(self.disable_click_to_off_button)
        self.list_of_all_widgets.append(self.send_schedule_to_employees_button)

        for widget in self.list_of_all_widgets:  # iterate through the list of all widgets
            widget.bind("<Command-b>", lambda event: None)  # remove the default binding for the back button triggering command
            widget.bind("<Command-n>", lambda event: None)  # remove the default binding for the next button triggering command
            widget.bind("<Command-e>", lambda event: None)  # remove the default binding for the edit button triggering command
            widget.bind("<Command-d>", lambda event: None)  # remove the default binding for the delete button triggering command
            widget.bind("<Up>", lambda event: None)  # remove the default binding for the up key
            widget.bind("<Down>", lambda event: None)  # remove the default binding for the down key
            widget.bind("<Tab>", lambda event: None)  # remove the default binding for the tab key
            widget.bind("<Shift-Tab>", lambda event: None)  # remove the default binding for the shift tab key
            widget.bind("<Return>", lambda event: None)  # remove the default binding for the return key
            widget.bind("<KP_Enter>", lambda event: None)  # remove the default binding for the keypad enter key
            widget.bind("<Command-s>", lambda event: None)  # remove the default binding for the save button triggering command
            # Disable the default focus traversal of the widget's class
            widget.unbind_class(widget.winfo_class(), "<Tab>")
            widget.unbind_class(widget.winfo_class(), "<Shift-Tab>")

            widget.bind("<FocusIn>", self.on_focus_in)  # bind the focus in event of the widget to the on_focus_in method
            widget.bind("<FocusOut>", self.on_focus_out)  # bind the focus out event of the widget to the on_focus_out method

        self.back_button.bind("<Return>", lambda event: self.move_backward_method(event=event))  # bind a back button focused return key press to the move_backward_method
        self.back_button.bind("<KP_Enter>", lambda event: self.move_backward_method(event=event))  # bind a back button focused keypad enter key press to the move_backward_method
        self.back_button.bind("<Button-1>", lambda event: self.move_backward_method(event=event))  # bind a back button left mouse click to the move_backward_method

        self.remove_am_pm_info_button.bind("<Return>", lambda event: self.remove_am_pm_info(event=event))  # bind a remove am pm info button focused return key press to the remove_am_pm_info method
        self.remove_am_pm_info_button.bind("<KP_Enter>", lambda event: self.remove_am_pm_info(event=event))  # bind a remove am pm info button focused keypad enter key press to the remove_am_pm_info method
        self.remove_am_pm_info_button.bind("<Button-1>", lambda event: self.remove_am_pm_info(event=event))  # bind a remove am pm info button left mouse click to the remove_am_pm_info method

        self.remove_zeros_button.bind("<Return>", lambda event: self.remove_zeros(event=event))  # bind a remove zeros button focused return key press to the remove_zeros method
        self.remove_zeros_button.bind("<KP_Enter>", lambda event: self.remove_zeros(event=event))  # bind a remove zeros button focused keypad enter key press to the remove_zeros method
        self.remove_zeros_button.bind("<Button-1>", lambda event: self.remove_zeros(event=event))  # bind a remove zeros button left mouse click to the remove_zeros method

        self.undo_button.bind("<Return>", lambda event: self.undo_action(event=event))  # bind an undo button focused return key press to the undo_action method
        self.undo_button.bind("<KP_Enter>", lambda event: self.undo_action(event=event))  # bind an undo button focused keypad enter key press to the undo_action method
        self.undo_button.bind("<Button-1>", lambda event: self.undo_action(event=event))  # bind an undo button left mouse click to the undo_action method

        self.redo_button.bind("<Return>", lambda event: self.redo_action(event=event))  # bind a redo button focused return key press to the redo_action method
        self.redo_button.bind("<KP_Enter>", lambda event: self.redo_action(event=event))  # bind a redo button focused keypad enter key press to the redo_action method
        self.redo_button.bind("<Button-1>", lambda event: self.redo_action(event=event))  # bind a redo button left mouse click to the redo_action method

        self.reset_all_data_button.bind("<Return>", lambda event: self.reset_all_data(event=event))  # bind a reset all data button focused return key press to the reset_all_data method
        self.reset_all_data_button.bind("<KP_Enter>", lambda event: self.reset_all_data(event=event))  # bind a reset all data button focused keypad enter key press to the reset_all_data method
        self.reset_all_data_button.bind("<Button-1>", lambda event: self.reset_all_data(event=event))  # bind a reset all data button left mouse click to the reset_all_data method

        self.enable_click_to_off_button.bind("<Return>", lambda event: self.enable_click_to_off(event=event))  # bind an enable click to off button focused return key press to the enable_click_to_off method
        self.enable_click_to_off_button.bind("<KP_Enter>", lambda event: self.enable_click_to_off(event=event))  # bind an enable click to off button focused keypad enter key press to the enable_click_to_off method
        self.enable_click_to_off_button.bind("<Button-1>", lambda event: self.enable_click_to_off(event=event))  # bind an enable click to off button left mouse click to the enable_click_to_off method

        self.disable_click_to_off_button.bind("<Return>", lambda event: self.disable_click_to_off(event=event))  # bind a disable click to off button focused return key press to the disable_click_to_off method
        self.disable_click_to_off_button.bind("<KP_Enter>", lambda event: self.disable_click_to_off(event=event))  # bind a disable click to off button focused keypad enter key press to the disable_click_to_off method
        self.disable_click_to_off_button.bind("<Button-1>", lambda event: self.disable_click_to_off(event=event))  # bind a disable click to off button left mouse click to the disable_click_to_off method

        self.send_schedule_to_employees_button.bind(
            "<Return>", lambda event: self.send_schedule_to_employees_button_clicked(event=event)
        )  # bind a next button focused return key press to the send_schedule_to_employees_button_clicked method
        self.send_schedule_to_employees_button.bind("<KP_Enter>", lambda event: self.send_schedule_to_employees_button_clicked(event=event))  # do the same thing for the keypad enter key
        self.send_schedule_to_employees_button.bind(
            "<Button-1>", lambda event: self.send_schedule_to_employees_button_clicked(event=event)
        )  # bind a next button left mouse click to the send_schedule_to_employees_button_clicked method

    def on_up_key(self, event):  # method to be called when the up key or shift tab key is pressed
        widget = event.widget  # initialize a widget variable to the widget that triggered the event
        if widget in self.list_of_all_widgets:  # check if the widget is in the list of all widgets
            idx = self.list_of_all_widgets.index(widget)  # initialize an idx variable to the index of the widget in the list of all widgets
            if idx > 0:  # make sure the index is greater than 0 to prevent going up if you're already at index 0
                self.list_of_all_widgets[idx - 1].focus_set()  # set the focus to the widget above the widget that triggered the event
        return "break"  # prevent event propagation to other default bindings by returning "break" after the method is called

    def on_down_key(self, event):  # method to be called when the down key or tab key is pressed
        widget = event.widget  # initialize a widget variable to the widget that triggered the event
        if widget in self.list_of_all_widgets:  # check if the widget is in the list of all widgets
            idx = self.list_of_all_widgets.index(widget)  # if so, initialize an idx variable to the index of the widget in the list of all widgets
            if idx < len(self.list_of_all_widgets) - 1:  # make sure the index is less than the length of the list of all widgets minus 1 to prevent going down if you're already at the last index
                self.list_of_all_widgets[idx + 1].focus_set()  # set the focus to the widget below the widget that triggered the event
        return "break"  # prevent event propagation to other default bindings by returning "break" after the method is called

    def tables_navigation_bindings(self):  # method to bind the entries of the Page3 class to certain methods
        # NOTE: the colon is used to indicate that you're modifying the original list, not creating a new one
        # since when data is updated, you delete and then recreate the entries, you need to rebind the entries to the methods
        # the deletion of the widgets happens in another method, but the removing of them from the list happens here
        self.list_of_all_widgets[:] = self.list_of_all_widgets[:9]  # remove all the widgets from the list of all widngets except for the first 9 widgets, which are the buttons

        for widget in self.employee_entries:  # now iterate through the updated list of employee entries
            self.list_of_all_widgets.append(widget)  # and add each entry to the list of all widgets

        for widget in self.employee_entries:
            widget.bind("<Command-b>", lambda event: None)  # remove the default binding for the back button triggering command
            widget.bind("<Command-n>", lambda event: None)  # remove the default binding for the next button triggering command
            widget.bind("<Up>", lambda event: None)  # remove the default binding for the up key
            widget.bind("<Down>", lambda event: None)  # remove the default binding for the down key
            widget.bind("<Tab>", lambda event: None)  # remove the default binding for the tab key
            widget.bind("<Shift-Tab>", lambda event: None)  # remove the default binding for the shift tab key
            widget.bind("<Return>", lambda event: None)  # remove the default binding for the return key
            widget.bind("<KP_Enter>", lambda event: None)  # remove the default binding for the keypad enter key
            widget.bind("<Command-z>", lambda event: None)  # remove the default system binding for the undo command
            widget.bind("<Command-Z>", lambda event: None)  # remove the default system binding for the redo command
            widget.bind("<Command-y>", lambda event: None)  # remove the default system binding for the redo command
            widget.bind("<Command-Y>", lambda event: None)  # remove the default system binding for the redo command
            widget.bind("<Command-s>", lambda event: None)  # remove the default binding for the save button triggering command
            # Disable the default focus traversal
            widget.unbind_class(widget.winfo_class(), "<Tab>")
            widget.unbind_class(widget.winfo_class(), "<Shift-Tab>")

            widget.bind("<FocusIn>", self.on_focus_in)  # bind the focus in event of the widget to the on_focus_in method
            widget.bind("<FocusOut>", self.on_focus_out)  # bind the focus out event of the widget to the on_focus_out method

            # NOTE: keypress, not keyRelease is used here since the changes saved onto the undo stack have to be immediate
            # if the user holds a button then uses the mouse to click on a button that extracts the data from the entries, the data will not be the updated data after the user released the button
            widget.bind("<KeyPress>", self.on_key_press)  # bind a widget focused key press to the on_key_press method

            # the turn_time_to_off method has checks in it to make sure it only takes action if the click to off setting is enabled
            widget.bind("<Button-1>", self.turn_time_to_off)  # bind a widget left mouse click to the turn_time_to_off method
            widget.bind("<Return>", self.turn_time_to_off)  # bind a widget focused return key press to the turn_time_to_off method
            widget.bind("<KP_Enter>", self.turn_time_to_off)  # bind a widget focused keypad enter key press to the turn_time_to_off method

    def on_focus_in(self, event):  # method to be called when a widget is focused on
        event.widget.original_color = event.widget.cget("bg")  # Store the original color in the widget's original_color attribute
        if event.widget in self.employee_entries:  # check if the widget is an employee entry
            event.widget.config(bg="dark blue")  # if so, change the background color to dark blue, this is because the text in the entries is white, so you need a dark background
        else:  # if not
            event.widget.config(bg="light blue")  # change the background color to light blue, this is because the text in the entries is white, so you need a light background for contrast

    def on_focus_out(self, event):  # method to be called when a widget is focused out of
        event.widget.config(bg=event.widget.original_color)  # Reset the event widget's background color to its original color, the widget's original color is stored in the widget's original_color attribute
        self.last_item_focused_on = event.widget  # this is used to know which button was last focused on, this is used in the other methods in this class
        self.main_file_instance.pg3_current_item_focused_on = event.widget  # NOTE: Diff than the last_item_focused_on variable belonging to this class, this is used for the page switching method in the MainFile class

    def calculate_parameters(self):
        # NOTE: don't use appkit, don't use nsscreen, use winfo instead, it provides more accurate results for what you need
        self.screen_width = self.parent.winfo_screenwidth()  # use the winfo_screenwidth method of the parent window to get the width of the screen, set it to the screen_width attribute of the Page3 class
        self.screen_height = self.parent.winfo_screenheight()  # use the winfo_screenheight method of the parent window to get the height of the screen, set it to the screen_height attribute of the Page3 class

        self.screen_resolution = round(self.screen_width * self.screen_height)  # calculate the screen resolution by multiplying the screen width and screen height, this will be used to determine font size

        font_based_on_screen_size = round((self.screen_resolution / 400000))  # calculate the font based on the screen size, set it to the font_based_on_screen_size attribute of the Page3 class
        font_based_on_screen_size = round(max(min(font_based_on_screen_size, 18), 15))  # set caps on the min and max font size, set it to the font_based_on_screen_size attribute of the Page3 class

        # NOTE: self.font is not self.font_size, self.font is a font object, self.font["size"] is the font size derived from the font object
        self.font = font.Font(family="Monaco", size=font_based_on_screen_size)  # insert font size into the font object
        self.font_size = self.font["size"]  # set font size to the font size derived from the font object

        # NOTE: never round a multiplier, there's a big difference between a 1.2 and 1.4 multiplier, you don't want both rounded to 1
        # you need the multipliers to be precise
        # on a side note, values like 16 and 15 below were values chosen after playing around with different values to see which ones fit best
        self.width_multiplier = self.font_size / 16  # this will be used to determine width of widgets
        self.height_multiplier = self.font_size / 16  # this will be used to determine height of widgets
        self.padx_multiplier = self.font_size / 15  # this will be used to determine padx of widgets
        self.pady_multiplier = self.font_size / 15  # this will be used to determine pady of widgets

    def create_widgets(self):
        # NOTE: the grid attributes of buttons like height, and padding are much bigger with buttons than they are with labels or entries
        # NOTE: for pady, you only need to alter the frame pady, not the widgets, the widgets will be altered by the frame pady

        self.page_number_label = CreateLabels.create_label(  # create a page number label
            frame=self.page3_row0_frame,  # place the label on the page3_row0_frame
            font=self.font,  # set the font to the font attribute of the Page3 class
            text="Page 3",  # set the text to "Page 3"
            background=self.bg_color,  # set the background color to the bg_color attribute of the Page3 class
            row=0,  # place the label in row 0 of the page3_row0_frame
            column=0,  # place the label in column 0 of the page3_row0_frame
            highlightthickness=0,  # remove the highlightthickness by setting it to 0
            padx=round(self.padx_multiplier),  # set the padx to the padx_multiplier attribute of the Page3 class
            pady=round(self.pady_multiplier * 0),  # set the pady to the pady_multiplier attribute to 0
        )

        self.back_button = CreateButtons.create_button(  # create a back button to move the user to the previous page
            frame=self.page3_row0_frame,
            font=self.font,
            text="Go Back",
            background=self.button_bg_color,
            row=0,
            column=1,
            highlightthickness=0,
            height=round(self.height_multiplier * 32),
            width=round(self.width_multiplier * 100),
            padx=round(self.padx_multiplier * 1.5),
            pady=round(self.pady_multiplier * 1.05),
        )

        # this will remove the am/pm info in the entries on page 3 when the button is pressed
        self.remove_am_pm_info_button = CreateButtons.create_button(
            frame=self.page3_row0_frame,
            font=self.font,
            text="Remove AM/PM Info From Time Entries",
            background=self.button_bg_color,
            row=0,
            column=2,
            highlightthickness=0,
            height=round(self.height_multiplier * 32),
            width=round(self.width_multiplier * 380),
            padx=round(self.padx_multiplier * 38),
            pady=round(self.pady_multiplier * 1.05),
        )

        # this will remove the zeros in the entries on page 3 when the button is pressed
        self.remove_zeros_button = CreateButtons.create_button(
            frame=self.page3_row0_frame,
            font=self.font,
            text="Remove Zeros From Time Entries",
            background=self.button_bg_color,
            row=0,
            column=3,
            highlightthickness=0,
            height=round(self.height_multiplier * 32),
            width=round(self.width_multiplier * 330),
            padx=round(self.padx_multiplier * 38),
            pady=round(self.pady_multiplier * 1.05),
        )

        # this will put the data in the entries onto the redo stack when pressed, then undo the last change made to the data entries on page 3
        self.undo_button = CreateButtons.create_button(
            frame=self.page3_row0_frame,
            font=self.font,
            text="Undo",
            background=self.button_bg_color,
            row=0,
            column=4,
            highlightthickness=0,
            height=round(self.height_multiplier * 32),
            width=round(self.width_multiplier * 60),
            padx=round(self.padx_multiplier * 1.5),
            pady=round(self.pady_multiplier * 1.05),
        )

        # this will put the data in the entries onto the undo stack when pressed, then redo the last change made to the data entries on page 3
        self.redo_button = CreateButtons.create_button(
            frame=self.page3_row0_frame,
            font=self.font,
            text="Redo",
            background=self.button_bg_color,
            row=0,
            column=5,
            highlightthickness=0,
            height=round(self.height_multiplier * 32),
            width=round(self.width_multiplier * 60),
            padx=round(self.padx_multiplier * 1.5),
            pady=round(self.pady_multiplier * 1.05),
        )

        # this will reset all the data in the entries on page 3 to the original data that was loaded from the employee_time_project_data_file.json file
        self.reset_all_data_button = CreateButtons.create_button(
            frame=self.page3_row0_frame,
            font=self.font,
            text="Reset All Data",
            background=self.button_bg_color,
            row=0,
            column=6,
            highlightthickness=0,
            height=round(self.height_multiplier * 32),
            width=round(self.width_multiplier * 160),
            padx=round(self.padx_multiplier * 1.5),
            pady=round(self.pady_multiplier * 1.05),
        )

        # this label will display instructions on how to use the click to off feature
        self.turn_time_to_off_instructions_label = CreateLabels.create_label(
            frame=self.page3_row1_frame,
            font=self.font,
            text='Press "Enable Click to OFF", then press a time entry to convert it to "OFF".',
            background=self.bg_color,
            row=0,
            column=0,
            highlightthickness=0,
            padx=round(self.padx_multiplier * 1.05),
            pady=round(self.pady_multiplier * 1.05),
        )

        # this will allow a user to click an entry, automatically converting it to "OFF"
        self.enable_click_to_off_button = CreateButtons.create_button(
            frame=self.page3_row1_frame,
            font=self.font,
            text="Enable Click to OFF",
            background=self.button_bg_color,
            row=0,
            column=1,
            highlightthickness=0,
            height=round(self.height_multiplier * 32),
            width=round(self.width_multiplier * 220),
            padx=round(self.padx_multiplier * 1.05),
            pady=round(self.pady_multiplier * 1.05),
        )

        # this will disable the click to off feature of the enable click to off button
        self.disable_click_to_off_button = CreateButtons.create_button(
            frame=self.page3_row1_frame,
            font=self.font,
            text="Disable Click to OFF",
            background=self.button_bg_color,
            row=0,
            column=2,
            highlightthickness=0,
            height=round(self.height_multiplier * 32),
            width=round(self.width_multiplier * 230),
            padx=round(self.padx_multiplier * 1.05),
            pady=round(self.pady_multiplier * 1.05),
        )

        # this label will display instructions for what you should be doing on page 3
        self.final_instructions_label = CreateLabels.create_label(
            frame=self.page3_row2_frame,
            font=self.font,
            text="Create your final schedule below, when finished, press this button -------->",
            background=self.bg_color,
            row=0,
            column=0,
            highlightthickness=0,
            padx=round(self.padx_multiplier * 1.05),
            pady=round(self.pady_multiplier * 1.05),
        )

        # this button will send the schedule to the employees
        self.send_schedule_to_employees_button = CreateButtons.create_button(
            frame=self.page3_row2_frame,
            font=self.font,
            text="Send Schedule to Employees",
            background=self.button_bg_color,
            row=0,
            column=1,
            highlightthickness=0,
            height=round(self.height_multiplier * 32),
            width=round(self.width_multiplier * 300),
            padx=round(self.padx_multiplier * 1.05),
            pady=round(self.pady_multiplier * 1.05),
        )

        # this label will be right above the column of employee name entries
        self.employees_label = CreateLabels.create_label(
            frame=self.data_frame,
            font=self.font,
            text="EMPLOYEES",
            background=self.bg_color,
            row=0,
            column=0,
            highlightthickness=0,
            padx=round(self.padx_multiplier * 1.05),
            pady=round(self.pady_multiplier * 1.05),
        )

        # iterate through the days of the week to create a label for each day, each label will have a column of entries below it for that respective day
        for day in self.dates_list:
            self.dates_label = CreateLabels.create_label(
                frame=self.data_frame,
                font=self.font,
                text=day,
                background=self.bg_color,
                row=0,
                column=self.dates_list.index(day) + 1,
                highlightthickness=0,
                padx=round(self.padx_multiplier * 1.05),
                pady=round(self.pady_multiplier * 1.05),
            )

        self.button_bindings()  # call the button_bindings method to bind the buttons of the Page3 class to the appropriate methods
        self.create_data()  # call the create_data method to create the data widgets of the Page3 class, these will be label and entry widgets

    def send_schedule_to_employees(self):  # method to send the schedule to the employees
        # you're going to populate the schedule_to_send_dict with the data from the entries, iterating through the entries would start you from left to right, monday through sunday,
        # and then down one row to the next employee, and then left to right again. The order of employees in the entries top to down should be the same as the order of employees in the json data,
        # that's why you can simply assume that the first 0-6 index of the entries corresponds to the first employee in the json data, and the next 7-13 index of the entries corresponds to the second employee in the json data, etc.
        # that's what you'll start off with an index of 0, then add 7 to the index to get to the next employee, since there are 7 days in a week
        starting_index_of_entries = 0  # initialize a starting_index_of_entries variable to 0, this will be used to keep track of the index of the entries you're currently on
        for json_line in self.json_data:  # iterate through the json data, each line should be a dictionary of the employee's data
            json_name = json_line["employee_name"].replace("\n", "")  # initialize a json_name variable to the name of the employee, remove the newline character to ensure you don't have any extra spaces at the end
            self.schedule_to_send_dict[json_name] = {
                # set a key of the employee's name to a dictionary of the employee's phone number, remove the newline character and dashes to ensure you don't have any extra spaces or dashes, the 1 at the beginning is for the country code
                "employee_phone_number": "+1" + json_line["employee_phone_number"].replace("\n", "").replace("-", ""),
                # now create a key of the employee's schedule, this will be a dictionary of the days of the week, each day will have a value of the start-end time for that work day
                # remove the newline character to ensure you don't have any extra spaces at the ends and remove any unnecessary spaces in the middle
                "employee_schedule": {
                    "Mon": self.employee_entries[starting_index_of_entries].get().replace("\n", "").replace(" ", ""),
                    "Tue": self.employee_entries[starting_index_of_entries + 1].get().replace("\n", "").replace(" ", ""),
                    "Wed": self.employee_entries[starting_index_of_entries + 2].get().replace("\n", "").replace(" ", ""),
                    "Thu": self.employee_entries[starting_index_of_entries + 3].get().replace("\n", "").replace(" ", ""),
                    "Fri": self.employee_entries[starting_index_of_entries + 4].get().replace("\n", "").replace(" ", ""),
                    "Sat": self.employee_entries[starting_index_of_entries + 5].get().replace("\n", "").replace(" ", ""),
                    "Sun": self.employee_entries[starting_index_of_entries + 6].get().replace("\n", "").replace(" ", ""),
                },
            }
            starting_index_of_entries += 7  # you add 7 to the starting_index_of_entries variable to get to the next employee, since there are 7 days in a week

        for employee in self.schedule_to_send_dict:  # iterate through each employee in the schedule_to_send_dict to create new variables for ease of use, then use these variables to create the message body
            number_to_send_to = self.schedule_to_send_dict[employee]["employee_phone_number"]  # initialize a number_to_send_to variable to the employee's phone number
            mon_schedule = self.schedule_to_send_dict[employee]["employee_schedule"]["Mon"]  # initialize a mon_schedule variable to the employee's monday schedule
            tue_schedule = self.schedule_to_send_dict[employee]["employee_schedule"]["Tue"]  # initialize a tue_schedule variable to the employee's tuesday schedule
            wed_schedule = self.schedule_to_send_dict[employee]["employee_schedule"]["Wed"]  # initialize a wed_schedule variable to the employee's wednesday schedule
            thu_schedule = self.schedule_to_send_dict[employee]["employee_schedule"]["Thu"]  # initialize a thu_schedule variable to the employee's thursday schedule
            fri_schedule = self.schedule_to_send_dict[employee]["employee_schedule"]["Fri"]  # initialize a fri_schedule variable to the employee's friday schedule
            sat_schedule = self.schedule_to_send_dict[employee]["employee_schedule"]["Sat"]  # initialize a sat_schedule variable to the employee's saturday schedule
            sun_schedule = self.schedule_to_send_dict[employee]["employee_schedule"]["Sun"]  # initialize a sun_schedule variable to the employee's sunday schedule

            message_body = (  # initialize a message_body variable to the message you want to send to the employee
                f"\nYour schedule for this week, {employee}: \n\n"  # insert the employee's name into the first line of the message, use the double newline character to create a space between the name and the schedule
                f"Mon: {mon_schedule}\n\n"  # insert the employee's monday schedule into the message
                f"Tue: {tue_schedule}\n\n"  # insert the employee's tuesday schedule into the message
                f"Wed: {wed_schedule}\n\n"  # insert the employee's wednesday schedule into the message
                f"Thu: {thu_schedule}\n\n"  # insert the employee's thursday schedule into the message
                f"Fri: {fri_schedule}\n\n"  # insert the employee's friday schedule into the message
                f"Sat: {sat_schedule}\n\n"  # insert the employee's saturday schedule into the message
                f"Sun: {sun_schedule}"  # insert the employee's sunday schedule into the message
            )
            # the try block is inside the for loop because you want to send the message to each employee, even if an error occurs when sending the message to one of the employees
            try:  # user a try except block to catch any errors that may occur when sending the message
                client = Client(ACCOUNT_SID, AUTH_TOKEN)  # create a Client object from the Client class, this is what you'll use to send the text message to your employees
                message = client.messages.create(body=message_body, from_=TWILIO_PHONE_NUMBER, to=number_to_send_to)  # use the twilio client to send the message to the employee's phone number
                self.schedule_was_sent = True  # if the message was sent, set the schedule_was_sent attribute of the Page3 class to True
            except Exception as e:  # if an error occurs when sending the message
                print(f"Failed to send message to {number_to_send_to}. Error: {e}")  # print the error to the console

    def yes_pressed(self, event):  # method triggered if the user presses yes on the pop up asking them if they want to send the schedule to the employees
        self.pop_up_in_focus.popup.grab_release()  # release the grab on the pop up, since the user pressed yes, you don't want the pop up to be in focus anymore

        self.pop_up_in_focus.popup.withdraw()  # then close the pop up since you're no longer using it

        self.send_schedule_to_employees()  # noq call the send_schedule_to_employees method to send the schedule to the employees

        if self.schedule_was_sent:  # check if the schedule was sent boolean is True, if so, you want to display a pop up saying the schedule was sent
            message = "Your schedule has been sent!"  # set the message to the schedule has been sent
        else:  # if the schedule was not sent, you want to display a pop up saying the schedule was not sent
            message = "ERROR: Your schedule could NOT be sent!"  # set the message to the schedule could not be sent

            self.pop_up_in_focus = SelfMadePopUp(  # then create the pop up
                title=None,
                message=f"\n{message}\n",  # set the message to the message variable
                height=3,
                width=50,
                font=self.font,
                row=0,
                col=0,
                padx=5,
                pady=5,
                cspan=1,  # you want this to be 1 if you're using the okay button version, since there isnt 2 columns, one for a yes button and one for a no button for this pop up
                bg_color=self.bg_color,
                okay_button_version=True,  # set the okay_button_version to True, this will tell the SelfMadePopUp class to create a pop up with an okay button instead of a yes and no button
                okay_command=lambda event: self.no_pressed(
                    event=event
                ),  # since pressing okay on this pop up simply closes it, you can set it to the no_pressed method, which essentially does the same thing if the user presses no on the yes/no pop up version
            )
            self.pop_up_in_focus.popup.grab_set()  # grab the pop up so the user can't interact with the program until they close the pop up

    def no_pressed(self, event):  # method triggered if the user presses no on the pop up asking them if they want to send the schedule to the employees
        self.pop_up_in_focus.popup.grab_release()  # release the grab on the pop up, since the user pressed no, you don't want the pop up to be in focus anymore
        self.pop_up_in_focus.popup.withdraw()  # then close the pop up since you're no longer using it

        if self.last_item_focused_on and self.widget_exists(self.last_item_focused_on):  # check if the last item focused on is not None and if the widget still exists
            self.last_item_focused_on.focus_set()  # if so, set the focus to the last item focused on, since you're no longer focused on anything from the pop up
        else:  # if the last item focused on is None or the widget no longer exists
            self.back_button.focus_set()  # set the focus to the back button since there's nothing else to focus on, the back button serves as the default widget to focus on for this page

    def widget_exists(self, widget):
        try:
            widget.winfo_exists()  # Attempt to access a standard attribute of the widget
            return True
        except TclError:
            return False  # If an error is raised, the widget does not exist

    def create_data(self):  # method to create the data widgets of the Page3 class, these will be label and entry widgets
        for employee in self.json_data:  # iterate through the json data, each line should be a dictionary of the employee's data
            employee_name = employee["employee_name"].replace(
                "\n", ""
            )  # initialize an employee_name variable to the name of the employee, remove the newline character to ensure you don't have any extra spaces at the end
            # now create the employee name label by inserting the employee_name variable into the text of the label
            self.employee_name_label = CreateLabels.create_label(
                frame=self.data_frame,
                font=self.font,
                text=employee_name,
                background=self.bg_color,
                row=self.json_data.index(employee) + 1,
                column=0,
                highlightthickness=0,
                width=round(self.width_multiplier * 21),
                padx=round(self.padx_multiplier * 1.05),
                pady=round(self.pady_multiplier * 5),
            )
            self.employee_name_labels.append(self.employee_name_label)  # then append the label to the employee_name_labels list

        for index, employee in enumerate(self.json_data):  # now do the same thing but for the schedule entries of each employee
            employee_schedule = employee["employee_schedule"]  # initialize an employee_schedule variable to the schedule of the employee

            for day_index, day in enumerate(self.dates_list):  # iterate through the dates list, each date should be a day of the week
                self.employee_schedule_entry = CreateEntries.create_entry(
                    frame=self.data_frame,
                    font=self.font,
                    background=None,
                    row=index + 1,
                    column=day_index + 1,
                    justify=CENTER,
                    highlightthickness=0,
                    width=round(self.width_multiplier * 17),
                    padx=round(self.padx_multiplier * 1.05),
                    pady=round(self.pady_multiplier * 5),
                )

                if employee_schedule[day][START_TIME] == "OFF":  # if the start time for the current day is "OFF"
                    # insert "OFF" into the entry widget because an "OFF" in the start time would indicate that the end time is also "OFF", so the entire label should be "OFF"
                    self.employee_schedule_entry.insert(0, "OFF")
                else:  # if the start time for the current day is not "OFF"
                    self.employee_schedule_entry.insert(0, f"{employee_schedule[day][START_TIME]}-{employee_schedule[day][END_TIME]}")  # insert the start and end times into the entry widget

                self.employee_entries.append(self.employee_schedule_entry)  # then append the entry widget to the employee_entries list

            self.undo_stack = []  # now that you've created the data, you need to initialize the undo stack, this is done by setting it to an empty list
            self.redo_stack = []  # now that you've created the data, you need to initialize the redo stack, this is done by setting it to an empty list

        self.tables_navigation_bindings()  # now that you've created the data, you need to bind the entries to the appropriate methods

    def send_schedule_to_employees_button_clicked(self, event):  # method to be called when the send_schedule_to_employees_button is clicked
        self.pop_up_in_focus = SelfMadePopUp(
            title=None,
            message=f"\nARE YOU SURE YOU WANT TO SEND THIS\n SCHEDULE TO YOUR EMPLOYEES?",  # ask the user if they're sure they want to send the schedule to the employees
            height=4,
            width=50,
            font=self.font,
            row=0,
            col=0,
            padx=5,
            pady=5,
            cspan=2,  # you want this to be 2 if you're using the yes/no button version of the popup class, since there are 2 columns, one for a yes button and one for a no button for this pop up
            bg_color=self.bg_color,
            yes_command=lambda event: self.yes_pressed(event=event),  # bind the yes button to the yes_pressed method
            no_command=lambda event: self.no_pressed(event=event),  # bind the no button to the no_pressed method
        )
        self.pop_up_in_focus.popup.grab_set()  # grab the pop up so the user can't interact with the program until they close the pop up

    def load_data(self, file_path):  # method to load the data from the json file
        try:  # try to open the json file
            with open(file_path, "r") as file:  # open the json file, set it as the file variable
                data = json.load(file)  # load the data from the json file into the data variable
            return data  # return the data variable
        except FileNotFoundError:  # if the json file is not found
            print("No file found")  # print "No file found"
            return None  # then return None

    def update_data(self, json_data):  # method to update the data widgets of the Page3 class
        # the json_data parameter method represents the data straight from the json file, while the self.json_data attribute represents the data of the data widgets on page 3
        # that's why you need to check if they're not equal first, cause if they are, then you don't need to update the data widgets
        if self.json_data != json_data:
            for name_label in self.employee_name_labels:  # if the json_data and self.json_data are not equal, then you need to update the data widgets
                name_label.destroy()  # first destroy all the name labels

            for entry in self.employee_entries:  # then destroy all the entries
                entry.destroy()

            self.employee_entries = []  # destroying a widget is not the same as removing it from a list, so you need to empty the employee_entries as well

            self.json_data = json_data  # now update the json_data attribute of the Page3 class to the json_data parameter of the update_data method

            self.create_data()  # now that the json_data attribute of the Page3 class has been updated, you can create the data widgets again

            # one of the things the self.create_data() above did was populated the self.employee_name_labels with the updated data from the json file, so you can use that to update the schedule_to_send_dict
            # create a list of keys to delete from the schedule_to_send_dict, these keys are the names of the employees that are no longer in the json_data
            keys_to_delete = [key for key in self.schedule_to_send_dict if key not in [label.cget("text") for label in self.employee_name_labels]]

            for key in keys_to_delete:
                del self.schedule_to_send_dict[key]  # now iterate through the keys_to_delete list and delete the keys from the schedule_to_send_dict

            self.undo_stack = []  # now that you've updated the data, you need to initialize the undo stack, this is done by setting it to an empty list
            self.redo_stack = []  # now that you've updated the data, you need to initialize the redo stack, this is done by setting it to an empty list

    def reset_all_data(self, event):  # method to reset all the data widgets to the original data that was loaded from the employee_time_project_data_file.json file when the reset_all_data_button is pressed
        list_widgets_cleared = []  # initialize a list_widgets_cleared list, this will be used to store the widgets content before it's cleared, this is used for the undo and redo stacks
        for index, widget in enumerate(self.employee_entries):  # iterate through the employee_entries list, each entry should be a entry widget
            content = widget.get()  # initialize a content variable to the content of the entry widget
            list_widgets_cleared.append((index, content))  # get the index and content of the widget from the employee_entries list and append it to the list_widgets_cleared list

        if list_widgets_cleared:  # if the list containing the index/content of widgets cleared is populated, then you can append it to the undo stack
            if self.undo_stack and list_widgets_cleared != self.undo_stack[-1]:  # first, check that you're not appending the same data to the undo stack, if you are, then you don't need to append it again
                self.undo_stack.append(list_widgets_cleared)  # if you're not appending the same data to the undo stack, then you can append it to the undo stack
            elif not self.undo_stack:  # if the undo stack is empty, then you can append the data to the undo stack since there's no way for it to be the same as the data already in the undo stack
                self.undo_stack.append(list_widgets_cleared)

        self.redo_stack = []  # now that you've appended the list_widgets_cleared list to the undo stack, you can set the redo stack to an empty list since you can't redo anything after resetting all the data

        # now that you cleared the data widgets of their content, you have to repopulate them with the original data from the json file
        entry_widget_index = 0  # for the first employee, the values will go from 0-6, for the second employee, the values will go from 7-13, for the third employee, the values will go from 14-20, etc.
        for employee in self.json_data:  # iterate through the json data, each line should be a dictionary of the employee's data
            employee_schedule = employee["employee_schedule"]  # extract the schedule of the current employee

            for day in self.dates_list:  # iterate through the dates list, each date should be a day of the week
                entry = self.employee_entries[entry_widget_index]  # get the entry widget from the employee_entries list you're currently on
                # next you'll have to clear that entry widget just in case the user typed something into it before pressing the reset all data button
                entry.delete(0, END)  # clear the entry widget from start to end

                # after clearing the entry widget, you can repopulate it with the original data from the json file
                if employee_schedule[day][START_TIME] == "OFF":  # first check if the start time for the current day is "OFF"
                    entry.insert(END, "OFF")  # if it is, then insert "OFF" into the entry widget because an "OFF" in the start time would indicate that the end time is also "OFF", so the entire label should be "OFF"
                else:  # if the start time for the current day is not "OFF", then you can insert the start and end times into the entry widget
                    entry.insert(END, f"{employee_schedule[day][START_TIME]}-{employee_schedule[day][END_TIME]}")

                entry_widget_index += 1  # increment the entry_widget_index by 1 to get to the next entry widget for this employee

    def remove_am_pm_info(self, event):  # method to remove the am/pm info from the entries on page 3 when the remove_am_pm_info_button is pressed
        list_am_pm_widgets_changed = []  # initialize a list_am_pm_widgets_changed list, this will be used to store the widgets content before it's changed, this is used for the undo and redo stacks
        for index, widget in enumerate(self.employee_entries):  # iterate through the employee_entries list, each entry should be a entry widget
            content = widget.get()  # initialize a content variable to the content of the entry widget

            if "AM" in content or "PM" in content or "am" in content or "pm" in content:  # check if the content of the entry widget contains "AM" or "PM" or "am" or "pm"
                list_am_pm_widgets_changed.append((index, widget.get()))  # if it does, then append the index and content of the widget from the employee_entries list to the list_am_pm_widgets_changed list

                updated_content = content.replace("AM", "").replace("PM", "").replace("am", "").replace("pm", "")  # remove the "AM" and "PM" and "am" and "pm" from the content of the entry widget

                widget.delete(0, "end")  # now clear the entry widget from start to end just in case the user typed something into it before pressing the remove_am_pm_info_button

                widget.insert(0, updated_content)  # then insert the updated_content into the entry widget, this is the content of the entry widget with the "AM" and "PM" and "am" and "pm" removed

        if list_am_pm_widgets_changed:  # if the list containing the index/content of widgets changed is populated, then you can append it to the undo stack
            if self.undo_stack and list_am_pm_widgets_changed != self.undo_stack[-1]:  # first, check that you're not appending the same data to the undo stack, if you are, then you don't need to append it again
                self.undo_stack.append(list_am_pm_widgets_changed)  # if you're not appending the same data to the undo stack, then you can append it to the undo stack
            elif not self.undo_stack:  # if the undo stack is empty, then you can append the data to the undo stack since there's no way for it to be the same as the data already in the undo stack
                self.undo_stack.append(list_am_pm_widgets_changed)

    def remove_zeros(self, event):  # method to remove the zeros in the entries on page 3 when the remove_zeros_button is pressed
        # ensure you use int in this method, not round, since you're dealing with integers, not floats
        list_am_pm_widgets_changed = []  # initialize a list_am_pm_widgets_changed list, this will be used to store the widgets content before it's changed, this is used for the undo and redo stacks
        for index, widget in enumerate(self.employee_entries):  # iterate through the employee_entries list, each entry should be a entry widget
            content = widget.get()  # initialize a content variable to the content of the entry widget
            if "0" in content:  # check if the content of the entry widget contains a "0"
                list_am_pm_widgets_changed.append((index, widget.get()))  # if it does, then append the index and content of the widget from the employee_entries list to the list_am_pm_widgets_changed list
                times = content.split("-")  # split the content of the entry widget by the hyphen, this will give you a list of two times, the start time and the end time
                new_times = []  # initialize a new_times list, this will be used to store the updated times
                for time in times: # iterate through the times list, each time should be a start time or an end time
                    time_components = time.split(":") # split the time by the colon, this will give you a list of the hour and minute components of the time
                    hour = 0 # initialize an hour variable to 0
                    minute = 0 # initialize a minute variable to 0
                    meridiem = "" # initialize a meridiem variable to an empty string

                    # Check if hour component exists and process it
                    if len(time_components) > 0:
                        hour = int(time_components[0])

                    # Check if minute component exists and process it
                    if len(time_components) > 1:
                        if "AM" in time_components[1] or "PM" in time_components[1]:
                            # Extract and process minute, limit to two digits
                            minute = int(time_components[1][:-2][:2])
                            meridiem = time_components[1][-2:]  # Extract AM or PM
                        else:
                            # Limit minute to two digits if no meridiem
                            minute = int(time_components[1][:2])

                    # Create new time string based on available components
                    if meridiem:
                        # If meridiem exists, format accordingly
                        new_time = f"{hour}{meridiem}" if minute == 0 else f"{hour}:{minute:02d}{meridiem}"
                    else:
                        # If no meridiem, just format hour and minute
                        new_time = f"{hour}" if minute == 0 else f"{hour}:{minute:02d}"

                    new_times.append(new_time)  # after you've created the new time string, you can append it to the new_times list

                updated_content = "-".join(new_times)  # now you can join the new_times list by the hyphen to create the updated_content string eg: 9:00AM-5:00PM

                widget.delete(0, "end")  # now clear the entry widget from start to end just in case the user typed something into it before pressing the remove_zeros_button
                widget.insert(0, updated_content)  # then insert the updated_content into the entry widget, this is the content of the entry widget with the zeros removed

        if list_am_pm_widgets_changed:  # if the list containing the index/content of widgets changed is populated, then you can append it to the undo stack
            if self.undo_stack and list_am_pm_widgets_changed != self.undo_stack[-1]:  # first, check that you're not appending the same data to the undo stack, if you are, then you don't need to append it again
                self.undo_stack.append(list_am_pm_widgets_changed)  # if you're not appending the same data to the undo stack, then you can append it to the undo stack
            elif not self.undo_stack:  # if the undo stack is empty, then you can append the data to the undo stack since there's no way for it to be the same as the data already in the undo stack
                self.undo_stack.append(list_am_pm_widgets_changed)

    def turn_time_to_off(self, event):  # method to turn the time to off when the turn_time_to_off_button is pressed
        # the structure of this method is going to be simpler than the methods triggered by pressing the remove_am_pm_info_button and the remove_zeros_button because those methods can change the content of multiple widgets at once
        # while this method can only change the content of one widget at a time
        if self.click_to_off_setting:  # check if the click_to_off_setting is True, if it is, then you can turn clicked entry widgets to "OFF"
            current_widget = event.widget  # initialize a current_widget variable to the widget that was clicked on

            for index, employee_entry in enumerate(self.employee_entries):  # iterate through the employee_entries list, each entry should be a entry widget
                if current_widget == employee_entry:  # check if the clicked widget is the same as widget you're currently iterating through
                    list_widget_changed = []  # is yes, initialize a list_widget_changed list, this will be used to store the widgets content before it's changed, this is used for the undo and redo stacks
                    list_widget_changed.append((index, current_widget.get()))  # then append the index and content of the widget from the employee_entries list to the list_widget_changed list
                    self.undo_stack.append(list_widget_changed)  # now that you've appended the list_widget_changed list to the undo stack, you can append the list_widget_changed list to the undo stack

                    current_widget.delete(0, END)  # now clear the entry widget from start to end just in case the user typed something into it before pressing the turn_time_to_off_button
                    current_widget.insert(0, "OFF")  # then insert "OFF" into the entry widget

    def undo_action(self, event):  # method to undo the last action when the undo_button is pressed
        if self.undo_stack != []:  # check if the undo stack is not empty
            self.last_widget_or_widgets_modified = self.undo_stack.pop()  # if the undo stack is not empty, then you can pop the last widget or widgets modified from the undo stack

            for widget_index, widget_content_link in enumerate(self.employee_entries):  # iterate through the employee_entries list, each entry should be a entry widget
                for modified_widget in self.last_widget_or_widgets_modified:  # iterate through the last widget or widgets modified
                    modified_widget_index = modified_widget[0]  # get the index of the modified widget
                    modified_widget_content = modified_widget[1]  # get the content of the modified widget

                    if widget_index == modified_widget_index:  # check if the index of the widget you're currently iterating through is the same as the index of the modified widget
                        list_undo_widgets_changed = []  # initialize a list_undo_widgets_changed list, this will be used to store the widgets content before it's changed, this is used for the redo stack
                        # then append the index and content of the widget from the employee_entries list to the list_undo_widgets_changed list
                        list_undo_widgets_changed.append((widget_index, widget_content_link.get()))
                        self.employee_entries[widget_index].delete(0, END)  # now clear the entry widget from start to end just in case the user typed something into it before pressing the undo_button
                        self.employee_entries[widget_index].insert(0, modified_widget_content)  # then insert the modified_widget_content into the entry widget

                        if list_undo_widgets_changed:  # if the list containing the index/content of widgets changed is populated, then you can append it to the redo stack
                            # first, check that you're not appending the same data to the redo stack, if you are, then you don't need to append it again
                            if self.redo_stack and list_undo_widgets_changed != self.redo_stack[-1]:
                                self.redo_stack.append(list_undo_widgets_changed)  # if you're not appending the same data to the redo stack, then you can append it to the redo stack
                            elif not self.redo_stack:  # if the redo stack is empty, then you can append the data to the redo stack since there's no way for it to be the same as the data already in the redo stack
                                self.redo_stack.append(list_undo_widgets_changed)

    def redo_action(self, event):  # method to redo the last action when the redo_button is pressed
        if self.redo_stack != []:  # check if the redo stack is not empty
            self.last_widget_or_widgets_modified = self.redo_stack.pop()  # if the redo stack is not empty, then you can pop the last widget or widgets modified from the redo stack
            for widget_index, widget_content_link in enumerate(self.employee_entries):  # iterate through the employee_entries list, each entry should be a entry widget
                for modified_widget in self.last_widget_or_widgets_modified:  # iterate through the last widget or widgets modified
                    modified_widget_index = modified_widget[0]  # get the index of the modified widget
                    modified_widget_content = modified_widget[1]  # get the content of the modified widget

                    if widget_index == modified_widget_index:  # check if the index of the widget you're currently iterating through is the same as the index of the modified widget
                        list_redo_widgets_changed = []  # initialize a list_redo_widgets_changed list, this will be used to store the widgets content before it's changed, this is used for the undo stack
                        # then append the index and content of the widget from the employee_entries list to the list_redo_widgets_changed list
                        list_redo_widgets_changed.append((widget_index, widget_content_link.get()))
                        self.employee_entries[widget_index].delete(0, END)  # now clear the entry widget from start to end just in case the user typed something into it before pressing the redo_button
                        self.employee_entries[widget_index].insert(0, modified_widget_content)  # then insert the modified_widget_content into the entry widget

                        if list_redo_widgets_changed:  # if the list containing the index/content of widgets changed is populated, then you can append it to the undo stack
                            # first, check that you're not appending the same data to the undo stack, if you are, then you don't need to append it again
                            if self.undo_stack and list_redo_widgets_changed != self.undo_stack[-1]:
                                self.undo_stack.append(list_redo_widgets_changed)  # if you're not appending the same data to the undo stack, then you can append it to the undo stack
                            elif not self.undo_stack:  # if the undo stack is empty, then you can append the data to the undo stack since there's no way for it to be the same as the data already in the undo stack
                                self.undo_stack.append(list_redo_widgets_changed)

    def on_key_press(self, event):  # method to be called when a key is pressed on page 3
        widget = event.widget  # initialize a widget variable to the widget that was focused on when the key was pressed

        if type(widget) == Entry:  # check if the widget is an entry widget, you're only really checking for entry widgets on page 3 for undo/redo purposes
            for index, employee_entry in enumerate(self.employee_entries):  # iterate through the employee_entries list, each entry should be a entry widget
                if widget == employee_entry:
                    list_widget_changed = []  # if it is, initialize a list_widget_changed list, this will be used to store the widgets content before it's changed, this is used for the undo stack

                    list_widget_changed.append((index, widget.get()))  # then append the index and content of the widget from the employee_entries list to the list_widget_changed list

                    if list_widget_changed:  # if the list containing the index/content of widgets changed is populated, then you can append it to the undo stack
                        if self.undo_stack and list_widget_changed != self.undo_stack[-1]:  # first, check that you're not appending the same data to the undo stack, if you are, then you don't need to append it again
                            self.undo_stack.append(list_widget_changed)  # if you're not appending the same data to the undo stack, then you can append it to the undo stack
                        elif not self.undo_stack:  # if the undo stack is empty, then you can append the data to the undo stack since there's no way for it to be the same as the data already in the undo stack
                            self.undo_stack.append(list_widget_changed)

    def enable_click_to_off(self, event):  # method to enable the click_to_off_setting when the enable_click_to_off_button is pressed
        self.click_to_off_setting = True  # set the click_to_off_setting to True
        self.enable_click_to_off_button.config(highlightbackground="red")  # change the highlightbackground of the enable_click_to_off_button to red so the user knows it's enabled
        self.disable_click_to_off_button.config(highlightbackground="gray20")  # change the highlightbackground of the disable_click_to_off_button to gray20 so the user knows it's disabled

    def disable_click_to_off(self, event):  # method to disable the click_to_off_setting when the disable_click_to_off_button is pressed
        self.click_to_off_setting = False  # set the click_to_off_setting to False
        self.disable_click_to_off_button.config(highlightbackground="red")  # change the highlightbackground of the disable_click_to_off_button to red so the user knows it's enabled
        self.enable_click_to_off_button.config(highlightbackground="gray20")  # change the highlightbackground of the enable_click_to_off_button to gray20 so the user knows it's disabled
