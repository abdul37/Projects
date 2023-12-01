from tkinter import *  # import almost everything from tkinter package


class HighlightAmPmButton:  # class to highlight the am/pm button that was clicked
    # staticmethod is used to call the method without instantiating the class
    def highlight_am_pm_button(
        event,  # event that triggered the method
        data_dict,  # dictionary containing the am/pm buttons
        list_of_days,  # list of days
    ):
        event.widget.config(highlightbackground="red")  # highlight the button that was clicked to red
        for day in list_of_days:  # loop through the list of days
            # check which day and which am/pm button was clicked, then highlight its counterpart to gray20
            if event.widget == data_dict[day]["start_time"]["am_button"]:
                data_dict[day]["start_time"]["pm_button"].config(highlightbackground="gray20")
            elif event.widget == data_dict[day]["start_time"]["pm_button"]:
                data_dict[day]["start_time"]["am_button"].config(highlightbackground="gray20")
            elif event.widget == data_dict[day]["end_time"]["am_button"]:
                data_dict[day]["end_time"]["pm_button"].config(highlightbackground="gray20")
            elif event.widget == data_dict[day]["end_time"]["pm_button"]:
                data_dict[day]["end_time"]["am_button"].config(highlightbackground="gray20")
