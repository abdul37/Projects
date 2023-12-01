import pandas as pd  # import pandas as pd

from tabulate import tabulate  # from tabulate import tabulate
from tkinter import *  # import almost everything from tkinter module


class DualTableCreation:  # class to create dual tables that will display an employee's name, phone number, and schedule in popup windows
    def create_name_num_table(self, name, phone_number):  # method to create the name and phone number table
        main_table = pd.DataFrame(columns=["Employee Name", "Employee Phone Num"])  # create a dataframe with the columns "Employee Name" and "Employee Phone Num"
        main_table.loc[0] = [name, phone_number]  # add the name and phone number to the dataframe
        return tabulate(
            main_table,  # the dataframe you created above
            headers="keys",  # the headers for the table
            tablefmt="plain",  # the table format
            showindex=False,  # don't show the index of the rows of the table as column all the way on the left of the table
            numalign="right",  # align the numbers to the right
            stralign="right",  # align the strings to the right
        )  # return the table

    def create_schedule_table(self, schedule):  # method to create the schedule table
        schedule_table = pd.DataFrame(columns=["Day", "Start Time", "End Time"])  # create a dataframe with the columns "Day", "Start Time", and "End Time"
        for day, times in schedule.items():
            # with each iteration, you're populating the dataframe with a new row containing the day, start time, and end time, increasing the tables length by 1 each time
            schedule_table.loc[len(schedule_table)] = [day, times["start_time"], times["end_time"]]
        return tabulate(
            schedule_table,  # the dataframe you created above
            headers="keys",  # the headers for the table
            tablefmt="plain",  # the table format
            showindex=False,  # don't show the index of the rows of the table as column all the way on the left of the table
            numalign="right",  # align the numbers to the right
            stralign="right",  # align the strings to the right
        )

    # method that utilizes the two methods above to create the two tables and return them
    def return_dual_table_for_employee(
        self,
        employee=None,  # employee dict
        alt_method=False,  # boolean to determine if you're using the employee dict to get employee name, phone number, and schedule or being given the employee name, phone number, and schedule directly
        employee_name=None,  # employee name
        employee_phone_number=None,  # employee phone number
        employee_schedule=None,  # employee schedule
    ):
        if not alt_method:  # if you're using the employee dict to get the employee name, phone number, and schedule
            name_num_table = self.create_name_num_table(employee["employee_name"], employee["employee_phone_number"])
            schedule_table = self.create_schedule_table(employee["employee_schedule"])
        else:  # if you're directly being given the employee name, phone number, and schedule into this method's parameters, thus not needing to use the employee dict
            name_num_table = self.create_name_num_table(employee_name, employee_phone_number)
            schedule_table = self.create_schedule_table(employee_schedule)

        return name_num_table, schedule_table  # return the two tables so you can use them in the popup windows in other methods
