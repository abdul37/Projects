# import almost everything from tkinter module
from tkinter import *


class TimeCorrector:  # class to correct time entries
    def time_entry_corrector(time_entries, event):  # function to correct time entries, takes in time_entry and event to
        # keep track of which entry is being corrected

        for dual_time_entry in time_entries:  # loop through list of time entries
            for time_entry in dual_time_entry:  # loop through start and end time of each day
                # get cursor position
                cursor_pos = time_entry.index("insert")

                # get number of digits in entry
                num_digits = 0  # will use this variable to check other conditions later on
                for char in time_entry.get():  # loop through each character in the entry
                    if char.isdigit():  # if the character is a digit, add 1 to num_digits
                        num_digits += 1

                num_of_colons = 0  # will use this variable to check other conditions later on
                for char in time_entry.get():  # loop through each character in the entry
                    if char == ":":  # if the character is a ':', add 1 to num_of_colons
                        num_of_colons += 1

                if num_of_colons > 1:  # check if there's more than 1 ':', there should only be 1 ':' in a time entry
                    time_entry.delete(cursor_pos - 1)  # delete the last ':' if there's more than 1
                    time_entry.icursor(cursor_pos - 1)  # set the cursor back to the original position after deleting the last ':'

                # NOTE: these conditions ONLY apply if the user ISN'T moving back and forth with the arrow keys
                if event.keysym not in (
                    "Left",
                    "Right",
                ):  # event.keysym gets the key that was just pressed
                    if event.keysym == "space":  # if the user presses space, delete it since you don't want spaces in a time entry
                        for index, value in enumerate(time_entry.get()):  # loop through each character in the entry
                            if value == " ":  # check if the current character is a space
                                time_entry.delete(index)  # if it is, delete it

                    cursor_pos = time_entry.index("insert")  # get the cursor index position

                    index = 0  # index to keep track of which character is being checked
                    if time_entry.get().split():  # prevents empty string error by creating a list of the characters in
                        # the entry, automatically deleting spaces, returns none if the entry is just spaces
                        while index <= len(time_entry.get()) - 1:  # while loop to check each character in the entry
                            if time_entry.get()[index] == ":":  # check if current character is a ':'
                                if index != 2 and num_digits > 3:  # NOTE: a ':' would only be present in a value like "12:34" or "1:23"
                                    # NOTE: this condition checks for incorrect placement of ':' in the entry with more than 3 digits, so only conditions with
                                    # "12:34"
                                    time_entry.delete(index)

                            elif not time_entry.get()[index].isdigit():  # if the character is neither a ':' or a digit, delete it
                                time_entry.delete(index)

                            index += 1  # add 1 to index to check the next character in the entry
                    else:
                        time_entry.delete(0, END)  # if the entry is empty(just spaces), delete it

                    if num_digits > 4:  # an entry over 4 characters triggers this
                        # Get the current contents of the entry widget
                        current_text = time_entry.get()
                        # Get the index of the last character entered
                        last_char_index = time_entry.index(INSERT) - 1
                        # Remove the last character from the text to reduce the length of the entry to 4
                        new_text = current_text[:last_char_index] + current_text[last_char_index + 1 :]
                        time_entry.delete(0, END)  # Delete all the text in the entry widget
                        time_entry.insert(0, new_text)  # Insert the new length appropriate text in the entry widget
                        time_entry.icursor(cursor_pos - 1)  # Set the cursor to the position of the last character entered

                    # after correcting for length, you need to delete any ':' that aren't at index 2 or 1
                    for index, char in enumerate(time_entry.get()):  # enumerate through the entry
                        if char == ":":  # check if the current character is a ':'
                            if index != 2 and index != 1:  # and if the current index of the ':' is not 2 or 1
                                time_entry.delete(index)  # delete it because "12:34" or "1:23" are the only acceptable formats for a time entry

                    # conditions if the user presses backspace
                    # NOTE: you need to be careful with backspaces because the value of the entry the code deals with is after the backspace has deleted a character
                    if event.keysym == "BackSpace":
                        if num_digits<3: # if the entry has less than 3 digits, you can't have a ':' in the entry
                            for index, char in enumerate(time_entry.get()):
                                if char == ":":
                                    time_entry.delete(index)
                        
                        if cursor_pos == 2:  # cursor position is 2 if the user backspaces on the first ':' in the time entry
                            if num_digits > 2 and time_entry.get()[2] != ":":  # if you have 3 or more digits and there isn't already a ':' at index 2
                                time_entry.insert(2, ":")  # insert a ':' at index 2
                                time_entry.icursor(cursor_pos)  # set the cursor back to the original position after inserting the ':'

                        else:  # if the user backspaces on a number, not a ':'
                            if num_digits > 2 and (time_entry.get()[2] != ":" and time_entry.get()[1] != ":"):  # if you have 3 or more digits and there isn't already a ':' at index 2 or 1
                                time_entry.insert(2, ":")  # insert a ':' at index 2

                    else:  # condition if the user enters a number or a letter(only applies if the user ISN'T pressing backspace)
                        if ":" not in time_entry.get():  # if there isn't a ':' in the entry
                            if num_digits > 2:  # if there's 3 or more digits
                                time_entry.insert(2, ":")  # insert a ':' at index 2
