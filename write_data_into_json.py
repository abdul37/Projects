import os  # import os module
import json  # import json module
from tkinter import *  # import almost everything from tkinter module

TIME = "time"  # create a constant variable for the string "time" so you don't have to type it out every time


class WriteDataIntoJson:  # class to write data into json file
    def __init__(  # initialize the class
        self,  # instance of the class
        name,  # string variable for the name
        name_entry,  # widget for the name entry
        number,  # string variable for the phone number
        number_entry,  # widget for the phone number entry
        final_dict,  # final dict that contains the correct data from the dates dictionary
        dates_dictionary,  # dictionary that contains the widget/schedule data
        list_of_dates,  # list of dates, mon-sun
        bg_color,  # background color
        employee_to_edit,  # insert the employee to edit variable
    ):
        self.name = name  # set the name variable to the name variable passed in
        self.name_entry = name_entry  # set the name entry widget to the name entry widget passed in
        self.number = number  # set the phone number variable to the phone number variable passed in
        self.phone_number_entry = number_entry  # set the phone number entry widget to the phone number entry widget passed in
        self.final_dict = final_dict  # set the final dict variable to the final dict variable passed in
        self.dates_dictionary = dates_dictionary  # set the dates dictionary variable to the dates dictionary variable passed in
        self.list_of_dates = list_of_dates  # set the list of dates variable to the list of dates variable passed in
        self.bg_color = bg_color  # set the background color variable to the background color variable passed in
        self.employee_to_edit = employee_to_edit  # set the employee to edit variable to the employee to edit variable passed in
        self.write_data_to_json_file()  # then call the write data to json file method

    def write_data_to_json_file(self):  # method to read data from json file
        filename = "employee_time_project_data_file.json"  # set the filename variable to the string "employee_time_project_data_file.json"
        self.existing_data = []  # Initialize to empty list in case file doesn't exist

        if os.path.isfile(filename):  # Check if file exists
            with open(filename, "r") as file:  # Open file in read mode
                try:  # Try to load data from file
                    self.existing_data = json.load(file)  # Load data from file
                except json.JSONDecodeError:  # If you can't load data from file
                    pass  # move on

        # create a new dict with the data from the class variables gathered from the init method
        new_employee_data = {"employee_name": self.name, "employee_phone_number": self.number, "employee_schedule": self.final_dict}

        if not self.employee_to_edit: # if you are not in the edit sequence, append the new dict to the existing data list
            self.existing_data.append(new_employee_data)

        else:  # if you are in the edit sequence, you update the data, not append it
            # NOTE:using a for loop to alter data in the original list of dicts works here because you're iterating through mutable objects (dicts)
            # if you were iterating through a list of strings or numbers, you would have to use a while loop
            for employee in self.existing_data: # iterate through the existing data list
                if employee["employee_name"] == self.employee_to_edit["employee_name"]: # if the employee name in the existing data list is equal to the employee name in the employee to edit dict
                    employee["employee_name"] = self.name # set the employee name in the existing data list to the new name variable passed in
                    employee["employee_phone_number"] = self.number # set the employee phone number in the existing data list to the new phone number variable passed in
                    employee["employee_schedule"] = self.final_dict # set the employee schedule in the existing data list to the new final dict variable passed in

        try: # now try to write the data to the file
            with open(filename, "w") as file: # Open file in write mode
                json.dump(self.existing_data, file) # Write data to file using json.dump()
        except Exception as e: # If you can't write the data to the file
            print("Error: Failed to write data to the file.") # print an error message
            print(str(e)) # print the exact error message
