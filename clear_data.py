from tkinter import *  # import almost everything from tkinter package

TIME = "time"  # create constant for time key in dictionary


class ClearData:  # class to clear the data from the entry boxes and reset the buttons
    # staticmethod is used to call the method without instantiating the class
    def clear_inputs(
        name_entry,  # name entry value
        phone_number_entry,  # phone number entry value
        dates_dictionary,  # dictionary containing the dates and their corresponding am/pm buttons/values
        list_of_dates,  # list of dates, monday to friday
        bg_color,  # background color
    ):
        name_entry.delete(0, END)  # clear name entry from first index value character to last
        phone_number_entry.delete(0, END)  # clear phone number entry from first index value character to last
        for date in list_of_dates:  # loop through the list of dates
            # clear the start and end time entry values for each date
            dates_dictionary[date]["start_time"][TIME].delete(0, END)
            dates_dictionary[date]["end_time"][TIME].delete(0, END)

        # reset the am/pm buttons to their original color
        for date in list_of_dates:  # loop through the list of dates
            dates_dictionary[date]["start_time"]["am_button"].config(highlightbackground="red")  # start time am button to red
            dates_dictionary[date]["start_time"]["pm_button"].config(highlightbackground=bg_color)  # start time pm button to gray20
            dates_dictionary[date]["end_time"]["am_button"].config(highlightbackground=bg_color)  # end time am button to gray20
            dates_dictionary[date]["end_time"]["pm_button"].config(highlightbackground="red")  # end time pm button to red
