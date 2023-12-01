from tkinter import *  # import almost everything from tkinter module

from tkinter import font  # special import for font

import json  # import json module

from widget_creation.label_creator import CreateLabels  # import CreateLabels class from label_creator.py

from widget_creation.button_creator import CreateButtons  # import CreateButtons class from button_creator.py

from self_made_pop_up_creation import SelfMadePopUp  # import SelfMadePopUp class from self_made_pop_up_creation.py

from dual_table_creation import DualTableCreation  # import DualTableCreation class from dual_table_creation.py

START_TIME = "start_time"  # create constant for start time
END_TIME = "end_time"  # create constant for end time


class Page2(Frame):  # create Page2 class that inherits from Frame class
    def __init__(
        self,  # self is the instance of the Page2 class
        parent,  # parent is the root window
        move_forward,  # move_forward is the method that moves the user to the next page
        move_backward,  # move_backward is the method that moves the user to the previous page
        page1_instance,  # page1_instance is the instance of the Page1 class
        main_file_instance,  # NOTE: THIS IS THE MAIN FILE INSTANCE
    ):
        # call the __init__ method of the Frame class to help create the Page2 class since it uses aspects of the Frame class
        super().__init__(parent)

        self.dual_table_creation_instance = DualTableCreation()  # create an instance of the DualTableCreation class to later call its methods

        # remember to use the pop_in variable of this class variable to know which pop up window is in focus
        self.pop_up_in_focus = None

        # NOTE: this is used to know which button was last focused on
        self.last_item_focused_on = None

        # initialize the instance of the Page2 class to itself
        self.instance_of_page2 = self

        # this is used to know which page you're on
        self.current_page_index = 1

        # initialize the parent of the Page2 class to the root window
        self.parent = parent

        # use the winfo_screenwidth and winfo_screenheight methods to get the width and height of the screen
        self.screen_width = self.parent.winfo_screenwidth()
        self.screen_height = self.parent.winfo_screenheight()

        # call the calculate_parameters method to calculate the font size and the width and height multipliers
        self.calculate_parameters()

        # initialize a main_file_instance variable to the main_file_instance parameter
        self.main_file_instance = main_file_instance

        # initialize a page1_instance variable to the page1_instance parameter
        self.page1_instance = page1_instance

        # initialize a dict_of_dates variable to the dates_dictionary attribute of the page1_instance, which you'll use to create the data widgets
        self.dict_of_dates = self.page1_instance.dates_dictionary

        # initialize a frame variable to a Frame widget that is a child of the Page2 class(the self variable refers to the parent, here being the Page2 class)
        self.frame = Frame(self)

        # initialize a row0_frame variable to a Frame widget that is a child of the frame variable, you need the frame class to create frames
        self.row0_frame = Frame(self.frame)
        # initialize a row1_frame variable to a Frame widget that is a child of the frame variable
        self.row1_frame = Frame(self.frame)
        # initialize a data_frame variable to a Frame widget that is a child of the frame variable
        self.data_frame = Frame(self.frame)

        # use the grid method to place the row0_frame, row1_frame, and data_frame widgets on the frame widget
        self.row0_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0, columnspan=3)
        self.row1_frame.grid(row=1, column=0, sticky=NSEW, padx=0, pady=1, columnspan=2)
        self.data_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=0, pady=0)

        # update tasks that are not always updated, this is important when you need to get the height of a widget
        self.frame.update_idletasks()

        # use the grid method to place the frame widget on the parent window
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # initialize a bg_color variable to the background color of the page2 class
        self.bg_color = "gray20"

        # this is used to keep track of the table widgets created, so you can delete them and recreate them
        self.employee_tables_list = []

        # initialize move_forward_method and move_backward_method variables to the move_forward and move_backward parameters
        self.move_forward_method = move_forward
        self.move_backward_method = move_backward

        # initialize a dates_list variable to a list of the dates of the week
        self.dates_list = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

        # initialize variables to keep track of which employee is in the edit or delete sequence
        self.employee_to_edit = None
        self.employee_to_delete = None

        # initialize a json_data variable to the data in the json file
        self.json_data = self.load_data("employee_time_project_data_file.json")

        self.list_of_all_widgets = []  # List of widgets to navigate through

        self.create_widgets()  # call the create_widgets method to create the widgets on the Page2 class

        self.frame.update_idletasks()  # update idle tasks again

    # NOTE: this method focuses on highlighting ONLY the widgets that are in the employee_tables_list
    # These data widgets will ALSO use highlightcolor in addition to highlightbackground, this is because highlightbackground is used to determine which widget was clicked
    # while highlightcolor is simply used for visibility, since highlightbackground's red outline isnt very visible
    def data_table_widget_page2_button_click(self, event):  # method to be called when the user clicks on a data widget on page 2
        event.widget.focus_set()  # Focus on the widget that was clicked

        widget_clicked = event.widget  # initialize a widget_clicked variable to the widget that was clicked

        widget_clicked.config(highlightbackground="red")  # configure the widget that was clicked to have a red HIGHLIGHTBACKGROUND color

        # HIGHLIGHT is used only for visibility, it's not used to determine which widget was clicked, all other widgets in this program only use HIGHLIGHTBACKGROUND
        widget_clicked.config(highlightcolor="red")  # ALSO configure the widget that was clicked to have a red HIGHLIGHT color

        # Loop through all widgets and configure those that were not clicked
        for widget in self.employee_tables_list:  # loop through the widgets in the employee_tables_list
            if widget != widget_clicked:  # if the widget being looped through is not the widget that was clicked
                widget.config(highlightbackground="gray20")  # configure the widget to have the original HIGHLIGHTBACKGROUND color
                # HIGHLIGHT is used only for visibility, it's not used to determine which widget was clicked, all other widgets in this program only use HIGHLIGHTBACKGROUND
                widget.config(highlightcolor="gray20")  # ALSO configure the widget to have the original HIGHLIGHT color

    def on_up_key(self, event):  # method triggered by up key or shift tab
        widget = event.widget  # get the last widget that was focused on
        if widget in self.list_of_all_widgets:  # if the widget is in the list of all widgets
            idx = self.list_of_all_widgets.index(widget)  # get the index of the widget
            if idx > 0:  # check if the index of the widget is greater than 0
                self.list_of_all_widgets[idx - 1].focus_set()  # set the focus to the widget above it
        return "break"  # prevents event propagation which might lead to unintended default behavior

    def on_down_key(self, event):  # method triggered by down key or tab
        widget = event.widget  # get the last widget that was focused on
        if widget in self.list_of_all_widgets:  # if the widget is in the list of all widgets
            idx = self.list_of_all_widgets.index(widget)  # get the index of the widget
            if idx < len(self.list_of_all_widgets) - 1:  # makes sure the current widget is not the last widget in the list
                self.list_of_all_widgets[idx + 1].focus_set()  # set the focus to the widget below it
        return "break"  # prevents event propagation which might lead to unintended default behavior

    def tables_navigation_bindings(self):  # method to bind the widgets in the employee_tables_list
        # NOTE: the colon in the list below indicates that you're modifying the original list, otherwise you would just be creating a new list with that expression
        self.list_of_all_widgets[:] = self.list_of_all_widgets[:4]

        for widget in self.employee_tables_list:  # loop through the widgets in the employee_tables_list
            self.list_of_all_widgets.append(widget)  # add the widget to the list of all widgets

        for widget in self.employee_tables_list:  # loop through the widgets in the employee_tables_list
            widget.bind("<Command-b>", lambda event: None)  # remove the default bindings for the back button triggering command
            widget.bind("<Command-n>", lambda event: None)  # remove the default bindings for the next button triggering command
            widget.bind("<Command-e>", lambda event: None)  # remove the default bindings for the edit button triggering command
            widget.bind("<Command-D>", lambda event: None)  # remove the default bindings for the delete button triggering command
            widget.bind("<Up>", lambda event: None)  # remove the default bindings for the up key triggering command
            widget.bind("<Down>", lambda event: None)  # remove the default bindings for the down key triggering command
            widget.bind("<Tab>", lambda event: None)  # remove the default bindings for the tab key triggering command
            widget.bind("<Shift-Tab>", lambda event: None)  # remove the default bindings for the shift tab key triggering command
            widget.bind("<Return>", lambda event: None)  # remove the default bindings for the return key triggering command
            widget.bind("<KP_Enter>", lambda event: None)  # remove the default bindings for the keypad enter key triggering command
            # Disable the default focus traversal
            widget.unbind_class(widget.winfo_class(), "<Tab>")  # remove the default bindings for the tab key triggering command
            widget.unbind_class(widget.winfo_class(), "<Shift-Tab>")  # remove the default bindings for the shift tab key triggering command
            widget.unbind_class(widget.winfo_class(), "<Up>")  # remove the default bindings for the up key triggering command
            widget.unbind_class(widget.winfo_class(), "<Down>")  # remove the default bindings for the down key triggering command

            widget.bind("<FocusIn>", self.on_focus_in)  # bind the on_focus_in method to the focus in event, highlighting focused widgets blue
            widget.bind("<FocusOut>", self.on_focus_out)  # bind the on_focus_out method to the focus out event, resetting the color of the widget to the original color
            widget.bind("<Return>", self.data_table_widget_page2_button_click)  # bind the data_table_widget_page2_button_click method to the return key, triggering the button click method
            widget.bind("<KP_Enter>", self.data_table_widget_page2_button_click)  # bind the data_table_widget_page2_button_click method to the keypad enter key, triggering the button click method
            widget.bind("<Button-1>", self.data_table_widget_page2_button_click)  # bind the data_table_widget_page2_button_click method to the left mouse button, triggering the button click method

    def on_focus_in(self, event):  # method to highlightcolor the widget blue when it's in focus
        event.widget.original_color = event.widget.cget("bg")  # Store the original color
        if event.widget in self.employee_tables_list:
            event.widget.config(bg="dark blue")  # data widgets are highlighted light blue since their text is black
        else:
            event.widget.config(bg="lightblue")  # NONE data widgets are highlighted dark blue since their text is white

    def on_focus_out(self, event):  # method to reset the color of the widget to the original color when it's not in focus
        event.widget.config(bg=event.widget.original_color)  # Reset the color to the original color
        self.last_item_focused_on = event.widget  # this is used to know which button was last focused on
        self.main_file_instance.pg2_current_item_focused_on = event.widget  # NOTE: Diff than last item focused on,
        # the last items focused on tend to be the back or next buttons, this makes sure it's the widget before they were clicked on

    def calculate_parameters(self):
        # NOTE: don't use appkit or nsscreen, use winfo instead, it's more accurate to what you want
        self.screen_width = self.parent.winfo_screenwidth()
        self.screen_height = self.parent.winfo_screenheight()

        self.screen_resolution = round(self.screen_width * self.screen_height)  # this will be used to determine font size

        self.font_size = None  # initialize font size

        font_based_on_screen_size = round((self.screen_resolution / 400000))  # calculate font size based on screen size
        font_based_on_screen_size = round(max(min(font_based_on_screen_size, 18), 16))  # set caps on min and max font size

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

    def create_widgets(self):  # method to create the widgets on the Page2 class
        # create a label showing what page the user is on
        self.page_number_label = CreateLabels.create_label(
            frame=self.row0_frame,  # place the label on the row0_frame
            text="Page 2",  # set the text of the label to "Page 2"
            font=self.font,  # set the font of the label to the font attribute of the Page2 class
            background="gray20",  # set the background of the label to gray20
            padx=self.padx_multiplier,  # set the xpadding of the label to the padx_multiplier attribute of the Page2 class
            pady=self.pady_multiplier * 0,  # set the y padding to 0
            row=0,  # place the label in row 0 of the row0_frame
            column=0,  # place the label in column 0 of the row0_frame
            highlightthickness=0,  # set the highlightthickness to 0 to remove the border around the label
        )

        # create back button
        self.back_button = CreateButtons.create_button(
            frame=self.row0_frame,
            text="go back".title(),  # use the title method to capitalize the first letter of each word in the string
            font=self.font,
            row=0,
            column=1,
            padx=self.padx_multiplier,
            pady=self.pady_multiplier * 2,
            background="gray75",
            height=round(self.height_multiplier * 30),
            width=round(self.width_multiplier * 100),
        )
        # create an instructions label to help guide the user
        self.second_pg_instructions_label = CreateLabels.create_label(
            frame=self.row0_frame,
            background=self.bg_color,
            font=self.font,
            text="To 'Edit' or 'Delete' : Click on an Employee then Press either 'Edit' or 'Delete'",
            padx=self.padx_multiplier,
            pady=self.pady_multiplier * 0,
            row=0,
            column=2,
            highlightthickness=0,
        )
        # create an edit button so the user can edit a data widget after selecting it
        self.edit_button = CreateButtons.create_button(
            frame=self.row0_frame,
            text="EDIT".title(),
            font=self.font,
            row=0,
            column=3,
            padx=self.padx_multiplier,
            pady=self.pady_multiplier * 2,
            background="gray75",
            height=round(self.height_multiplier * 30),
            width=round(self.width_multiplier * 125),
        )
        # create a delete button so the user can delete a data widget after selecting it
        self.delete_button = CreateButtons.create_button(
            frame=self.row0_frame,
            text="DELETE".title(),
            font=self.font,
            row=0,
            column=4,
            padx=self.padx_multiplier,
            pady=self.pady_multiplier * 2,
            background="gray75",
            height=round(self.height_multiplier * 30),
            width=round(self.width_multiplier * 125),
        )
        # create a label to show the user what to do after they're done reviewing their data
        self.done_review_label = CreateLabels.create_label(
            frame=self.row1_frame,
            background=self.bg_color,
            font=self.font,
            text="Review your data, when you're done, click the 'Next Step' Button -->",
            row=0,
            column=0,
            sticky=None,
            padx=self.padx_multiplier,
            pady=self.pady_multiplier * 2,
            columnspan=None,
        )
        # create a next button so the user can move to the next page
        self.next_button = CreateButtons.create_button(
            frame=self.row1_frame,
            text="NEXT STEP".title(),
            font=self.font,
            padx=self.padx_multiplier,
            pady=self.pady_multiplier * 2,
            row=0,
            column=1,
            background="gray75",
            height=round(self.height_multiplier * 30),
            width=round(self.width_multiplier * 125),
        )

        self.button_bindings()  # call the button_bindings method to bind the buttons you just created to their respective methods
        self.create_data()  # call the create_data method to create the data widgets

    def yes_pressed(self, event):  # method to be called when the user presses the yes button on the delete selected employee pop up window
        self.delete_data()  # call the delete_data method to delete the data of the employee that was selected
        if self.employee_to_delete == self.page1_instance.employee_to_edit:  # check if the employee to delete is the same as the employee to edit from page 1
            self.page1_instance.employee_to_edit = None  # if so, set that page 1 variable to None
            self.page1_instance.inside_edit_sequence = False  # also set page 1's inside_edit_sequence variable to False
            # these are important variables that help keep each page of the program in sync with each other

        self.employee_to_delete = None  # NOTE: this line must be below self.delete_data() because that method uses this variable

        # grab prevents the user from interacting with the main window until they close the pop up, grab_release releases that grab
        self.pop_up_in_focus.popup.grab_release()

        self.pop_up_in_focus.popup.withdraw()  # withdraw the pop up window after the grab is released

        # when a user presses yes to deleting an employee, they are deleting one of the data widgets on page 2 and 3, so if the focus happened to be on that widget,
        # you would need to reset the focus to the back button since that data widget no longer exists
        # first check if self.last_item_focused_on isnt None, if it isnt, then put it through the widget_exists method to check if it exists
        if self.widget_exists(self.last_item_focused_on):  # check if the last item focused on exists
            self.last_item_focused_on.focus_set()  # if so, set the focus to that widget
        else:
            self.back_button.focus_set()  # if not, set the focus to the back button

    def no_pressed(self, event):  # method to be called when the user presses the no button on the delete selected employee pop up window
        self.pop_up_in_focus.popup.grab_release()  # if they press no, then you would simply release the grab and withdraw the pop up window
        self.pop_up_in_focus.popup.withdraw()
        if self.widget_exists(self.last_item_focused_on):  # check if the last item focused on exists
            self.last_item_focused_on.focus_set()  # if so, set the focus to that widget
        else:
            self.back_button.focus_set()  # if not, set the focus to the back button

    def widget_exists(self, widget):
        try:
            return widget.winfo_exists()  # Return the result of winfo_exists()
        except TclError:
            return False

    def create_data(self):  # method to create the data widgets
        table_row = 2  # initialize a table_row variable to 2, this will be used to place the data widgets in the data_frame
        table_col = 0  # initialize a table_col variable to 0, this will be used to place the data widgets in the data_frame

        for employee in self.json_data:  # loop through the data in the json file
            (
                name_num_table,  # initialize a name_num_table variable to the name_num_table attribute of the DualTableCreation class
                schedule_table,  # initialize a schedule_table variable to the schedule_table attribute of the DualTableCreation class
            ) = self.dual_table_creation_instance.return_dual_table_for_employee(
                employee=employee
            )  # call the return_dual_table_for_employee method of the DualTableCreation class to get the name_num_table and schedule_table for the employee
            employee_preview_table = f"{name_num_table}\n{schedule_table}"  # initialize an employee_preview_table variable to the name_num_table and schedule_table combined
            # create a Text widget to display the employee_preview_table
            employee_preview_table_text = Text(
                self.data_frame,  # place the Text widget on the data_frame
                width=round(max(min(self.width_multiplier * 42, 42), 42)),  # set the width of the Text widget to 42
                height=10,
                font=self.font,
                background="gray22",  # set the background of the Text widget to gray22, different from the usual gray20 used for everything else, you want the data widgets to be slightly lighter than the rest of the widgets for visibility
                pady=self.padx_multiplier,
                padx=self.pady_multiplier * 2,
            )

            employee_preview_table_text.insert(END, employee_preview_table)  # insert the employee_preview_table into the Text widget

            # Add the tag and config after inserting the text
            employee_preview_table_text.tag_add("right", "1.0", "end")  # tags will move the first line, starting at character 0(1.0) to the end of the text to the right, this specifically focuses on the text
            employee_preview_table_text.tag_config("right", justify="right")  # this will take that tag and move it to the right, this specifically focuses on the thing holding the text

            employee_preview_table_text.grid(row=table_row, column=table_col, sticky=NSEW)  # use the grid method to place the Text widget in the data_frame
            employee_preview_table_text.config(state=DISABLED)  # prevent the user from editing the Text widget, they can only view it, if they want to edit it, they have to select it and press the edit button

            # columns start at 0 and you want the data widgets to only span up to 3 columns, so if the table_col is 2, then you want to reset it to 0 and increase the table_row by 1 to move the next trio of data widgets to the next row
            if table_col == 2:  # if you're on the 3rd column
                table_col = -1  # reset the table_col to -1(since you add 1 to it at the end of the loop, it'll be 0)
                table_row += 1  # increase the table_row by 1 to move the next trio of data widgets to the next row
            table_col += 1  # increase the table_col by 1 to move the next data widget to the next column

            self.employee_tables_list.append(employee_preview_table_text)  # add the Text widget to the employee_tables_list so you can access them later

        # put into navigation list so you can navigate through them using the up and down keys and the tab and shift tab keys
        for widget in self.employee_tables_list:  # loop through the widgets in the employee_tables_list
            self.list_of_all_widgets.append(widget)  # add the widget to the list of all widgets

        self.tables_navigation_bindings()  # bind the widgets in the employee_tables_list to their respective methods

    def load_data(self, file_path):  # method to load the data from the json file
        try:  # try to open the json file
            with open(file_path, "r") as file:  # open the json file, set it as the file variable
                data = json.load(file)  # load the data from the json file into the data variable
            return data  # return the data variable
        except FileNotFoundError:  # if the json file is not found
            print("No file found")  # print "No file found"
            return None  # then return None

    def update_data(self, json_data):  # method to update the data widgets
        if json_data != self.json_data:  # check if the json_data is equal to the json_data attribute of the Page2 class
            self.json_data = json_data  # if it's not equal, set the json_data attribute of the Page2 class to the json_data, thereby updating it

            # NOTE: removing a widget from a list is not the same as deleting it, so you need to make sure you do both
            if self.employee_tables_list != []:  # check if the employee_tables_list is empty
                for widget in self.employee_tables_list:  # if it's not empty, loop through the widgets in the employee_tables_list
                    widget.destroy()  # then destroy the widgets in the employee_tables_list, deleting them
                self.employee_tables_list = []  # then reset the employee_tables_list to an empty list, removing them from the list

            self.create_data()  # after completely ridding of the old data widgets, call the create_data method to create the new data widgets

        self.frame.update_idletasks()  # then update idle tasks again, since you just did a big reconfiguration of the widgets, which will have a big impact on other aspects of the program

    def button_bindings(self):  # method to bind the buttons to their respective methods
        self.list_of_all_widgets.append(self.back_button)  # add the back button to the list of all widgets
        self.list_of_all_widgets.append(self.edit_button)  # add the edit button to the list of all widgets
        self.list_of_all_widgets.append(self.delete_button)  # add the delete button to the list of all widgets
        self.list_of_all_widgets.append(self.next_button)  # add the next button to the list of all widgets

        # bindings, mainly for the buttons
        for widget in self.list_of_all_widgets:
            widget.bind("<Command-b>", lambda event: None)  # for back button
            widget.bind("<Command-n>", lambda event: None)  # for next button
            widget.bind("<Command-e>", lambda event: None)  # for edit button
            widget.bind("<Command-d>", lambda event: None)  # for delete button
            widget.bind("<Up>", lambda event: None)  # for up key
            widget.bind("<Down>", lambda event: None)  # for down key
            widget.bind("<Button-1>", lambda event: None)  # for left mouse button
            widget.bind("<Tab>", lambda event: None)  # for tab key
            widget.bind("<Shift-Tab>", lambda event: None)  # for shift tab key
            widget.bind("<Return>", lambda event: None)  # for return key
            widget.bind("<KP_Enter>", lambda event: None)  # for keypad enter key
            # Disable the default focus traversal
            widget.unbind_class(widget.winfo_class(), "<Tab>")
            widget.unbind_class(widget.winfo_class(), "<Shift-Tab>")
            widget.unbind_class(widget.winfo_class(), "<Up>")
            widget.unbind_class(widget.winfo_class(), "<Down>")

            widget.bind("<FocusIn>", self.on_focus_in)  # will highlightcolor focused widgets blue
            widget.bind("<FocusOut>", self.on_focus_out)  # will reset the color of the widget to the original color
            widget.bind("<Return>", self.data_table_widget_page2_button_click)  # enter key will trigger the button click method
            widget.bind("<KP_Enter>", self.data_table_widget_page2_button_click)  # keypad enter key will trigger the button click method
            widget.bind("<Button-1>", self.data_table_widget_page2_button_click)  # left mouse button will trigger the button click method

        self.back_button.bind("<Return>", lambda event: self.move_backward_method(event=event))  # if back button is focused on and user presses enter key, trigger the move_backward_method
        self.back_button.bind("<KP_Enter>", lambda event: self.move_backward_method(event=event))  # if back button is focused on and user presses keypad enter key, trigger the move_backward_method
        self.back_button.bind("<Button-1>", lambda event: self.move_backward_method(event=event))  # if the user clicks the left mouse button on the back button trigger the move_backward_method

        self.next_button.bind("<Return>", lambda event: self.move_forward_method(event=event))  # if next button is focused on and user presses enter key, trigger the move_forward_method
        self.next_button.bind("<KP_Enter>", lambda event: self.move_forward_method(event=event))  # if next button is focused on and user presses keypad enter key, trigger the move_forward_method
        self.next_button.bind("<Button-1>", lambda event: self.move_forward_method(event=event))  # if the user clicks the left mouse button on the next button trigger the move_forward_method

        self.edit_button.bind("<Return>", lambda event: self.edit_button_click(event=event))  # if edit button is focused on and user presses enter key, trigger the edit_button_click method
        self.edit_button.bind("<KP_Enter>", lambda event: self.edit_button_click(event=event))  # if edit button is focused on and user presses keypad enter key, trigger the edit_button_click method
        self.edit_button.bind("<Button-1>", lambda event: self.edit_button_click(event=event))  # if the user clicks the left mouse button on the back button trigger the edit_button_click method

        self.delete_button.bind("<Button-1>", lambda event: self.delete_button_click(event))  # if the user clicks the left mouse button on the delete button trigger the delete_button_click method
        self.delete_button.bind("<Return>", lambda event: self.delete_button_click(event))  # if delete button is focused on and user presses enter key, trigger the delete_button_click method
        self.delete_button.bind("<KP_Enter>", lambda event: self.delete_button_click(event))  # if delete button is focused on and user presses keypad enter key, trigger the delete_button_click method
        self.delete_button.bind("<Command-d>", lambda event: self.delete_button_click(event))  # if the user presses command d, trigger the delete_button_click method

    def delete_data(self):  # method to delete the data of the employee that was selected
        data = self.load_data("employee_time_project_data_file.json")  # load the data from the json file

        new_data = [entry for entry in data if entry != self.employee_to_delete]  # use list comprehension to create a new list of data without the employee that was selected to be deleted

        with open("employee_time_project_data_file.json", "w") as file:  # open the json file, set it as the file variable
            json.dump(new_data, file, indent=4)  # dump the new updated data into the json file

        new_data = self.load_data("employee_time_project_data_file.json")  # load the new updated data from the json file into the new_data variable

        self.update_data(new_data)  # call the update_data method to update the data widgets with this new updated data variable

        self.main_file_instance.adjust_window_size()  # call the adjust_window_size method of the main_file_instance to adjust the window size to fit the new data widgets

    def delete_button_click(self, event):  # method called when the user triggers the delete button
        if self.current_page_index == 1:  # check if the user is on the correct page
            for widget in self.employee_tables_list:  # loop through the widgets in the employee_tables_list
                if widget.cget("highlightbackground") == "red":  # checks if one of the widgets is highlighted red, that means it was selected before the user clicked the delete button
                    # after getting the highlighted widget, you need to loop through the data in the json file to find the line of data that created the widget that was selected
                    for employee in self.json_data:  # loop through the data in the json file
                        tuple_value = self.dual_table_creation_instance.return_dual_table_for_employee(employee=employee)  # this creates a tuple value of the name_num_table and schedule_table for each employee
                        final_value = tuple_value[0] + tuple_value[1]  # now you combine the name_num_table and schedule_table to create a singular data widget value

                        # remove the new line characters from the final_value and the widget that was highlighted red, that way you can compare them without any unexpected differences
                        final_value = final_value.replace("\n", "")  # this is the final value from the json file
                        str_widget = widget.get(1.0, END).replace("\n", "")  # this is the final value derived from the widget that was highlighted red

                        if final_value == str_widget:  # now compare the two values
                            self.employee_to_delete = employee  # if they're equal, set the employee_to_delete variable to the employee that was selected, this variable is important for other methods in the program

                            (name_table, sched_table) = self.dual_table_creation_instance.return_dual_table_for_employee(
                                employee=self.employee_to_delete
                            )  # now recreate the name_table and sched_table for the employee that was selected

                            data_to_show = f"{name_table}\n{sched_table}"  # then combine the name_table and sched_table to create a singular data widget

                            # create a pop up window to confirm if the user wants to delete the selected employee
                            self.pop_up_in_focus = SelfMadePopUp(
                                title=None,  # omit the title parameter
                                message=f"\nARE YOU SURE YOU WANT TO DELETE THIS DATA?\n\n\n{data_to_show}",  # set the message to the data_to_show variable, asking the user if they're sure they want to delete the data
                                height=20,
                                width=50,
                                font=self.font,  # set the font to the font attribute of the Page2 class
                                row=0,
                                col=0,
                                padx=5,
                                pady=5,
                                cspan=2,  # there will be a yes and no button, each on one column, so this message will span across both columns
                                bg_color=self.bg_color,
                                yes_command=lambda event: self.yes_pressed(event=event),  # set the yes_command to the yes_pressed method
                                no_command=lambda event: self.no_pressed(event=event),  # set the no_command to the no_pressed method
                            )

        # after creating the contents of the pop up window, you need to grab it, so the user can't interact with the main window until they close the pop up window
        if self.pop_up_in_focus:  # first check if the pop up exists
            self.pop_up_in_focus.popup.grab_set()  # if it does, set the grab to the pop up window

    def edit_button_click(self, event):  # method called when the user triggers the edit button
        if self.current_page_index == 1:  # check if the user is on the correct page
            for widget in self.employee_tables_list:  # loop through the widgets in the employee_tables_list
                if widget.cget("highlightbackground") == "red":  # if one of the widgets is highlighted red, that means it was selected before the user clicked the edit button
                    for employee in self.json_data:  # loop through the data in the json file to fine the line of data that created the widget that was selected
                        tuple_value = self.dual_table_creation_instance.return_dual_table_for_employee(employee=employee)  # this creates a tuple value of the name_num_table and schedule_table for each employee
                        final_value = tuple_value[0] + tuple_value[1]  # now you combine the name_num_table and schedule_table to create a singular data widget value

                        # using the replace method, remove the new line characters from the final_value and the widget that was highlighted red, that way you can compare them without any unexpected differences
                        final_value = final_value.replace("\n", "")  # this is the final value from the json file
                        # NOTE: instead of doing widget=widget.get(1.0, END), you need to do widget_content=widget.get(1.0, END), otherwise you'll get an error
                        # this is because during the first iteration, the widget variable is a Text widget, but during the second iteration, the widget variable is a string
                        # so you can't use the get method on a string, you can only use the get method on a Text widget, so you have to create a new variable to store the get method result
                        # hence the creation of the widget_content variable
                        widget_content = widget.get(1.0, END).replace("\n", "")  # this is the final value derived from the widget that was highlighted red

                        if final_value == widget_content:  # now compare the two values
                            self.employee_to_edit = employee  # if they're equal, set the employee_to_edit variable to the employee that was selected, this variable is important for other methods in the program
                            self.finish_edit_process(event=event)  # call the finish_edit_process method to finish the edit process

    def finish_edit_process(self, event):  # method to finish the edit process
        # NOTE: when a user presses on a data widget of an employee on page 2 to edit it, you will take the data from that data widget and put it into the data entries on page 1
        self.page1_instance.name_entry.delete(0, END)  # first delete the data in the name entry on page 1
        self.page1_instance.name_entry.insert(0, self.employee_to_edit["employee_name"])  # then insert the name of the employee to edit from that data widget into the name entry on page 1
        self.page1_instance.phone_number_entry.delete(0, END)  # then delete the data in the phone number entry on page 1
        self.page1_instance.phone_number_entry.insert(0, self.employee_to_edit["employee_phone_number"])  # then insert the phone number of the employee to edit from that data widget into the phone number entry on page 1

        employee_data = self.dict_of_dates  # initialize a variable to the dict_of_dates attribute of the Page1 class, this is a dictionary with all the links to the buttons and entries on page 1
        employee_schedule = self.employee_to_edit["employee_schedule"]  # initialize a variable to the employee_schedule of the employee_to_edit variable

        # this for loop is to insert the start and end times from the json data linked to the employee_to_edit variable into the start and end time entries on page 1
        # and to highlightcolor the am/pm buttons on page 1 based on the start and end time's AM/PM values from the json data linked to the employee_to_edit variable

        # this for loop is to highlightcolor the am/pm buttons on page 1 based on the start and end time's AM/PM values from the json data linked to the employee_to_edit variable
        # THEN insert the start and end times from the json data linked to the employee_to_edit variable into the start and end time entries on page 1
        # NOTE: the code dealing with the highlighting MUST be BEFORE the code dealing with inserting the start and end times into the entries on page 1
        # this is because the code dealing with the inserting of the start and end times will first remove the AM/PM from the json data linked to the employee_to_edit variable
        # so if you put the code dealing with the highlighting after the code dealing with the inserting of the start and end times, the code dealing with the highlighting will not work
        for day in self.dates_list:  # loop through the dates_list attribute of the Page1 class
            date_start_time = employee_schedule[day][START_TIME]  # initialize a variable to the start time of the employee_to_edit variable for the day currently being looped through
            date_end_time = employee_schedule[day][END_TIME]  # initialize a variable to the end time of the employee_to_edit variable for the day currently being looped through
            # first check if "AM" or "PM" is in the start time value
            if "AM" in date_start_time:  # check if the start time json value has an AM in it
                employee_data[day][START_TIME]["am_button"].config(highlightbackground="red")  # if so, highlightcolor the am button button linked to that json value red
                employee_data[day][START_TIME]["pm_button"].config(highlightbackground=self.page1_instance.bg_color)  # then highlightcolor its paired pm button the original color
            elif "PM" in date_start_time:  # check if the start time json value has a PM in it
                employee_data[day][START_TIME]["pm_button"].config(highlightbackground="red")  # if so, highlightcolor the pm button button linked to that json value red
                employee_data[day][START_TIME]["am_button"].config(highlightbackground=self.page1_instance.bg_color)  # then highlightcolor its paired am button the original color
            else:  # if the start_time json value for that day doesnt have an AM or PM in it, that means the employee is off for that day so set the am/pm buttons for that entry to the default colors
                employee_data[day][START_TIME]["am_button"].config(highlightbackground="red")
                employee_data[day][START_TIME]["pm_button"].config(highlightbackground=self.page1_instance.bg_color)

            # now check if "AM" or "PM" is in the end time json value
            if "AM" in date_end_time:  # check if the end time json value has an AM in it
                employee_data[day][END_TIME]["am_button"].config(highlightbackground="red")  # if so, highlightcolor the am button button linked to that json value red
                employee_data[day][END_TIME]["pm_button"].config(highlightbackground=self.page1_instance.bg_color)  # and highlightcolor the pm button the original color
            elif "PM" in date_end_time:  # check if the end time json value has a PM in it
                employee_data[day][END_TIME]["pm_button"].config(highlightbackground="red")  # if so, highlightcolor the pm button button linked to that json value red
                employee_data[day][END_TIME]["am_button"].config(highlightbackground=self.page1_instance.bg_color)  # and highlightcolor the am button the original color
            else:  # if the end_time json value for that day doesnt have an AM or PM in it, that means the employee is off for that day so set the am/pm buttons for that entry to the default colors
                employee_data[day][END_TIME]["am_button"].config(highlightbackground=self.page1_instance.bg_color)
                employee_data[day][END_TIME]["pm_button"].config(highlightbackground="red")

            # now you can deal with inserting the start and end times from the json data linked to the employee_to_edit variable into the start and end time entries on page 1
            date_start_time = date_start_time.replace("AM", "")  # remove the AM from the start time json value linked to the employee_to_edit variable
            date_start_time = date_start_time.replace("PM", "")  # remove the PM from the start time json value linked to the employee_to_edit variable
            date_end_time = date_end_time.replace("AM", "")  # remove the AM from the end time json value linked to the employee_to_edit variable
            date_end_time = date_end_time.replace("PM", "")  # remove the PM from the end time json value linked to the employee_to_edit variable
            employee_data[day][START_TIME]["time"].delete(0, END)  # delete the data in the start time entry on page 1 for the day currently being looped through to open it up for new data
            employee_data[day][END_TIME]["time"].delete(0, END)  # delete the data in the end time entry on page 1 for the day currently being looped through to open it up for new data

            # if start time is off, end time would also off so set the start and end time entries to OFF,
            # it's important that this if loop is before you insert the start and end time json values into the entries on page 1
            if date_start_time == "OFF":
                date_start_time = ""  # set the start time entry to an empty string, that way the code dealing with this data automatically knows that the employee is off for that day
                date_end_time = ""  # set the end time entry to an empty string, that way the code dealing with this data automatically knows that the employee is off for that day

            employee_data[day][START_TIME]["time"].insert(
                0, date_start_time
            )  # insert the start time json value linked to the employee_to_edit variable into the start time entry on page 1 for the day currently being looped through
            employee_data[day][END_TIME]["time"].insert(
                0, date_end_time
            )  # insert the end time json value linked to the employee_to_edit variable into the end time entry on page 1 for the day currently being looped through

        self.page1_instance.inside_edit_sequence = True  # set the inside_edit_sequence variable of the Page1 class to True, this methods in that class are in sync with what's going on with page 2
        self.page1_instance.employee_to_edit = self.employee_to_edit  # similar to the reasoning above, you want to set the employee_to_edit variable of the Page1 class to the employee_to_edit variable of the Page2 class
        self.move_backward_method(event)  # after setting up the data to start editing the data widget selected on page 2, you need to move the user to page 1 since the actual editing of the data will take place there
