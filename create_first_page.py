from tkinter import *  # import almost everything from tkinter package
from tkinter import font  # specify that you want to import the font module from tkinter package

from widget_creation.label_creator import CreateLabels  # import the CreateLabels class from the label_creator module
from widget_creation.button_creator import CreateButtons  # import the CreateButtons class from the button_creator module
from widget_creation.entry_creator import CreateEntries  # import the CreateEntries class from the entry_creator module
from entry_correctors.name_corrector import NameCorrector  # import the NameCorrector class from the name_corrector module
from entry_correctors.phone_corrector import PhoneCorrector  # import the PhoneCorrector class from the phone_corrector module
from entry_correctors.time_corrector import TimeCorrector  # import the TimeCorrector class from the time_corrector module
from am_pm_highlighter import HighlightAmPmButton  # import the HighlightAmPmButton class from the am_pm_highlighter module
from save_button_processes import SaveButtonProcesses  # import the SaveButtonProcesses class from the save_button_processes module
from clear_data import ClearData  # import the ClearData class from the clear_data module


from PIL import Image, ImageTk  # import the Image and ImageTk classes from the PIL module


from self_made_pop_up_creation import SelfMadePopUp
from dual_table_creation import DualTableCreation
from clear_data import ClearData

START_TIME = "start_time"
END_TIME = "end_time"
TIME = "time"


# NOTE:If you're not using the "event" variable, it's common practice to replace it with an
# underscore (_) to indicate that the variable is being deliberately ignored:
# This is important because Tkinter passes an event object to the method that is bound to the button.
# Therefore, you should expect one additional argument in your bound method.
# In this case, the "event" argument is the event that has occurred. When the user clicks the button,
# an event is generated and passed to the choose_button_click_method. Even if you're not using this
# event object in your method, you still need to declare it because Tkinter is passing it anyway.
# By adding "event" as a second argument in the method definition, you accommodate the additional argument
# that Tkinter passes to bound methods.
# eg: def choose_button_click_method(self, event):


# NOTE: whenever you need to get attributes like screen width or height, use wininfo instead of appkit or nsscreen,
# also don't mix winfo_height and winfo_screenheight, use one or the other, best to use winfo_screenheight here though


class Page1(Frame):  # create the Page1 class and inherit from the Frame class
    # initialize the class
    def __init__(
        self,  # reference to the Page1 class itself
        parent,  # parent is the root window
        move_forward,  # move_forward is the method that moves the user to the next page
        main_file_instance,  # main_file_instance is the instance of the MainFile class
    ):
        super().__init__(parent)  # initialize the parent class, the Frame class, since you need the Frame class to create the Page1 class

        self.dual_table_creation_instance = DualTableCreation()  # create an instance of the DualTableCreation class to later call its methods

        self.current_page_index = 0  # set the current page index to 0

        self.main_file_instance = main_file_instance  # initialize a main_file_instance variable to the instance of the MainFile class

        self.next_button_pressed_while_editing = (
            None  # initialize a next_button_pressed_while_editing variable to None, this variable will be used to determine if the user pressed the next button while editing an employee
        )

        self.asking_user_if_they_want_to_stop_editing_pop_up = (
            None  # initialize an asking_user_if_they_want_to_stop_editing_pop_up variable to None, this variable will be used to store the pop up that asks the user if they want to stop editing an employee
        )

        self.instance_of_page1 = self  # initialize an instance_of_page1 variable to the instance of the Page1 class
        self.parent = parent  # initialize a parent variable to the root window
        self.frame = Frame(self)  # initialize a frame variable to a frame belonging to the Page1 class
        self.canvas_frame = Frame(self.frame)  # initialize a canvas_frame variable to a frame belonging to the Page1 class, place the canvas on this frame
        self.undo_redo_frame = Frame(self.frame)  # initialize an undo_redo_frame variable to a frame belonging to the Page1 class, place the undo and redo buttons on this frame
        self.save_entry_view_entries_frame = Frame(self.frame)  # initialize a save_entry_view_entries_frame variable to a frame belonging to the Page1 class, place the save entry and next buttons on this frame

        self.day_frame = Frame(self.frame)  # initialize a day_frame variable to a frame belonging to the Page1 class, place the days of the week on this frame

        self.day_label_list = []  # initialize a day_label_list variable to an empty list, place the labels of the week in this list later

        self.inside_edit_sequence = False  # initialize an inside_edit_sequence variable to False, this variable is used to determine if the user is editing an employee or not
        # this boolean will be used later on in the program
        self.employee_to_edit = None  # initialize an employee_to_edit variable to None, this variable is used to store the employee that the user is editing
        # this variable will be used later on in the program

        self.bg_color = "gray20"  # initialize a bg_color variable to gray20, this will be used as the background color for certain widgets
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # place the frame on the root window
        self.name_entry = None  # initialize a name_entry variable to None, this variable will be used to store the name entry widget
        self.phone_number_entry = None  # initialize a phone_number_entry variable to None, this variable will be used to store the phone number entry widget
        self.time_entries = []  # initialize a time_entries variable to an empty list, this variable will be used to store the time entry widgets
        self.time_buttons = []  # initialize a time_buttons variable to an empty list, this variable will be used to store the time button widgets
        self.page1_move_forward = move_forward  # initialize a when_next_button_triggered variable to the move_forward method, this variable will be used to move the user to the next page
        self.am_button = None  # initialize an am_button variable to None, this variable will be used to store the am button widget
        self.pm_button = None  # initialize a pm_button variable to None, this variable will be used to store the pm button widget

        # initialize a list_of_dates variable to a list of the days of the week, this will be helpful in iterating through data later on in the program
        self.list_of_dates = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

        # initialize a dates_dictionary variable to a dictionary, this dictionary will be used to store the start and end time widgets and their corresponding am and pm buttons for each day of the week
        self.dates_dictionary = {
            date: {
                "start_time": {"time": None, "am_button": None, "pm_button": None},
                "end_time": {"time": None, "am_button": None, "pm_button": None},
            }
            for date in self.list_of_dates
        }

        self.list_all_types_of_widgets = []  # initialize a an empty list variable that will be used to store all the widgets on the page
        self.undo_stack = []  # initialize an empty list variable that will be used to store the widgets that were changed when the user presses the undo button
        self.redo_stack = []  # initialize an empty list variable that will be used to store the widgets that were changed when the user presses the redo button
        self.last_widget_or_widgets_modified = None  # initialize a variable that will be used to store the last widget or widgets that were modified

        self.calculate_parameters()  # call the calculate_parameters method, adjusting the size of the font and thus the size of the widgets
        self.create_widgets()  # call the create_widgets method, creating the widgets on the page
        self.bind_entries_to_correctors()  # call the bind_entries_to_correctors method, binding the entries to their respective correctors
        self.create_and_populate_list_of_widgets_for_navigation()  # call the create_and_populate_list_of_widgets_for_navigation method, creating and populating a list of widgets for navigation
        self.bindings_that_affect_all_items_in_list_of_widgets_for_navigation()  # call the bindings_that_affect_all_items_in_list_of_widgets_for_navigation method, binding the widgets in the list of widgets for navigation to the correct methods
        self.bind_widgets_to_return_key_kp_enter_and_mouse_click()  # call the bind_widgets_to_return_key_kp_enter_and_mouse_click method, binding the widgets to the correct methods
        self.frame.update_idletasks()  # update the frame's idle tasks

    def bind_widgets_to_return_key_kp_enter_and_mouse_click(self):
        self.undo_button.bind("<Return>", lambda event: self.undo_action(event=event))  # bind undo button focused return key press event to the undo_action method
        self.undo_button.bind("<KP_Enter>", lambda event: self.undo_action(event=event))  # bind undo button focused keypad enter key press event to the undo_action method
        self.undo_button.bind("<Button-1>", lambda event: self.undo_action(event=event))  # bind undo button mouse click event to the undo_action method
        self.undo_button.bind("<Command-z>", lambda event: self.undo_action(event=event))  # bind undo button command-z key press event to the undo_action method

        self.redo_button.bind("<Return>", lambda event: self.redo_action(event=event))  # bind redo button focused return key press event to the redo_action method
        self.redo_button.bind("<KP_Enter>", lambda event: self.redo_action(event=event))  # bind redo button focused keypad enter key press event to the redo_action method
        self.redo_button.bind("<Button-1>", lambda event: self.redo_action(event=event))  # bind redo button mouse click event to the redo_action method
        self.redo_button.bind("<Command-y>", lambda event: self.redo_action(event=event))  # bind redo button command-y key press event to the redo_action method

        self.clear_button.bind("<Button-1>", lambda event: self.activate_clearing_of_inputs(event=event))  # bind clear button mouse click event to the activate_clearing_of_inputs method
        self.clear_button.bind("<Command-D>", lambda event: self.activate_clearing_of_inputs(event=event))  # bind clear button command-d key press event to the activate_clearing_of_inputs method

        self.save_entry_button.bind("<Return>", lambda event: self.start_post_save_processes(event=event))  # bind a save-entry-button focused return key press event to the start_post_save_processes method
        self.save_entry_button.bind("<KP_Enter>", lambda event: self.start_post_save_processes(event=event))  # bind a save-entry-button focused keypad enter key press event to the start_post_save_processes method
        self.save_entry_button.bind("<Button-1>", lambda event: self.start_post_save_processes(event=event))  # bind a save-entry-button mouse click event to the start_post_save_processes method
        self.save_entry_button.bind("<Command-s>", lambda event: self.start_post_save_processes(event=event))  # bind a save-entry-button command-s key press event to the start_post_save_processes method

        self.next_button.bind("<Return>", lambda event: self.when_next_button_triggered(event=event))  # bind a next-button focused return key press event to the when_next_button_triggered method
        self.next_button.bind("<KP_Enter>", lambda event: self.when_next_button_triggered(event=event))  # bind a next-button focused keypad enter key press event to the when_next_button_triggered method
        self.next_button.bind("<Button-1>", lambda event: self.when_next_button_triggered(event=event))  # bind a next-button mouse click event to the when_next_button_triggered method
        self.next_button.bind("<Command-n>", lambda event: self.when_next_button_triggered(event=event))  # bind a next-button command-n key press event to the when_next_button_triggered method

        # bind each am/pm button to a return/keypad enter/mouse click event to the on_key_press and highlight_time_button methods
        for dual_buttons in self.time_buttons:
            for button in dual_buttons:
                # NOTE: you need to put the methods in a list here because you're binding multiple methods to the same event
                button.bind("<Return>", lambda event: [self.on_key_press(event), self.highlight_time_button(event)])  # the method will trigger these methods in the order they're in the list
                button.bind("<KP_Enter>", lambda event: [self.on_key_press(event), self.highlight_time_button(event)])
                button.bind("<Button-1>", lambda event: [self.on_key_press(event), self.highlight_time_button(event)])

    def when_next_button_triggered(self, event):
        if self.inside_edit_sequence:  # if the user is inside the edit sequence and they clear the data, you should ask them if they want to stop editing the selected employee
            # create a messagebox to ask the user if they want to stop editing the selected employee

            self.next_button_pressed_while_editing = True  # this will be used by the yes_stop_editing method to determine if the user pressed the next button while editing an employee

            # first get the tuple value of the data table containing the name/phone number and schedule of the employee to edit, using the dual table creation class
            name_table, sched_table = self.dual_table_creation_instance.return_dual_table_for_employee(
                alt_method=True,
                employee_name=self.employee_to_edit["employee_name"],  # get the name of the employee from the data containing the employee to edit
                employee_phone_number=self.employee_to_edit["employee_phone_number"],  # get the phone number of the employee from the data containing the employee to edit
                employee_schedule=self.employee_to_edit["employee_schedule"],  # get the schedule of the employee from the data containing the employee to edit
            )

            data_to_show = f"{name_table}\n{sched_table}"  # create a string containing the name/phone number and schedule of the employee to edit

            # create a pop up that asks the user if they want to stop editing the selected employee
            self.asking_user_if_they_want_to_stop_editing_pop_up = SelfMadePopUp(
                title=None,
                message=f"\nWould you like to stop editing this employee?\n\n{data_to_show}",  # ask the user if they want to stop editing the selected employee
                height=17,
                width=50,
                font=self.font,
                row=0,
                col=0,
                padx=5,
                pady=5,
                cspan=2,
                bg_color=self.bg_color,
                yes_command=lambda event=event: self.yes_stop_editing(event),  # if the user presses the yes button, call the yes_stop_editing method
                no_command=lambda event=event: self.no_stop_editing(event=event),  # if the user presses the no button, call the no_stop_editing method
            )
            self.asking_user_if_they_want_to_stop_editing_pop_up.popup.grab_set()
        else:  # if you're not inside the edit sequence, just move the user to the next page
            self.page1_move_forward(event=event)

    def bindings_that_affect_all_items_in_list_of_widgets_for_navigation(
        self,
    ):  # method that binds the widgets in the list of widgets for navigation to the correct methods
        # disable default bindings for commands you might later bind to custom methods, then bind the custom methods to the widgets
        for widget in self.list_of_widgets_for_navigation:
            widget.bind("<Command-z>", lambda event: None)
            widget.bind("<Command-Z>", lambda event: None)
            widget.bind("<Command-y>", lambda event: None)
            widget.bind("<Command-Y>", lambda event: None)
            widget.bind("<Command-D>", lambda event: None)
            widget.bind("<Command-n>", lambda event: None)
            widget.bind("<Command-s>", lambda event: None)
            widget.bind("<Up>", lambda event: None)
            widget.bind("<Down>", lambda event: None)
            widget.bind("<Tab>", lambda event: None)
            widget.bind("<Shift-Tab>", lambda event: None)
            # Disable the default focus traversal
            widget.unbind_class(widget.winfo_class(), "<Tab>")
            widget.unbind_class(widget.winfo_class(), "<Shift-Tab>")

            widget.bind("<Up>", lambda event: self.on_up_key(event=event))
            widget.bind("<Down>", lambda event: self.on_down_key(event=event))
            widget.bind("<Tab>", lambda event: self.on_down_key(event=event))
            widget.bind("<Shift-Tab>", lambda event: self.on_up_key(event=event))

            # bind the focusing in event to the on_focus_in method and the correct_entries method
            widget.bind(
                "<FocusIn>",
                lambda event: [
                    self.on_focus_in(event=event),
                    self.correct_entries(event=event),
                ],
            ),

            # bind the focusing out event to the on_focus_out method,
            # since you want this event to trigger multiple methods,
            # you have to use this list of methods because if you bind the methods individually to
            # focus out, only the last one will work
            widget.bind(
                "<FocusOut>",
                lambda event: [
                    self.on_focus_out(event=event),
                    self.correct_entries(event=event),
                ],
            )

    def create_and_populate_list_of_widgets_for_navigation(
        self,
    ):  # method that creates and populates a list of widgets for navigation
        self.list_of_widgets_for_navigation = []  # List of widgets to navigate through when moving up or down from widget to widget

        self.list_of_widgets_for_navigation.append(self.redo_button)  # add the redo button to the list of widgets for navigation
        self.list_of_widgets_for_navigation.append(self.undo_button)  # add the undo button to the list of widgets for navigation
        self.list_of_widgets_for_navigation.append(self.name_entry)  # add the name entry widget to the list of widgets for navigation
        self.list_of_widgets_for_navigation.append(self.phone_number_entry)  # add the phone number entry widget to the list of widgets for navigation

        for day in self.list_of_dates:  # this for loop adds the widgets in the appropriate order to the list of widgets for navigation
            # starting with the start_time of a day, it's respective am and pm buttons, then the end time of the day, and it's respective am and pm buttons
            self.list_of_widgets_for_navigation.append(self.dates_dictionary[day]["start_time"]["time"])
            self.list_of_widgets_for_navigation.append(self.dates_dictionary[day]["start_time"]["am_button"])
            self.list_of_widgets_for_navigation.append(self.dates_dictionary[day]["start_time"]["pm_button"])
            self.list_of_widgets_for_navigation.append(self.dates_dictionary[day]["end_time"]["time"])
            self.list_of_widgets_for_navigation.append(self.dates_dictionary[day]["end_time"]["am_button"])
            self.list_of_widgets_for_navigation.append(self.dates_dictionary[day]["end_time"]["pm_button"])

        self.list_of_widgets_for_navigation.append(self.save_entry_button)  # add the save entry button to the list of widgets for navigation
        self.list_of_widgets_for_navigation.append(self.next_button)  # add the next button to the list of widgets for navigation

    def bind_entries_to_correctors(
        self,
    ):  # method that binds the entries to their respective correctors
        self.name_entry.bind(
            "<KeyPress>",  # bind the name entry widget to an KeyPress event that calls the correct_name_entry and on_key_press methods in that order, given the use of a list
            lambda event: [
                self.correct_name_entry(event=event),
                self.on_key_press(event=event),
            ],
        )
        # bind the name entry widget to an KeyRelease event that calls the correct_name_entry method
        self.name_entry.bind("<KeyRelease>", lambda event: self.correct_name_entry(event=event))
        # bind the phone number entry widget to an KeyPress event that calls the correct_phone_entry and on_key_press methods in that order, given the use of a list
        self.phone_number_entry.bind(
            "<KeyPress>",
            lambda event: [
                self.correct_phone_entry(event=event),
                self.on_key_press(event=event),
            ],
        )
        # bind the phone number entry widget to an KeyRelease event that calls the correct_phone_entry method
        self.phone_number_entry.bind("<KeyRelease>", lambda event: self.correct_phone_entry(event=event))
        # iterate through the list of time entries to bind each time entry widget to an KeyPress event that calls the correct_time_entry and on_key_press methods in that order, given the use of a list
        for dual_entry in self.time_entries:
            for entry in dual_entry:
                entry.bind(
                    "<KeyPress>",
                    lambda event: [
                        self.correct_time_entry(event=event),
                        self.on_key_press(event=event),
                    ],
                )
                # iterate through the list of time entries to bind each time entry widget to an KeyRelease event that calls the correct_time_entry method
                entry.bind("<KeyRelease>", lambda event: self.correct_time_entry(event=event))
                entry.configure(justify=RIGHT)

    def correct_entries(self, event):  # method called when the user focuses out of a widget
        self.correct_name_entry(event)  # call the correct_name_entry method
        self.correct_phone_entry(event)  # call the correct_phone_entry method
        self.correct_time_entry(event)  # correct the start and end time entries

    def undo_action(self, event):  # method called when the user presses the undo button
        if self.current_page_index == 0:  # since multiple pages have undo buttons, you need to make sure the user is on the first page for this undo button to work
            list_undo_widgets_changed = []  # initialize a list of widgets changed just incase the user changed multiple widgets at once

            if self.undo_stack:  # prevent an error from occuring if the user presses the undo button when there are no widgets to undo
                self.last_widget_or_widgets_modified = (
                    self.undo_stack.pop()
                )  # set the last_widget_or_widgets_modified variable to the last widget or widgets that were modified, while also removing them from the undo stack

                # create a for loop that saves a PRE modified widget's index and content into a list you'll eventually append to the REDO stack
                for widget_index, widget_content_link in enumerate(self.list_all_types_of_widgets):  # iterate through the list of all widgets
                    for modified_widget in self.last_widget_or_widgets_modified:  # iterate through the list of the last widget or widgets that were modified
                        modified_widget_index = modified_widget[0]  # set the modified_widget_index variable to the index of the modified widget
                        modified_widget_content = modified_widget[1]  # set the modified_widget_content variable to the content of the modified widget

                        if widget_index == modified_widget_index:  # if the index of the widget in the list of all widgets is equal to the index of the modified widget
                            if widget_content_link.winfo_class() == "Entry":  # and if the class of the widget is Entry
                                widget_content = widget_content_link.get()  # set the widget_content variable to the content of the widget

                            elif type(widget_content_link).__name__ == "Button":  # if the class of the widget is Button
                                widget_content = widget_content_link["highlightbackground"]  # set the widget_content variable to the highlightbackground of the widget
                                if widget_content != "red":
                                    widget_content = "gray20"  # NOTE: FOR MACOSX BUTTONS, THE HIGHLIGHTBACKGROUND RETURNS SYSTEMWINDOWBACKGROUND COLOR INSTEAD OF A COLOR SO YOU NEED TO SET IT TO GRAY20

                            # append the pre modified widget's index and content to the list of widgets changed
                            list_undo_widgets_changed.append((widget_index, widget_content))

                # append the PRE modified widgets to the opposing stack, the REDO stack in this case, since the undo button was pressed to activate this method
                if list_undo_widgets_changed:  # prevent adding empty lists to the redo stack
                    if self.redo_stack and list_undo_widgets_changed != self.redo_stack[-1]:  # ensure the redo stack isnt empty first before checking if its last element is equal to the list of widgets changed
                        self.redo_stack.append(list_undo_widgets_changed)  # if it is, append the list of widgets changed to the redo stack
                    elif not self.redo_stack:  # if the redo stack is empty
                        self.redo_stack.append(list_undo_widgets_changed)  # append the list of widgets changed to the redo stack

                # create a for loop that edits the widgets to their PRE modified state
                # NOTE: it is essential that you use a separate for loop to edit the widgets because if you put the if statements below inside the for loop above,
                # you would be editing the widgets before saving them
                for widget_index, widget_content_link in enumerate(self.list_all_types_of_widgets):  # iterate through the list of all widgets
                    for modified_widget in self.last_widget_or_widgets_modified:  # iterate through the list of the last widget or widgets that were modified
                        modified_widget_index = modified_widget[0]  # set the modified_widget_index variable to the index of the modified widget
                        modified_widget_content = modified_widget[1]  # set the modified_widget_content variable to the content of the modified widget

                        if widget_index == modified_widget_index:  # if the index of the widget in the list of all widgets is equal to the index of the modified widget
                            if widget_content_link.winfo_class() == "Entry":  # and if the class of the widget is Entry
                                self.list_all_types_of_widgets[widget_index].delete(0, END)  # delete the content of the widget
                                self.list_all_types_of_widgets[widget_index].insert(0, modified_widget_content)  # then insert the pre modified content of the widget

                            elif type(widget_content_link).__name__ == "Button":  # if the class of the widget is Button
                                if modified_widget_content == "red":  # if the pre modified content of the widget is red
                                    opposing_color = "gray20"  # set the opposing_color variable to gray20
                                if modified_widget_content == "gray20":  # if the pre modified content of the widget is gray20
                                    opposing_color = "red"  # set the opposing_color variable to red
                                # Update colors for the other buttons
                                for day in self.list_of_dates:  # iterate through the list of days of the week
                                    # if a time am/pm button is the widget that was modified, set its color to the pre modified color and its pair button's color to the opposing color
                                    # this is because for each pair, only one button can be red at a time, indicting am or pm
                                    if self.list_all_types_of_widgets[widget_index] == self.dates_dictionary[day]["start_time"]["am_button"]:
                                        self.dates_dictionary[day]["start_time"]["am_button"].config(highlightbackground=modified_widget_content)
                                        self.dates_dictionary[day]["start_time"]["pm_button"].config(highlightbackground=opposing_color)
                                    elif self.list_all_types_of_widgets[widget_index] == self.dates_dictionary[day]["start_time"]["pm_button"]:
                                        self.dates_dictionary[day]["start_time"]["pm_button"].config(highlightbackground=modified_widget_content)
                                        self.dates_dictionary[day]["start_time"]["am_button"].config(highlightbackground=opposing_color)
                                    elif self.list_all_types_of_widgets[widget_index] == self.dates_dictionary[day]["end_time"]["am_button"]:
                                        self.dates_dictionary[day]["end_time"]["am_button"].config(highlightbackground=modified_widget_content)
                                        self.dates_dictionary[day]["end_time"]["pm_button"].config(highlightbackground=opposing_color)
                                    elif self.list_all_types_of_widgets[widget_index] == self.dates_dictionary[day]["end_time"]["pm_button"]:
                                        self.dates_dictionary[day]["end_time"]["pm_button"].config(highlightbackground=modified_widget_content)
                                        self.dates_dictionary[day]["end_time"]["am_button"].config(highlightbackground=opposing_color)

            return "break"  # return "break" to prevent event propagation beyond the functions of the undo button method

    def redo_action(self, event):  # method called when the user presses the redo button
        if self.current_page_index == 0:  # since multiple pages have redo buttons, you need to make sure the user is on the first page for this redo button to work
            list_redo_widgets_changed = []  # initialize a list of widgets changed just incase the user changed multiple widgets at once

            if self.redo_stack:  # prevent an error from occuring if the user presses the redo button when there are no widgets to redo
                self.last_widget_or_widgets_modified = (
                    self.redo_stack.pop()
                )  # set the last_widget_or_widgets_modified variable to the last widget or widgets that were modified, while also removing them from the redo stack

                # create a for loop that puts a PRE modified widget's index and content into a list you'll eventually append to the UNDO stack
                for widget_index, widget_content_link in enumerate(self.list_all_types_of_widgets):  # iterate through the list of all widgets
                    for modified_widget in self.last_widget_or_widgets_modified:  # iterate through the list of the last widget or widgets that were modified
                        modified_widget_index = modified_widget[0]  # set the modified_widget_index variable to the index of the modified widget
                        modified_widget_content = modified_widget[1]  # set the modified_widget_content variable to the content of the modified widget

                        if widget_index == modified_widget_index:  # if the index of the widget in the list of all widgets is equal to the index of the modified widget
                            if widget_content_link.winfo_class() == "Entry":  # and if the class of the widget is Entry
                                widget_content = widget_content_link.get()  # set the widget_content variable to the content of the widget

                            elif type(widget_content_link).__name__ == "Button":  # if the class of the widget is Button
                                widget_content = widget_content_link["highlightbackground"]  # set the widget_content variable to the highlightbackground of the widget
                                if widget_content != "red":
                                    widget_content = "gray20"
                            list_redo_widgets_changed.append((widget_index, widget_content))  # append the pre modified widget's index and content to the list of widgets changed

                # append the PRE modified widgets to the opposing stack, the UNDO stack in this case, since the redo button was pressed to activate this method
                if list_redo_widgets_changed:  # prevent adding empty lists to the undo stack
                    # if the undo stack isn't empty and the list of widgets changed isn't equal to the last element in the undo stack
                    if self.undo_stack and list_redo_widgets_changed != self.undo_stack[-1]:
                        self.undo_stack.append(list_redo_widgets_changed)  # append the list of widgets changed to the undo stack
                    elif not self.undo_stack:  # if the undo stack is empty
                        self.undo_stack.append(list_redo_widgets_changed)  # append the list of widgets changed to the undo stack

                # note: you need to use a separate for loop to edit the widgets because if you put the if statements below inside the for loop above,
                # you would be editing the widgets before saving them onto the opposing stack, the undo stack in this case.
                # Below, the for loop that edits the widgets to their PRE modified state
                for widget_index, widget_content_link in enumerate(self.list_all_types_of_widgets):  # iterate through the list of all widgets
                    for modified_widget in self.last_widget_or_widgets_modified:  # iterate through the list of the last widget or widgets that were modified
                        modified_widget_index = modified_widget[0]  # set the modified_widget_index variable to the index of the modified widget
                        modified_widget_content = modified_widget[1]  # set the modified_widget_content variable to the content of the modified widget

                        if widget_index == modified_widget_index:  # if the index of the widget in the list of all widgets is equal to the index of the modified widget
                            if widget_content_link.winfo_class() == "Entry":  # and if the class of the widget is Entry
                                self.list_all_types_of_widgets[widget_index].delete(0, END)  # delete the content of the widget
                                self.list_all_types_of_widgets[widget_index].insert(0, modified_widget_content)  # then insert the pre modified content of the widget

                            elif type(widget_content_link).__name__ == "Button":  # if the class of the widget is Button
                                if modified_widget_content == "red":  # if the pre modified content of the widget is red
                                    opposing_color = "gray20"  # set the opposing_color variable to gray20
                                if modified_widget_content == "gray20":  # if the pre modified content of the widget is gray20
                                    opposing_color = "red"  # set the opposing_color variable to red
                                # Update colors for the other buttons
                                for day in self.list_of_dates:  # iterate through the list of days of the week
                                    # if a time am/pm button is the widget that was modified, set its color to the pre modified color and its pair button's color to the opposing color
                                    if self.list_all_types_of_widgets[widget_index] == self.dates_dictionary[day]["start_time"]["am_button"]:
                                        self.dates_dictionary[day]["start_time"]["am_button"].config(highlightbackground=modified_widget_content)
                                        self.dates_dictionary[day]["start_time"]["pm_button"].config(highlightbackground=opposing_color)
                                    elif self.list_all_types_of_widgets[widget_index] == self.dates_dictionary[day]["start_time"]["pm_button"]:
                                        self.dates_dictionary[day]["start_time"]["pm_button"].config(highlightbackground=modified_widget_content)
                                        self.dates_dictionary[day]["start_time"]["am_button"].config(highlightbackground=opposing_color)
                                    elif self.list_all_types_of_widgets[widget_index] == self.dates_dictionary[day]["end_time"]["am_button"]:
                                        self.dates_dictionary[day]["end_time"]["am_button"].config(highlightbackground=modified_widget_content)
                                        self.dates_dictionary[day]["end_time"]["pm_button"].config(highlightbackground=opposing_color)
                                    elif self.list_all_types_of_widgets[widget_index] == self.dates_dictionary[day]["end_time"]["pm_button"]:
                                        self.dates_dictionary[day]["end_time"]["pm_button"].config(highlightbackground=modified_widget_content)
                                        self.dates_dictionary[day]["end_time"]["am_button"].config(highlightbackground=opposing_color)

            return "break"  # return "break" to prevent event propagation beyond the functions of the redo button method

    def on_key_press(self, event):  # method called when the user presses a key, essentially placing a widgets index and content into the undo stack
        # Get the changed widget
        widget = event.widget

        self.list_all_types_of_widgets = [
            self.name_entry,
            self.phone_number_entry,
        ]  # initialize a list of all types of widgets to the name and phone number entries

        # extend works on iterables like lists, that's why doing this works on the list of widgets
        # remember you put dual entries in lists of pairs, so you need to iterate through them
        for dual_entry in self.time_entries:  # use the extend to add the values iterated through in a dual ENTRIES to the list of all types of widgets
            self.list_all_types_of_widgets.extend(iter(dual_entry))

        for dual_buttons in self.time_buttons:  # use the extend to add the values iterated through in a dual BUTTONS to the list of all types of widgets
            self.list_all_types_of_widgets.extend(iter(dual_buttons))

        for index, current_widget in enumerate(self.list_all_types_of_widgets):  # iterate through the list of all types of widgets
            if widget == current_widget:  # if the widget pressed is equal to the current widget being iterated through
                # NOTE NOTE NOTE:even though one widget at a time is being changed, you still need to put them in a list
                # because the way you structured your undo and redo methods, they iterate through a list of widgets
                # is is because some buttons change multiple widgets at a time, so you needed to create methods
                # that can account for either one widget or multiple widgets being changed at a time
                list_widget_changed = []  # initialize a list of widgets changed

                if widget.winfo_class() == "Entry":  # if the widget is an entry
                    list_widget_changed.append((index, widget.get()))  # append the index of the widget and the content of the widget to the list of widgets changed

                elif widget.winfo_class() == "Canvas":  # if the widget is a canvas(which is the class for macosx buttons)
                    # get the highlightbackground color of the button before it's changed
                    if widget["highlightbackground"] != "red":
                        widget["highlightbackground"] = "gray20"

                    list_widget_changed.append((index, widget["highlightbackground"]))

                if list_widget_changed:  # prevent adding empty lists to the undo stack
                    if self.undo_stack and list_widget_changed != self.undo_stack[-1]:  # ensure the undo stack isnt empty first before checking if its last element is equal to the list of widgets changed
                        self.undo_stack.append(list_widget_changed)
                    elif not self.undo_stack:  # if the undo stack is empty
                        self.undo_stack.append(list_widget_changed)  # append the list of widgets changed to the undo stack

    def page1_buttons(self, frame):  # method called to create the buttons on the page
        self.undo_redo_frame.grid(row=0, column=6, columnspan=2, padx=0, pady=self.pady_multiplier * 0)  # place the undo redo frame on the page's frame

        self.undo_button = CreateButtons.create_button(  # create the undo button
            frame=self.undo_redo_frame,  # place the undo button on the undo redo frame
            text="UNDO".title(),  # set the text of the undo button to "Undo" using the title method
            font=self.font,  # set the font of the undo button to the font variable
            row=0,  # set the row of the undo button to 0 of the undo redo frame
            column=0,  # set the column of the undo button to 0 of the undo redo frame
            padx=self.padx_multiplier,  # set the padx padding around the undo button to the padx_multiplier variable
            pady=self.pady_multiplier * 2,  # set the pady padding around the undo button to the pady_multiplier variable
            background="gray75",  # set the background of the undo button to gray75
            height=round(self.height_multiplier * 30),  # set the height of the undo button to the height_multiplier variable
            width=round(self.width_multiplier * 80),  # set the width of the undo button to the width_multiplier variable
            cspan=None,  # set the column span of the undo button to None to ensure it doesnt turn to a default value
            command=None,  # set the command of the undo button to None, since you use event binding to call the undo_action method
        )

        self.redo_button = CreateButtons.create_button(
            frame=self.undo_redo_frame,
            text="REDO".title(),
            font=self.font,
            row=0,
            column=1,
            padx=self.padx_multiplier,
            pady=self.pady_multiplier * 2,
            background="gray75",
            height=round(self.height_multiplier * 30),
            width=round(self.width_multiplier * 80),
            cspan=None,
            command=None,
        )

        for day in self.list_of_dates:  # iterate through the list of days of the week to help create the time entries and buttons
            self.dates_dictionary[day]["start_time"]["am_button"] = CreateButtons.create_button(
                frame=self.day_frame,
                text="AM",
                font=self.font,
                command=None,
                background="gray75",
                row=self.list_of_dates.index(day) + 6,  # you use +6 because you have mon-fri set vertically and since the first row will be at index 0 of the day frame,
                # you need to add 6 relative to the index of the day in the days list to get the correct row the widgets representing that day will be placed on
                column=2,  # set the column of the am button to 2 of the day frame since the first am buttons will be placed on the 2nd column of the day frame
                padx=self.padx_multiplier,
                pady=self.pady_multiplier * 1,
                sticky=W,
                width=round(self.width_multiplier * 35),
                height=round(self.height_multiplier * 25),
                highlightbackground="red",  # set initial highlight color
            )

            self.dates_dictionary[day]["start_time"]["pm_button"] = CreateButtons.create_button(
                frame=self.day_frame,
                text="PM",
                font=self.font,
                command=None,
                background="gray75",
                row=self.list_of_dates.index(day) + 6,
                column=3,  # set the column of the pm button to 3 of the day frame since the first pm buttons will be placed on the 3rd column of the day frame
                padx=self.padx_multiplier,
                pady=self.pady_multiplier * 1,
                sticky=W,
                width=round(self.width_multiplier * 35),
                height=round(self.height_multiplier * 25),
            )

            self.dates_dictionary[day]["end_time"]["am_button"] = CreateButtons.create_button(
                frame=self.day_frame,
                text="AM",
                font=self.font,
                command=None,
                background="gray75",
                row=self.list_of_dates.index(day) + 6,
                column=5,  # set the column of the am button to 5 of the day frame since the second column of am buttons will be placed on the 5th column of the day frame
                padx=self.padx_multiplier,
                pady=self.pady_multiplier * 1,
                sticky=W,
                width=round(self.width_multiplier * 35),
                height=round(self.height_multiplier * 25),
            )

            self.dates_dictionary[day]["end_time"]["pm_button"] = CreateButtons.create_button(
                frame=self.day_frame,
                text="PM",
                font=self.font,
                command=None,
                background="gray75",
                row=self.list_of_dates.index(day) + 6,
                column=6,  # set the column of the pm button to 6 of the day frame since the second column of pm buttons will be placed on the 6th column of the day frame
                padx=self.padx_multiplier,
                pady=self.pady_multiplier * 1,
                sticky=W,
                width=round(self.width_multiplier * 35),
                height=round(self.height_multiplier * 25),
                highlightbackground="red",  # set initial highlight color
            )

            # append the START TIME am/pm buttons to the time buttons list, that way you can access them later
            self.time_buttons.append(
                [
                    self.dates_dictionary[day]["start_time"]["am_button"],
                    self.dates_dictionary[day]["start_time"]["pm_button"],
                ]
            )
            # append the END TIME am/pm buttons to the time buttons list, that way you can access them later
            self.time_buttons.append(
                [
                    self.dates_dictionary[day]["end_time"]["am_button"],
                    self.dates_dictionary[day]["end_time"]["pm_button"],
                ]
            )

        # create a save entry frame to place the save entry and next step buttons on
        self.save_entry_view_entries_frame.grid(
            row=13,
            column=7,
            rowspan=2,  # set the rowspan of the save entry frame to 2 since the save entry button will be placed on top of the next step button
            padx=self.padx_multiplier,
            pady=self.pady_multiplier * 0,
        )
        # create the save entry button
        self.save_entry_button = CreateButtons.create_button(
            frame=self.save_entry_view_entries_frame,
            text="SAVE ENTRY".title(),
            font=self.font,
            background="gray75",
            row=0,  # set the row of the save entry button to 0 of the save entry view entries frame
            column=0,
            padx=2,
            pady=self.pady_multiplier * 2,
            cspan=None,
            height=round(self.height_multiplier * 30),
            width=round(self.width_multiplier * 150),
        )

        self.next_button = CreateButtons.create_button(
            frame=self.save_entry_view_entries_frame,
            text="next step".title(),
            font=self.font,
            row=1,  # set the row of the next button to 1 of the save entry view entries frame
            column=0,
            padx=2,
            pady=self.pady_multiplier * 2,
            background="gray75",
            height=round(self.height_multiplier * 30),
            width=round(self.width_multiplier * 150),
            cspan=None,
        )

        # create the clear button
        self.clear_button = CreateButtons.create_button(
            frame=self.frame,  # place the clear button on the page's frame
            text="CLEAR ALL",
            font=self.font,
            row=14,  # set the row of the clear button to the farthest bottom row of the page's frame
            column=0,  # set the column to the fartherst left column of the page's frame
            padx=2,
            pady=self.pady_multiplier * 0,
            sticky=N,
            background="gray75",
            height=round(self.height_multiplier * 30),
            width=round(self.width_multiplier * 100),
            cspan=None,
        )

    def activate_clearing_of_inputs(self, event):  # method called when the user presses the clear button
        if self.current_page_index == 0:  # since multiple pages have clear buttons, you need to make sure the user is on the first page for this clear button to work
            list_widgets_cleared = []  # initialize a list of widgets cleared to later append to the undo stack

            # iterate through the list of all types of widgets to get their index and content into the undo stack before their content is cleared
            for index, widget in enumerate(self.list_all_types_of_widgets):
                if widget.winfo_class() == "Entry":  # if the widget is an entry
                    content = widget.get()  # set the content variable to the content of the widget
                    list_widgets_cleared.append((index, content))  # then append the index of the widget and the content of the widget to the list of widgets cleared
                elif type(widget).__name__ == "Button":  # you used type(widget).__name__ == "Button" instead of widget.winfo_class() == "Canvas" because
                    # the class for macosx buttons is canvas so this is easier to keep track of the fact that you're actually dealing with a button
                    content = widget.cget("highlightbackground")  # set the content variable to the highlightbackground of the widget
                    if content != "red":
                        content = "gray20"  # NOTE: DOING THIS IS ESSENTIAL BECAUSE MACOSX BUTTONS cget("highlightbackground") RETURNS "systemWindowBackgroundColor" INSTEAD OF a color
                    list_widgets_cleared.append((index, content))

            if list_widgets_cleared:  # prevent adding empty lists to the undo stack
                if self.undo_stack and list_widgets_cleared != self.undo_stack[-1]:  # ensure the undo stack isnt empty first before checking if its last element is equal to the list of widgets cleared
                    self.undo_stack.append(list_widgets_cleared)  # if it is, append the list of widgets cleared to the undo stack
                else:  # if the undo stack is empty
                    self.undo_stack.append(list_widgets_cleared)  # append the list of widgets cleared to the undo stack

            # after you saved the pre modified widgets to the undo stack, you can now clear the widgets by calling the clear_inputs method from the ClearData class
            ClearData.clear_inputs(
                name_entry=self.name_entry,  # link to the name entry
                phone_number_entry=self.phone_number_entry,  # link to the phone number entry
                dates_dictionary=self.dates_dictionary,  # this dictionary has all the data that links to the time entries and buttons
                list_of_dates=self.list_of_dates,  # this will help you iterate through the dictionary in some of the methods in the ClearData class
                bg_color=self.bg_color,  # you pass the bg_color variable to the clear_inputs method so that the appropriate colors can be set to their original color
            )

            if self.inside_edit_sequence:  # if the user is inside the edit sequence and they clear the data, you should ask them if they want to stop editing the selected employee
                # create a messagebox to ask the user if they want to stop editing the selected employee

                name_table, sched_table = self.dual_table_creation_instance.return_dual_table_for_employee(
                    alt_method=True,
                    employee_name=self.employee_to_edit["employee_name"],  # get the name of the employee from the name entry NOTE NOTE NOTE
                    employee_phone_number=self.employee_to_edit["employee_phone_number"],  # get the phone number of the employee from the phone number entry
                    employee_schedule=self.employee_to_edit["employee_schedule"],
                )  # get the schedule of the employee from the dates dictionary

                data_to_show = f"{name_table}\n{sched_table}"

                self.asking_user_if_they_want_to_stop_editing_pop_up = SelfMadePopUp(
                    title=None,
                    message=f"\nWould you like to stop editing this employee?\n\n{data_to_show}",
                    height=17,
                    width=50,
                    font=self.font,
                    row=0,
                    col=0,
                    padx=5,
                    pady=5,
                    cspan=2,
                    bg_color=self.bg_color,
                    yes_command=lambda event=event: self.yes_stop_editing(event),
                    no_command=lambda event=event: self.no_stop_editing(event=event),
                )

                self.asking_user_if_they_want_to_stop_editing_pop_up.popup.grab_set()

            self.redo_stack = []  # set the redo stack to an empty list since the user just cleared the widgets, so there's nothing to redo now, only undo

    def yes_stop_editing(self, event):
        # if the user says they do want to stop editing an employee after they press the next button, then you actually want to clear the data and move them to the next page
        # NOTE: you must change the inside_edit_sequence variable to False before calling the activate_clearing_of_inputs method because the activate_clearing_of_inputs method uses the inside_edit_sequence variable to determine what to do
        self.inside_edit_sequence = False  # reset the inside edit sequence variable to False
        self.activate_clearing_of_inputs(event=event)  # call the activate_clearing_of_inputs method to clear the data

        self.employee_to_edit = None  # reset the employee to edit variable to None
        self.asking_user_if_they_want_to_stop_editing_pop_up.popup.grab_release()  # release the grab on the pop up
        self.asking_user_if_they_want_to_stop_editing_pop_up.popup.withdraw()  # withdraw the pop up

        if self.next_button_pressed_while_editing:  # if the user pressed the next button while editing, you need to move them to the next page after withdrawing the pop up
            self.page1_move_forward(event=event)  # move the user to the next page

        else:  # if the pop up showed up without the user pressing the next button, and they say yes they want to stop editing, then simply withdraw the pop up then return focus to the name entry
            self.instance_of_page1.name_entry.focus_set()

        self.next_button_pressed_while_editing = False  # reset the next button pressed while editing variable to False, this will be set back to true if the user presses the next button while editing

    def no_stop_editing(self, event):
        # if the user presses the no button, you need to return focus to the name entry and withdraw the pop up, don't let them move to the next page
        self.next_button_pressed_while_editing = False  # ALSO reset the next button pressed while editing variable to False, this will be set back to true if the user presses the next button while editing
        self.asking_user_if_they_want_to_stop_editing_pop_up.popup.grab_release()
        self.asking_user_if_they_want_to_stop_editing_pop_up.popup.withdraw()
        self.instance_of_page1.name_entry.focus_set()

    # method to alter a widget's color when it's focused on
    def on_focus_in(self, event):
        event.widget.original_color = event.widget.cget("bg")  # Store the original color in event.widget's original_color attribute
        if type(event.widget).__name__ == "Entry":  # if the widget is an entry
            event.widget.config(bg="dark blue")  # Change its color to dark blue, this is because light blue is too light and you can't see the text in the entries since it's white
        else:
            event.widget.config(bg="light blue")  # Change its color to light blue, this is because dark blue is too dark and you can't see the text on the buttons since it's black

    # method to reset a widget's color when it's no longer focused on
    def on_focus_out(self, event):
        event.widget.config(bg=event.widget.original_color)  # Reset the color to the event.widget's original_color attribute value

        # set the main file instance's pg1_current_item_focused_on variable to the widget that was last focused on because when a user presses a next or back button,
        # the last thing focused on becomes the last button pressed, which would be the next or back button, which is not what you want, you want the last thing focused on to
        # be the last widget focused on right before the user pressed the next or back button moving them to another page
        self.main_file_instance.pg1_current_item_focused_on = event.widget

    # method to move the focus to the widget above the current widget when the user presses the up key, or shift + tab
    def on_up_key(self, event):
        if self.current_page_index == 0:  # since multiple pages have widgets that need to be navigated through, you need to make sure the user is on the first page for this method to work
            widget = event.widget  # get the current widget
            if widget in self.list_of_widgets_for_navigation:  # if the current widget is in the list of widgets that need to be navigated through
                idx = self.list_of_widgets_for_navigation.index(widget)  # get its index in the list of widgets that need to be navigated through
                if idx > 0:  # prevent going up if the current widget is the first widget in the list of widgets that need to be navigated through
                    self.list_of_widgets_for_navigation[idx - 1].focus_set()  # then set the focus to the widget above the current widget(here index - 1)
            return "break"  # return "break" to prevent event propagation beyond the functions of the on_up_key method

    # method to move the focus to the widget below the current widget when the user presses the down key, or tab
    def on_down_key(self, event):
        if self.current_page_index == 0:  # since multiple pages have widgets that need to be navigated through, you need to make sure the user is on the first page for this method to work
            widget = event.widget  # get the current widget
            if widget in self.list_of_widgets_for_navigation:  # if the current widget is in the list of widgets that need to be navigated through
                idx = self.list_of_widgets_for_navigation.index(widget)  # get its index in the list of widgets that need to be navigated through
                if idx < len(self.list_of_widgets_for_navigation) - 1:  # prevent going down if the current widget is the last widget in the list of widgets that need to be navigated through
                    self.list_of_widgets_for_navigation[idx + 1].focus_set()  # then set the focus to the widget below the current widget(here index + 1)
            return "break"  # return "break" to prevent event propagation beyond the functions of the on_down_key method

    # method to calculate the font size and the multipliers that will affect the size of the widgets
    def calculate_parameters(self):
        # don't use appkit or nsscreen, use winfo instead, it will give you more accurate results
        self.screen_width = self.parent.winfo_screenwidth()  # get the width of the screen using the winfo_screenwidth method
        self.screen_height = self.parent.winfo_screenheight()  # get the height of the screen using the winfo_screenheight method

        self.screen_resolution = round(self.screen_width * self.screen_height)  # calculate the screen resolution by multiplying the screen width and height
        self.font_size = None  # initialize the font size variable

        font_based_on_screen_size = round((self.screen_resolution / 140000))  # calculate the font size based on the screen resolution, values were played around with until
        # dividing by 14000 gave the best results, since this variable is used to calculate the multipliers, you don't want it to be too big or too small

        font_based_on_screen_size = round(max(min(font_based_on_screen_size, 28), 24))  # put caps on the font size, you don't want it to be too big or too small
        self.font = font.Font(family="Monaco", size=font_based_on_screen_size)  # set the font variable to the font that will be used in the app, the font size is based on the screen size
        self.font_size = self.font["size"]  # set the font size variable to the font size of the font variable

        # NOTE:MULTIPLIERS SHOULD BE BASED ON THE FONT SIZE, NOT THE SCREEN SIZE, since font size is a less volatile variable, it's better to base the multipliers on it
        # NOTE : MULTIPLIERS SHOULD NOT BE ROUNDED, ONLY ROUND WHEN YOU'RE MULTIPLYING THEM WITH A WIDGETS WIDTH OR HEIGHT
        # THIS IS BECAUSE THERE'S A BIG DIFFERENCE BETWEEN A 1.2 AND 1.4 MULTIPLIER, YOU DON'T WANT TO ROUND BOTH TO 1
        # Calculate width and height multipliers based on font size, again notice how there's no rounding here, since you want to be percise with the multipliers
        self.width_multiplier = self.font_size / 16  # 16 and 15 were the results of playing around with different values until the best results were achieved
        self.height_multiplier = self.font_size / 16
        self.padx_multiplier = self.font_size / 15
        self.pady_multiplier = self.font_size / 15

    # method to create all the widgets on the page
    def create_widgets(self):
        self.create_canvas()  # create the canvas
        self.create_image()  # create the image on the canvas
        self.page1_buttons(self.frame)  # create the buttons on the page
        self.page1_labels(self.frame)  # create the labels on the page
        self.page1_entries(self.frame)  # create the entries on the page
        self.frame.update_idletasks()  # update tasks that are not always updated, or updated on time

    # method to create the canvas
    def create_canvas(self):
        self.canvas_width = round(max(min(self.font_size * 4, 500), 80))  # calculate the width of the canvas, you don't want it to be too big or too small
        self.canvas_height = round(max(min(self.font_size * 4, 500), 80))  # NOTE: the values from width were used for height because you want the canvas to be a square
        self.canvas = Canvas(
            self.canvas_frame,  # place the canvas on the canvas frame
            width=self.canvas_width,  # set the width of the canvas to the canvas_width variable
            height=self.canvas_height,  # set the height of the canvas to the canvas_height variable
            background="gray20",  # set the background of the canvas to gray20
            highlightthickness=0,  # set the highlightthickness of the canvas to 0 to remove the border around the canvas
        )
        self.image = None  # placeholder prevents this object from being trashed by the garbage collector
        self.canvas.grid(row=0, column=0, sticky="nsew")  # place the canvas on the canvas frame
        self.canvas_frame.grid(row=0, column=3, sticky="nsew", columnspan=5, rowspan=2)  # place the canvas frame on the page's frame

    # method to create the image you'll place on the canvas
    def create_image(self):
        with Image.open("images/schedule_image.png") as img:  # open the image file with the Image.open method using the image file path, set it as img
            new_size = (
                self.canvas_width,
                self.canvas_height,
            )  # set the new size of the image to the canvas width and height

            img = img.resize(new_size, Image.LANCZOS)  # resize the image using the new size and the LANCZOS resampling filter, cause sometimes the image is too big or too small

        self.image = ImageTk.PhotoImage(img)  # Convert the Image object to a PhotoImage object using the ImageTk.PhotoImage method, set it as self.image

        image_x_cor = self.canvas_width / 2  # calculate the x coordinate of the image on the canvas
        image_y_cor = self.canvas_height / 2  # calculate the y coordinate of the image on the canvas

        # create the image on the canvas using the create_image method
        self.canvas.create_image(
            round(image_x_cor),  # set the x coordinate of the image on the canvas to the image_x_cor variable
            round(image_y_cor),  # set the y coordinate of the image on the canvas to the image_y_cor variable
            image=self.image,  # set the image parameter to the self.image variable
        )

    # method to initiate saving data entered on the first page
    def start_post_save_processes(self, event):
        if self.current_page_index == 0:  # since multiple pages have save entry buttons, you need to make sure the user is on the first page for this method to work
            # call SaveButtonProcesses class
            self.instance_of_save_button_processes_class = SaveButtonProcesses(
                name=self.name_entry.get().strip(),  # the strip method removes any leading or trailing spaces, this is the final name modification on the name entry VALUE
                number=self.phone_number_entry.get(),  # get the content of the phone number entry VALUE
                dates_dictionary=self.dates_dictionary,  # get the data from the dates dictionary that links to the time entries and buttons
                list_of_dates=self.list_of_dates,  # get the list of dates to help iterate through the dates dictionary
                name_entry=self.name_entry,  # link to the name entry, different from the name entry VALUE above
                phone_number_entry=self.phone_number_entry,  # link to the phone number entry, different from the phone number entry VALUE above
                background_color=self.bg_color,  # get the background color of the page
                font=self.font,  # get the font of the page
                instance_of_page1=self.instance_of_page1,  # link to the instance of the page1 class
                main_file_instance=self.main_file_instance,  # you're using just self.font here cause self.font was already overwritten by the update_font size
            )

    # method to highlight the am/pm button that was pressed
    def highlight_time_button(self, event):
        # call HighlightAmPmButton class to use its highlight_am_pm_button method
        HighlightAmPmButton.highlight_am_pm_button(
            event=event,  # pass the event linked to the button pressed
            data_dict=self.dates_dictionary,  # pass the data from the dates dictionary that links to the time entries and buttons
            list_of_days=self.list_of_dates,  # pass the list of dates to help iterate through the dates dictionary
        )

    # method to correct the name entry
    def correct_name_entry(self, event):
        # call NameCorrector class to use its name_entry_corrector method
        NameCorrector.name_entry_corrector(name_entry=self.name_entry, event=event)  # pass the name entry and the event linked to the triggering of the correct_name_entry method

    # method to correct the phone number entry
    def correct_phone_entry(self, event):
        # call PhoneCorrector class to use its phone_number_entry_corrector method
        PhoneCorrector.phone_number_entry_corrector(
            phone_number_entry=self.phone_number_entry,
            event=event,  # pass the phone number entry and the event linked to the triggering of the correct_phone_entry method
        )

    # method to correct the time entry
    def correct_time_entry(self, event):
        # you're going to pass the entire list of entries instead of just the current one
        # that way you can iterate and correct all of them, not just the one you're focused on
        # cause if a user presses tab to move to the next time entry before the previous one done being corrected
        # the correction doesn't end up finishing on that previous entry
        TimeCorrector.time_entry_corrector(time_entries=self.time_entries, event=event)  # pass the list of time entries and the event linked to the triggering of the correct_time_entry method

    # method to create the entries on the page
    def page1_entries(self, frame):
        # create the name entry
        self.name_entry = CreateEntries.create_entry(
            frame=self.frame,  # place the name entry on the page's frame
            row=2,  # set the row of the name entry to 2 of the page's frame
            column=1,  # set the column of the name entry to 1 of the page's frame
            sticky=W,  # set the sticky parameter to W to ensure the name entry is left aligned
            columnspan=6,  # set the columnspan of the name entry to 6 to ensure it spans across the entire width of the page
            width=round(max(min(self.width_multiplier * 40, 25), 1)),  # calculate the width of the name entry, you don't want it to be too big or too small
            font=self.font,  # set the font of the name entry to the font variable
        )
        # create the phone number entry
        self.phone_number_entry = CreateEntries.create_entry(
            frame=self.frame,  # place the phone number entry on the page's frame
            row=3,  # set the row of the phone number entry to 3 of the page's frame
            column=1,  # set the column of the phone number entry to 1 of the page's frame
            sticky=W,  # set the sticky parameter to W to ensure the phone number entry is left aligned
            columnspan=6,  # set the columnspan of the phone number entry to 6 to ensure it spans across the entire width of the page
            width=round(max(min(self.width_multiplier * 40, 25), 1)),  # calculate the width of the phone number entry, you don't want it to be too big or too small
            font=self.font,  # set the font of the phone number entry to the font variable
        )

        # create the time entries
        for day in self.list_of_dates:  # iterate through the list of days of the week to help create the time entries
            # use the self.dates_dictionary to store the time entries, that way you can access them later
            self.dates_dictionary[day]["start_time"]["time"] = CreateEntries.create_entry(
                frame=self.day_frame,  # place the time entry on the day frame
                row=self.list_of_dates.index(day) + 6,  # you use +6 because you have mon-fri set vertically and since the first row will be at index 0 of the day frame,
                # you need to add 6 relative to the index of the day in the days list to get the correct row the widgets representing that day will be placed on
                column=1,  # set the column of the time entry to 1 of the day frame
                sticky=W,  # set the sticky parameter to W to ensure the time entry is left aligned
                width=round(max(min(self.width_multiplier * 10, 5), 1)),  # calculate the width of the time entry, you don't want it to be too big or too small
                font=self.font,  # set the font of the time entry to the font variable
            )

            self.dates_dictionary[day]["end_time"]["time"] = CreateEntries.create_entry(
                frame=self.day_frame,
                row=self.list_of_dates.index(day) + 6,
                column=4,  # set the column of the time entry to 4 of the day frame, allowing for a space between the start and end time entries for the am/pm buttons between them
                sticky=E,  # set the sticky parameter to E to ensure the time entry is right aligned
                width=round(max(min(self.width_multiplier * 10, 5), 1)),
                font=self.font,
            )

            # append the START TIME and END TIME entries to the time entries list, that way you can access them later
            self.time_entries.append(
                [
                    self.dates_dictionary[day]["start_time"]["time"],
                    self.dates_dictionary[day]["end_time"]["time"],
                ]
            )

    def page1_labels(self, frame):
        # create a label that will display the page number
        self.page_number_label = CreateLabels.create_label(
            frame=self.frame,  # place the page number label on the page's frame
            text="Page 1",
            font=self.font,
            background="gray20",
            padx=self.padx_multiplier,  # set the padx padding around the page number label to the padx_multiplier variable
            pady=self.pady_multiplier * 0,  # set the pady padding around the page number label to 0
            row=0,
            column=0,
            sticky=NW,  # set the sticky parameter to NW to ensure the page number label is top left aligned
            highlightthickness=0,  # set the highlightthickness of the page number label to 0 to remove the border around the page number label
            columnspan=2,  # set the columnspan of the page number label to 2 to ensure it spans across the entire width the labels on the left side of the page, that will be on average 2 columns wide
        )
        # create a label that leads the user to the name entry
        self.name_label = CreateLabels.create_label(
            frame=self.frame,
            text="Employee name:".title(),  # use the title method to capitalize the first letter of each word in the text
            font=self.font,
            background="gray20",
            padx=self.padx_multiplier,
            pady=self.pady_multiplier * 5,
            row=2,
            column=0,
            sticky=E,  # set the sticky parameter to E to ensure the name label is right aligned
        )

        # create a label that leads the user to the phone number entry
        self.phone_label = CreateLabels.create_label(
            frame=self.frame,
            text="Employee phone #:".title(),
            font=self.font,
            background="gray20",
            padx=self.padx_multiplier,
            pady=self.pady_multiplier * 5,
            row=3,
            column=0,
            sticky=E,
        )
        # create a label that leads the user to the time entries
        self.can_work_on_label = CreateLabels.create_label(
            frame=self.frame,
            text="Can work on:".title(),
            font=self.font,
            background="gray20",
            padx=self.padx_multiplier,
            pady=self.pady_multiplier * 5,
            row=4,
            column=0,
            sticky=E,
        )

        # create a label that leads the user to the start time entries
        self.start_time_label = CreateLabels.create_label(
            frame=self.frame,
            text="Start time".title(),
            font=self.font,
            background="gray20",
            padx=self.padx_multiplier,
            pady=self.pady_multiplier * 2,
            row=5,
            column=2,
            sticky=NSEW,
            columnspan=None,
        )

        # create a label that leads the user to the end time entries
        self.end_time_label = CreateLabels.create_label(
            frame=self.frame,
            text="End time".title(),
            font=self.font,
            background="gray20",
            padx=self.padx_multiplier,
            pady=self.pady_multiplier * 2,
            row=5,
            column=5,
            sticky=NSEW,
            columnspan=None,
        )

        self.day_frame.grid(row=6, column=1, rowspan=8, columnspan=6)  # you created frame just for the labels, buttons, and entries for the days of the week, so you need to place it on the page's frame
        # NOTE: you did this because there was constant spacing issues between the labels/buttons/entries when you placed them directly on the page's frame, so you created a frame to place them on, then place that frame on the page's frame
        for day in self.list_of_dates:  # iterate through the list of days of the week to help create the labels for the days of the week
            day_label = CreateLabels.create_label(
                frame=self.day_frame,
                text=f"{day}:",  # make the label text the day of the week being iterated through
                font=self.font,
                background="gray20",
                row=self.list_of_dates.index(day)
                + 6,  # you use +6 because you have mon-fri set vertically and since the first row will be at index 0 of the day frame, you need to add 6 relative to the index of the day in the days list to get the correct row the widgets representing that day will be placed on
            )

            self.day_label_list.append(day_label)  # append the day label to the day label list, that way you can access them later
