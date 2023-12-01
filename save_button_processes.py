from tkinter import *  # import almost everything from tkinter module
import json  # import json module
from self_made_pop_up_creation import SelfMadePopUp  # import SelfMadePopUp class from self_made_pop_up_creation.py
from write_data_into_json import WriteDataIntoJson  # import WriteDataIntoJson class from write_data_into_json.py
from dual_table_creation import DualTableCreation  # import DualTableCreation class from dual_table_creation.py
from clear_data import ClearData  # import ClearData class from clear_data.py

START_TIME = "start_time"  # create constant for start time
END_TIME = "end_time"  # create constant for end time
TIME = "time"  # create constant for time


class SaveButtonProcesses:  # create a class that will handle all the processes that need to be done when the user presses the save button on an employee data entry page
    # initialize the class
    def __init__(
        self,  # instance of self
        name_entry=None,  # name entry widget
        phone_number_entry=None,  # phone number entry widget
        name=None,  # name string
        number=None,  # number string
        dates_dictionary=None,  # will hold a dictionary of all the dates and their corresponding start and end time widgets
        list_of_dates=None,  # will hold a list of all the dates, mon to sun
        background_color=None,  # background color of the page
        font=None,  # font of the page
        instance_of_page1=None,  # instance of page 1
        main_file_instance=None,  # instance of main file
    ):
        self.dual_table_creation_instance = DualTableCreation()  # create an instance of the DualTableCreation class to later call its methods

        self.main_window_link = main_file_instance  # link to main file
        self.instance_of_page1 = instance_of_page1  # link to page 1
        self.name = name  # name string
        self.name_entry = name_entry  # name entry widget
        self.number = number  # number string
        self.phone_number_entry = phone_number_entry  # number entry widget
        self.pop_up_in_focus = None  # will be set to the pop up that is in focus

        self.dates_dictionary = dates_dictionary  # dictionary of all the dates and their corresponding start and end time widgets

        self.list_of_dates = list_of_dates  # list of all the dates, mon to sun

        self.bg_color = background_color  # background color of the page

        self.times_to_convert_to_off = ("", "00:00")  # strings of times that would be converted to off

        self.name_entered = True  # boolean that will be set to false if the user doesn't enter a name

        self.number_entered = True  # boolean that will be set to false if the user doesn't enter a phone number

        self.time_entries_empty = True  # this is purely going to be used for if the user presses edit on an employee and then clears all the data, then presses save, indicating that they want to delete the employee

        self.delete_data_window = None  # will be set to the pop up that asks the user if they want to delete the employee they're editing
        self.employee_to_delete = None  # will be set to the employee the user is currently editing

        self.valid_dict_of_dates = True  # boolean that will be set to false if the user enters an invalid time entry
        self.date_needed_to_correct = None  # will be set to the date that needs to be corrected
        self.start_or_finish_time = None  # will be set to the start or finish time that needs to be corrected
        self.hours_or_minutes = None  # will be set to hours or minutes depending on what needs to be corrected
        self.ready_to_save = None  # will be set to the pop up that asks the user if they're ready to save the data they entered

        self.font = font  # font of the text on the page

        self.check_for_blank_name_or_number()  # check if the user entered a name or number
        self.final_hours_fix()  # fix the hours and minutes entries
        self.find_time_entry_error()  # check if the user entered a valid time entry

        self.final_dict = {}  # init the final dictionary of data for the current employee that will be written to the json file
        self.create_final_dict()  # create the final dictionary of data for the current employee that will be written to the json file
        self.add_am_pm_to_final_dict()  # add am or pm to the final dictionary of data for the current employee that will be written to the json file

        self.name_duplicate = False
        self.num_duplicate = False
        self.non_dict_duplicate_data = None  # later set to message that includes the bi-table of the duplicate employee
        self.dict_duplicate_data = None  # later set to extracted dictionary data of the duplicate employee

        self.invalid_name_pop_up = None
        self.invalid_phone_pop_up = None
        self.invalid_time_pop_up = None
        self.self_made_pop_up = None  # init the custom window

        self.check_for_name_or_num_duplicate()  # self.non_dict_duplicate_data and self.dict_duplicate_data are set here

        self.present_user_error_pop_up()  # present the user with an error pop up if they entered invalid data

        self.show_user_preview_ask_to_save()  # show the user a preview of the data they entered and ask them if they want to save it

    def show_user_preview_ask_to_save(self, post_duplicate_delete=False):  # show the user a preview of the data they entered and ask them if they want to save it
        # the post_duplicate_delete parameter is used to indicate that the user has tried to save his data, a duplicate was found, and they chose to overwrite it with their new data
        # NOTE: the reason it's used prefaced with an "or" in the if statements belows is because the method that determines the state of the post_duplicate_delete boolean also checks that the data entered was valid

        # this if statement first checks that the user is NOT currently editing an employee. the else statement is for when the user is editing an employee
        if not self.instance_of_page1.inside_edit_sequence:
            if (self.name_entered and (not self.name_duplicate) and (not self.num_duplicate) and self.number_entered and self.valid_dict_of_dates) or post_duplicate_delete:  # now check that they entered valid data
                # if you pass all the if statements, you can use the return_dual_table_for_employee method to create the tables that will be shown to the user
                # the first table will be the name and number table, the second will be the schedule table
                (name_table, sched_table) = self.dual_table_creation_instance.return_dual_table_for_employee(
                    alt_method=True,
                    employee_name=self.name,  # enter the name of the employee
                    employee_phone_number=self.number,  # enter the phone number of the employee
                    employee_schedule=self.final_dict,  # enter the schedule of the employee
                )

                data_to_show = f"{name_table}\n{sched_table}"  # create a modified string of the tables that will be shown to the user

                self.ready_to_save = SelfMadePopUp(  # now you can create the pop up that will show the user the preview of their data and ask them if they want to save it
                    title=None,
                    message=f"\nThese are the inputs you've entered:\n\n\n{data_to_show}\n\nREADY TO SAVE?",  # the message will contain the tables you created above
                    height=17,
                    width=50,
                    font=self.font,
                    row=0,
                    col=0,
                    padx=5,
                    pady=5,
                    cspan=2,  # the pop up will span two columns, one for the yes button and one for the no button
                    bg_color=self.bg_color,
                    yes_command=lambda event: self.save_yes_pressed(event=event),  # if the user presses yes, the save_yes_pressed method will be called
                    no_command=lambda event: self.save_no_pressed(event=event),  # if the user presses no, the save_no_pressed method will be called
                )

        else:  # this else statement is for when the user IS editing an employee, there will be two sub scenarios within this else statement.
            # one if they press save and one if they press clear all then press save, indicating that they want to delete the employee.
            # this first if statement is for the scenario where the user is editing an employee and simply presses save after
            if self.name_entered and (not self.name_duplicate) and (not self.num_duplicate) and self.number_entered and self.valid_dict_of_dates:
                # after checking that the user entered valid data, you can use the return_dual_table_for_employee method to create the tables that will be shown to the user
                (name_table, sched_table) = self.dual_table_creation_instance.return_dual_table_for_employee(
                    alt_method=True,
                    employee_name=self.name,
                    employee_phone_number=self.number,
                    employee_schedule=self.final_dict,
                )

                data_to_show = f"{name_table}\n{sched_table}"  # create a modified string of the tables that will be shown to the user

                self.ready_to_save = SelfMadePopUp(  # now create the pop up that will show the user the preview of their data and ask them if they want to save it
                    title=None,
                    message=f"\nThis is your updated entry:\n\n\n{data_to_show}\n\nREADY TO SAVE?",  # the message will contain the tables you created above
                    height=17,
                    width=50,
                    font=self.font,
                    row=0,
                    col=0,
                    padx=5,
                    pady=5,
                    cspan=2,  # the pop up will span two columns, one for the yes button and one for the no button
                    bg_color=self.bg_color,
                    yes_command=lambda event: self.save_yes_pressed(event=event),  # if the user presses yes, the save_yes_pressed method will be called
                    no_command=lambda event: self.save_no_pressed(event=event),  # if the user presses no, the save_no_pressed method will be called
                )

            # this else statement is for the scenario where the user is editing an employee, presses clear all, then presses save, indicating that they want to delete the employee
            elif (not self.name_entered) and (not self.number_entered) and self.time_entries_empty and (not self.name_duplicate) and (not self.num_duplicate) and self.valid_dict_of_dates:
                # after checking that everything is empty, set the employee to delete to the employee to edit variable

                self.employee_to_delete = self.instance_of_page1.employee_to_edit  # set the employee to delete to the employee to edit variable

                # now use the employee to delete variable to create the tables that will be shown to the user to ask them if they're sure they want to delete the employee
                name_table, sched_table = self.dual_table_creation_instance.return_dual_table_for_employee(employee=self.employee_to_delete)

                data_to_show = f"{name_table}\n{sched_table}"  # create a modified string of the tables that will be shown to the user for easier readability

                self.delete_data_window = SelfMadePopUp(  # now create the pop up that will show the user the preview of their data and ask them if they want to save it
                    title=None,
                    message=f"\nARE YOU SURE YOU WANT TO DELETE THIS DATA?\n\n\n{data_to_show}",  # the message will contain the tables you created above
                    height=20,
                    width=50,
                    font=self.font,
                    row=0,
                    col=0,
                    padx=5,
                    pady=5,
                    cspan=2,  # the pop up will span two columns, one for the yes button and one for the no button
                    bg_color=self.bg_color,
                    yes_command=lambda event: self.delete_yes_pressed(event=event),  # if the user presses yes, the delete_yes_pressed method will be called
                    no_command=lambda event: self.delete_no_pressed(event=event),  # if the user presses no, the delete_no_pressed method will be called
                )

        if self.ready_to_save:  # check that the pop up is not none
            self.pop_up_in_focus = self.ready_to_save  # if it's not none, set it to the pop up in focus
            self.pop_up_in_focus.popup.grab_set()  # then grab the pop up so the user can't click on anything else until they press yes or no
        elif self.delete_data_window:  # if this particular pop up is not none
            self.pop_up_in_focus = self.delete_data_window  # set it to the pop up in focus
            self.pop_up_in_focus.popup.grab_set()  # then grab the pop up so the user can't click on anything else until they press yes or no

    def delete_yes_pressed(self, event):  # this method is called when the user presses yes on the pop up that asks them if they're sure they want to delete the employee
        data = self.load_data("employee_time_project_data_file.json")  # load the data from the json file

        new_data = [entry for entry in data if entry != self.employee_to_delete]  # create a new list of data that doesn't include the employee to delete using list comprehension

        with open("employee_time_project_data_file.json", "w") as file:  # open the json file in write mode to overwrite the old data with the new data
            json.dump(new_data, file, indent=4)

        new_data = self.load_data("employee_time_project_data_file.json")  # load the now updated data from the json file

        self.instance_of_page1.employee_to_edit = None  # reset the employee to edit variable to none since you just deleted that employee

        self.instance_of_page1.inside_edit_sequence = False  # reset the inside edit sequence variable to false since you just finished editing an employee

        self.pop_up_in_focus.popup.grab_release()  # then release the grab on the pop up
        self.pop_up_in_focus.popup.withdraw()  # then withdraw the pop up
        self.instance_of_page1.name_entry.focus_set()  # then return focus to the name entry widget since the pop up is now gone

    def delete_no_pressed(self, event):  # this method is called when the user presses no on the pop up that asks them if they're sure they want to delete the employee
        self.pop_up_in_focus.popup.grab_release()  # all you need to do is release the grab on the pop up and withdraw it
        self.pop_up_in_focus.popup.withdraw()
        self.instance_of_page1.name_entry.focus_set()  # then return focus to the name entry widget since the pop up is now gone

    def save_yes_pressed(self, event):  # this method is called when the user presses yes on the pop up that asks them if they're sure they want to save the data they entered for an employee
        WriteDataIntoJson(  # first write the data to the json file
            name=self.name,  # enter the name of the employee
            name_entry=self.name_entry,  # enter the name entry widget
            number=self.number,  # enter the phone number of the employee
            number_entry=self.phone_number_entry,  # enter the phone number entry widget
            final_dict=self.final_dict,  # enter the final dictionary of data for the current employee that will be written to the json file
            dates_dictionary=self.dates_dictionary,  # enter the dictionary of all the dates and their corresponding start and end time widgets
            list_of_dates=self.list_of_dates,  # enter the list of all the dates, mon to sun
            bg_color=self.bg_color,  # enter the background color of the page
            employee_to_edit=self.instance_of_page1.employee_to_edit,  # NOTE: this will be used to update the employee's data in the json file, so you don't create a duplicate
        )

        # after writing the data to the json file, clear all the inputs so the user can start fresh
        ClearData.clear_inputs(
            name_entry=self.name_entry,  # used to access the name entry widget
            phone_number_entry=self.phone_number_entry,  # used to access the phone number entry widget
            dates_dictionary=self.dates_dictionary,  # used to access the dictionary of all the dates and their corresponding start and end time widgets
            list_of_dates=self.list_of_dates,  # used to help iterate through the dictionary of all the dates and their corresponding start and end time widgets
            bg_color=self.bg_color,  # will be used to reset the highlight background color of the start and end time buttons
        )

        # reset the edit sequence after saving
        if self.instance_of_page1.inside_edit_sequence:  # first check that the user was editing an employee
            self.instance_of_page1.inside_edit_sequence = False  # if they were, reset the edit sequence variable to false
            self.instance_of_page1.employee_to_edit = None  # then reset the employee to edit variable to none

        self.pop_up_in_focus.popup.grab_release()  # release the grab on the pop up
        self.pop_up_in_focus.popup.withdraw()  # withdraw the pop up
        self.instance_of_page1.name_entry.focus_set()  # return focus to the name entry widget since the pop up is now gone

    def save_no_pressed(self, event):
        self.delete_no_pressed(event=event)  # this should do the same thing as the delete no pressed method

    def add_am_pm_to_final_dict(self):  # add meridiem info to the final dictionary of data for the current employee that will be written to the json file
        for date in self.list_of_dates:  # iterate through the list of dates
            if self.final_dict[date]["start_time"] != "OFF":  # check that the date start time is not off
                # NOTE: notice how you're getting the color from the dates_dictionary but placing the result in the final_dict
                highlight_color = self.dates_dictionary[date][START_TIME]["am_button"].cget("highlightbackground")
                if highlight_color == "red":  # if color is red, then it's am, so add am to start time, if not, then it's pm, so add pm to start time
                    self.final_dict[date]["start_time"] = self.final_dict[date]["start_time"] + "AM"
                else:
                    self.final_dict[date]["start_time"] = self.final_dict[date]["start_time"] + "PM"

            # check that the date end time is not off
            if self.final_dict[date]["end_time"] != "OFF":
                # get color of end time am button
                highlight_color = self.dates_dictionary[date][END_TIME]["am_button"].cget("highlightbackground")
                # if color is red, then it's am, so add am to end time, if not, then it's pm, so add pm to end time
                if highlight_color == "red":
                    self.final_dict[date]["end_time"] = self.final_dict[date]["end_time"] + "AM"
                else:
                    self.final_dict[date]["end_time"] = self.final_dict[date]["end_time"] + "PM"

    def create_final_dict(self):  # create the final dictionary of data for the current employee that will be written to the json file
        # create dict layout for final dict that replaces objects with their values and replaces any 0's or blanks with OFF
        self.final_dict = {date: {"start_time": None, "end_time": None} for date in self.list_of_dates}

        for date in self.list_of_dates:  # insert values into final dict and replace any 0's or blanks with OFF
            if self.dates_dictionary[date]["start_time"][TIME].get() in self.times_to_convert_to_off:  # checks if the value in the start time entry is in the times to convert to off tuple
                self.final_dict[date]["start_time"] = "OFF"  # if it is, then set the start time to off
            else:  # if it's not in the times to convert to off tuple
                self.final_dict[date]["start_time"] = self.dates_dictionary[date]["start_time"][TIME].get()  # then set the start time in the final dict to the value in the start time entry in the dates dictionary

            if self.dates_dictionary[date]["end_time"][TIME].get() in self.times_to_convert_to_off:  # now check for the end time
                self.final_dict[date]["end_time"] = "OFF"
            else:
                self.final_dict[date]["end_time"] = self.dates_dictionary[date]["end_time"][TIME].get()

    def load_data(self, file_path):  # method that loads data from a json file, will be used for other methods
        try:  # try to load the data from the json file
            with open(file_path, "r") as file:  # open the json file in read mode
                data = json.load(file)  # load the data from the json file
            return data  # return the data
        except FileNotFoundError:  # if the file is not found
            print("No file found")  # print no file found
            return None  # return none

    def okay_pressed(self, event):  # this method is called when the user presses okay on the pop up that tells them they entered invalid data
        # when they press okay on that pop up, it should be destroyed and focus should be returned to the entry widget that needs to be corrected
        if self.pop_up_in_focus:  # check that the pop up in focus is not none
            self.pop_up_in_focus.popup.grab_release()  # release the grab on the pop up
            self.pop_up_in_focus.popup.withdraw()  # withdraw the pop up
            self.pop_up_in_focus = None  # reset the pop up in focus since it's been destroyed

            # focus on the location of the error after pop up is destroyed
            if not self.name_entered:  # if the name is not entered, focus on the name entry widget
                self.instance_of_page1.name_entry.focus_set()  # focus on the name entry widget
            elif not self.number_entered:  # if the number is not entered, focus on the number entry widget
                self.instance_of_page1.phone_number_entry.focus_set()  # focus on the number entry widget
            elif not self.valid_dict_of_dates:  # if the time entry is invalid, focus on the time entry widget that needs to be corrected
                # all these variables you're entering into the dates dictionary to lead you to the entry of interest are determined in the find_time_entry_error method
                self.dates_dictionary[self.date_needed_to_correct][self.start_or_finish_time_wrong][TIME].focus_set()

    def delete_duplicate_line(self):  # method that deletes the duplicate line from the json file
        data = self.load_data("employee_time_project_data_file.json")  # load the data from the json file
        new_data = [entry for entry in data if entry != self.dict_duplicate_data]  # create a new list of data that doesn't include the duplicate employee using list comprehension
        with open("employee_time_project_data_file.json", "w") as file:  # open the json file in write mode to overwrite the old data with the new data
            json.dump(new_data, file, indent=4)  # write the new data to the json file

    def delete_duplicate_yes_pressed(self, event):  # method that is called when the user presses yes on the pop up that asks them if they want to delete the duplicate employee
        self.delete_duplicate_line()  # delete the duplicate line from the json file using the delete_duplicate_line method

        self.self_made_pop_up.popup.grab_release()  # then release the grab on the pop up
        self.self_made_pop_up.popup.withdraw()  # then withdraw the pop up
        # now call the show user preview ask to save method to show the user a preview of the data they entered and ask them if they want to save it
        # this is because to have even triggered the delete duplicate yes pressed method, the user must have entered data that matched a duplicate employee,
        # and them pressing yes on deleting the duplicate employee means they want to overwrite the duplicate employee's data with their new data, so you need to show them a preview of their new data and ask them if they want to save it
        # the post_duplicate_delete parameter will be used in the show_user_preview_ask_to_save method to determine which if statement to use
        self.show_user_preview_ask_to_save(post_duplicate_delete=True)

    def delete_duplicate_no_pressed(self, event):  # method that is called when the user presses no on the pop up that asks them if they want to delete the duplicate employee
        self.self_made_pop_up.popup.grab_release()  # first release the grab on the pop up
        self.self_made_pop_up.popup.withdraw()  # then withdraw the pop up
        self.instance_of_page1.name_entry.focus_set()  # then return focus to the name entry widget since the pop up is now gone

    def present_user_error_pop_up(self):  # method that presents the user with an error pop up if they entered invalid data
        # NOTE: the main over arching if statement is very important because there is a scenario where the user is editing an employee, they clear all the data, then press save, indicating that they want to delete the employee,
        # this if statement prevents the pop ups from showing up in that scenario, so that pop up can show up in its appropriate method instead
        if not (not self.name_entered and not self.number_entered and self.time_entries_empty and self.instance_of_page1.inside_edit_sequence):
            # now that you've checked that the user is not trying to delete an employee, you can check for the other errors
            if not self.name_entered:  # if an employee name is not entered
                self.invalid_name_pop_up = SelfMadePopUp(
                    title="CHECK EMPLOYEE NAME!",
                    message="INVALID EMPLOYEE NAME:\n DON'T LEAVE BLANK!",
                    font=self.font,
                    row=0,
                    col=0,
                    height=3,
                    pady=5,
                    width=50,
                    cspan=None,
                    bg_color=self.bg_color,
                    okay_command=lambda event: self.okay_pressed(event=event),  # if the user presses okay on this popup, the okay_pressed method will be called
                    okay_button_version=True,  # this is a boolean that will be used to determine if the pop up will have an okay button or a yes and no button
                )

            elif not self.number_entered:  # if an employee phone number is not entered
                self.invalid_phone_pop_up = SelfMadePopUp(
                    title="CHECK PHONE #!",
                    message="INVALID PHONE #:\n ENTER A VALID PHONE NUMBER!",
                    font=self.font,
                    row=0,
                    col=0,
                    height=3,
                    pady=5,
                    width=50,
                    cspan=None,
                    bg_color=self.bg_color,
                    okay_command=lambda event: self.okay_pressed(event=event),  # if the user presses okay on this popup, the okay_pressed method will be called
                    okay_button_version=True,  # this is a boolean that will be used to determine if the pop up will have an okay button or a yes and no button
                )

            elif not self.valid_dict_of_dates:  # if the user entered an invalid time entry
                self.invalid_time_pop_up = SelfMadePopUp(
                    title="CHECK TIME ENTRIES!",
                    # the message will return the date, whether the start or finish time is wrong, and whether the hours or minutes are wrong
                    message=f"INVALID TIME ENTRY:\n{self.hours_or_minutes} is incorrect on {self.date_needed_to_correct} {' '.join([l for l in self.start_or_finish_time_wrong.split('_')])}!",
                    font=self.font,
                    row=0,
                    col=0,
                    height=3,
                    pady=5,
                    width=50,
                    cspan=None,
                    bg_color=self.bg_color,
                    okay_command=lambda event: self.okay_pressed(event=event),  # if the user presses okay on this popup, the okay_pressed method will be called
                    okay_button_version=True,  # this is a boolean that will be used to determine if the pop up will have an okay button or a yes and no button
                )

            elif self.name_duplicate or self.num_duplicate:  # if the user entered a name or number that already exists in the json file
                name_or_num = "NAME" if self.name_duplicate else "NUMBER"  # if the name is a duplicate, set the name or num variable to name, if the number is a duplicate, set the name or num variable to number
                # the message will return the bi-table of the duplicate employee
                self.self_made_pop_up = SelfMadePopUp(
                    title=f"DUPLICATE {name_or_num} FOUND",  # THIS IS THE TITLE, it will display whether the duplicate is a name or number
                    message=self.non_dict_duplicate_data,  # THIS IS THE MESSAGE, it will display the bi-table of the duplicate employee
                    font=self.font,
                    row=0,
                    col=0,
                    height=17,
                    width=50,
                    padx=5,
                    pady=5,
                    cspan=2,  # the pop up will span two columns, one for the yes button and one for the no button
                    bg_color=self.bg_color,
                    yes_command=lambda event: self.delete_duplicate_yes_pressed(event=event),  # if the user presses yes on this popup, the delete_duplicate_yes_pressed method will be called
                    no_command=lambda event: self.delete_duplicate_no_pressed(event=event),  # if the user presses no on this popup, the delete_duplicate_no_pressed method will be called
                )

            # after creating the appropriate pop up, set the self.pop_up_in_focus variable to the pop up you just created then grab the pop up so the user can't click on anything else when it's in focus
            if self.invalid_name_pop_up:
                self.pop_up_in_focus = self.invalid_name_pop_up
                self.pop_up_in_focus.popup.grab_set()
            elif self.invalid_phone_pop_up:
                self.pop_up_in_focus = self.invalid_phone_pop_up
                self.pop_up_in_focus.popup.grab_set()
            elif self.invalid_time_pop_up:
                self.pop_up_in_focus = self.invalid_time_pop_up
                self.pop_up_in_focus.popup.grab_set()
            elif self.self_made_pop_up:
                self.pop_up_in_focus = self.self_made_pop_up
                self.pop_up_in_focus.popup.grab_set()

    def check_for_blank_name_or_number(self):  # this method will set the values of boolean variables that will be used to determine if the user entered a name or number
        if self.name == "":  # if the name is blank
            self.name_entered = False  # set the name entered boolean to false
        if self.number == "" or len(self.number) < 12:  # if the number is blank or less than 12 characters
            self.number_entered = False  # set the number entered boolean to false, this will tell them that the number they entered is invalid

    def find_time_entry_error(self):  # this method will check if the user entered a valid time entry
        self.start_or_finish_time_wrong = ""  # init the start or finish time wrong variable
        self.hours_or_minutes = ""  # init the hours or minutes variable
        self.date_needed_to_correct = ""  # init the date needed to correct variable

        # iterate through the dates dictionary so you can check all the time entries
        # you use reversed because if there is two invalid time entries, the later on in the week is the one that will be presented first
        # so to avoid this, you iterate through the dates dictionary in reverse order so the invalid time entry that is earlier in the week is presented first
        for date in reversed(self.dates_dictionary):
            # this if statement will return start time error if start time is off and end time is on, since you can't only one of the times of a day on
            if self.dates_dictionary[date][START_TIME][TIME].get() in self.times_to_convert_to_off and self.dates_dictionary[date][END_TIME][TIME].get() not in self.times_to_convert_to_off:
                self.valid_dict_of_dates = False  # set the valid dict of dates boolean to false
                self.hours_or_minutes = "TIME"  # NOTE: for errors where only one of the times of a day is on, instead of setting it to hours or minutes, set it to "TIME"
                self.start_or_finish_time_wrong = START_TIME  # set the start or finish time wrong variable to start time since the start time was the only one off for this day
                self.date_needed_to_correct = date  # set the date needed to correct variable to the date that needs to be corrected

            # this if statement will return end time error if end time is off and start time is on, since you can't only one of the times of a day on
            if self.dates_dictionary[date][END_TIME][TIME].get() in self.times_to_convert_to_off and self.dates_dictionary[date][START_TIME][TIME].get() not in self.times_to_convert_to_off:
                self.valid_dict_of_dates = False  # set the valid dict of dates boolean to false
                self.hours_or_minutes = "TIME"  # NOTE: for errors where only one of the times of a day is on, instead of setting it to hours or minutes, set it to "TIME"
                self.start_or_finish_time_wrong = END_TIME  # set the start or finish time wrong variable to end time since the end time was the only one off for this day
                self.date_needed_to_correct = date  # set the date needed to correct variable to the date that needs to be corrected

            # NOTE: This for loop is WITHIN the for loop above and uses the 'date' dummy variable from it to iterate through the start and end time entries for each day in the same dictionary
            # we use reversed for the same reason as above, if there are two invalid time entries, the later on in the week is the one that will be presented first, and this will prevent that
            # this specific for loop will be used to check if an hourly entry is greater than 12 hours or if a minute entry is greater than 59 minutes
            for start_and_end_str in reversed(self.dates_dictionary[date]):
                if start_and_end_str != "frame":  # if the key is not frame, then it's either start time or end time
                    if len(self.dates_dictionary[date][start_and_end_str][TIME].get()) == 5:  # if the length of the time entry is 5, then it's a valid time entry
                        # check if the hours are greater than 12 or if the hours are 0 and the minutes are not 0, this would be an issue cause you can't have 00:30 or 00:45 or 13:00 or 14:00
                        if int(self.dates_dictionary[date][start_and_end_str][TIME].get()[:2]) > 12 or (
                            self.dates_dictionary[date][start_and_end_str][TIME].get()[:2] == "00" and self.dates_dictionary[date][start_and_end_str][TIME].get()[3:] != "00"
                        ):
                            self.valid_dict_of_dates = False  # if the hours are greater than 12 or if the hours are 0 and the minutes are not 0, then set the valid dict of dates boolean to false
                            self.hours_or_minutes = "HOURS"  # set the hours_or_minutes variable to hours
                            self.start_or_finish_time_wrong = start_and_end_str  # set the start or finish time wrong variable to the start or finish time currently being iterated through
                            self.date_needed_to_correct = date  # set the date needed to correct variable to the date variable currently being iterated through in the outer for loop

                        # this checks if the minutes are greater than 59
                        if int(self.dates_dictionary[date][start_and_end_str][TIME].get()[3:]) > 59:  # if the minutes are greater than 59
                            self.valid_dict_of_dates = False  # set the valid dict of dates boolean to false
                            self.hours_or_minutes = "MINUTES"  # set the hours_or_minutes variable to minutes
                            self.start_or_finish_time_wrong = start_and_end_str  # set the start or finish time wrong variable to the start or finish time currently being iterated through
                            self.date_needed_to_correct = date  # set the date needed to correct variable to the date variable currently being iterated through in the outer for loop

        # there's a scenario where the user is editing an employee, presses clear all, then tries to press save, indicating that they want to delete the employee
        # this if statement checks all the time entries, ensuring that all of them must be off for that pop up to show up, if any of them are not off, then it sets a boolean necessary for that
        # pop up to not show up to false, thus preventing it from showing up
        for date in reversed(self.dates_dictionary):
            if self.dates_dictionary[date][START_TIME][TIME].get() != "" or self.dates_dictionary[date][END_TIME][TIME].get() != "":
                self.time_entries_empty = False

    def final_hours_fix(self):  # this method will fix the final hours in the final dict
        # NOTE: when writing data, it's best to keep the data in string form, so don't convert the work times to non-string types like int or float

        start_end = ["start_time", "end_time"]  # create a list of start and end times that will be used to iterate through the dates dictionary,

        for date in self.list_of_dates:  # iterate through the list of dates
            for time in start_end:  # iterate through the list containing the strings "start_time" and "end_time"
                # if the length of the time entry is not 5, then it'll have a form like "1" or "1:" or "1:0" or "1:00" or "01:0" or "10" or "10:"
                if len(self.dates_dictionary[date][time]["time"].get()) != 5:  # if a time entry has len of 5, that means it already has the necessary 0's and ":" to make it valid
                    if len(self.dates_dictionary[date][time]["time"].get()) == 1:  # entries with values like "1"
                        self.dates_dictionary[date][time]["time"].insert(0, "0")  # insert 0 at the beginning
                        self.dates_dictionary[date][time]["time"].insert(END, ":00")  # insert ":00" at the end

                    if len(self.dates_dictionary[date][time]["time"].get()) == 2:  # entries with values like "10"
                        self.dates_dictionary[date][time]["time"].insert(END, ":00")  # insert ":00" at the end

                    # NOTE: we will skip len=3 cause code in another method inserts a ":" whenever there's at least 3 DIGITS in the time entry, automatically turning any len from 3 to 4
                    # essentially meaning, this method will never receive a time entry with a len of 3, so we can skip it

                    if len(self.dates_dictionary[date][time]["time"].get()) == 4:  # entries with values like "1:00" or "01:0"
                        if self.dates_dictionary[date][time]["time"].get()[1] == ":":  # if the second character is a ":", then it's a value like "1:00"
                            self.dates_dictionary[date][time]["time"].insert(0, "0")  # insert 0 at the beginning
                        else:  # if the second character is not a ":", then it's a value like "01:0"
                            self.dates_dictionary[date][time]["time"].insert(END, "0")  # insert 0 at the end

    def check_for_name_or_num_duplicate(self):  # this method will check if the user entered a name or number that already exists in the json file
        try:  # try to load the data from the json file
            with open("employee_time_project_data_file.json", "r") as employee_time_project_data_file:  # Open the JSON file for reading
                data = json.load(employee_time_project_data_file)  # Load the JSON data into the variable data

            for employee in data:  # iterate through each employee in the the json file
                if employee != self.instance_of_page1.employee_to_edit:  # if the employee is not the employee to edit, then check for duplicates
                    if employee["employee_name"] == self.name:  # check if the name from the json file is the same as the name the user entered
                        self.name_duplicate = True  # if it is, set the name duplicate boolean to true
                        self.dict_duplicate_data = employee  # assign dict duplicate to init variable so you can find it and delete it later if user wants to overwrite it

                        (name_num_table, schedule_table) = self.dual_table_creation_instance.return_dual_table_for_employee(
                            employee=self.dict_duplicate_data
                        )  # use the dual table creation instance to create the tables that will be shown to the user

            if not self.name_duplicate:  # if the name is not a duplicate, then check for a duplicate number
                for employee in data:  # iterate through each employee in the the json file
                    if employee != self.instance_of_page1.employee_to_edit:  # if the employee is not the employee to edit, then check for duplicates
                        if employee["employee_phone_number"] == self.number:  # check if the number from the json file is the same as the number the user entered
                            self.num_duplicate = True  # if it is, set the num duplicate boolean to true
                            self.dict_duplicate_data = employee  # assign dict duplicate to init variable so you can find it and delete it later if user wants to overwrite it
                            (name_num_table, schedule_table) = self.dual_table_creation_instance.return_dual_table_for_employee(
                                employee=self.dict_duplicate_data
                            )  # use the dual table creation instance to create the tables that will be shown to the user

            if self.name_duplicate:  # if the name is a duplicate, then create the tables that will be shown to the user to ask them if they want to delete the employee in the json file with the duplicate name
                self.non_dict_duplicate_data = f"DUPLICATE NAME FOUND!\n\n{name_num_table}\n\n{schedule_table}\n\nWould you like to DELETE this entry?"
            elif self.num_duplicate:  # if the number is a duplicate, then create the tables that will be shown to the user to ask them if they want to delete the employee in the json file with the duplicate number
                self.non_dict_duplicate_data = f"DUPLICATE NUMBER FOUND!\n\n{name_num_table}\n\n{schedule_table}\n\nWould you like to DELETE this entry?"

        except FileNotFoundError:  # if the file is not found
            self.existing_data = []  # Initialize existing_data as an empty list since some methods require it to be a list
