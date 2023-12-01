# import almost everything from tkinter module
from tkinter import *


class PhoneCorrector:  # class to correct phone number entries
    def phone_number_entry_corrector(phone_number_entry, event):  # function to correct phone number entries, takes in phone_number_entry and event to keep track of which entry is being corrected
        cursor_pos = phone_number_entry.index("insert")  # get the cursor index position

        if len(phone_number_entry.get()) > 12:  # an entry over 12 characters triggers this
            # Get the current contents of the entry widget
            current_text = phone_number_entry.get()
            # Get the index of the last character entered
            last_char_index = phone_number_entry.index(INSERT) - 1
            # Remove the last character from the text
            new_text = current_text[:last_char_index] + current_text[last_char_index + 1 :]
            # Update the entry widget with the new text
            phone_number_entry.delete(0, END)  # Delete all the text in the entry widget
            phone_number_entry.insert(0, new_text)  # Insert the new length appropriate text in the entry widget
            phone_number_entry.icursor(cursor_pos - 1)  # Set the cursor to the position of the last character entered

        # check num of digits, must be outside all conditions so it doesnt get tangled up with the rest of the code
        num_digits = 0  # will use this variable to check other conditions later on
        for char in phone_number_entry.get():
            if char.isdigit():
                num_digits += 1

        # NOTE: THESE CONDITIONS ONLY APPLY IF THE USER ISNT MOVING BACK AND FORTH WITH THE ARROW KEYS
        # this prevents entry value modifications from being triggered when the user is simply moving between characters
        if event.keysym not in (
            "Left",
            "Right",
        ):  # event.keysym gets the key that was just pressed
            if event.keysym == "space":  # if the user presses space, delete it since you don't want spaces in a phone number
                for index, value in enumerate(phone_number_entry.get()):
                    if value == " ":
                        phone_number_entry.delete(index)

            cursor_pos = phone_number_entry.index("insert")  # get the cursor index position

            # instantly delete any '-' that isnt at index 3 or 7, the only places that '-' should be in a phone number
            # NOTE: YOU WON'T NEED ANY MORE CONDITIONS THAT DELETE '-' POST THIS
            if phone_number_entry.get().split():  # prevents empty string error by creating a list of the characters in the entry, returns none if empty
                index = 0  # index to keep track of which character is being checkedX
                while index <= len(phone_number_entry.get()) - 1:  # while loop to check each character in the entry
                    if phone_number_entry.get()[index] == "-":  # check if current character is a '-'
                        if index != 3 and index != 7:  # check if the current index of the '-' is not 3 or 7
                            phone_number_entry.delete(index)  # if it is, delete itX
                    elif not phone_number_entry.get()[index].isdigit():  # if the character is neither a '-' or a digit, delete it
                        phone_number_entry.delete(index)
                    index += 1
            else:
                phone_number_entry.delete(0, END)  # if the entry is empty(just spaces), delete it

            if event.keysym == "BackSpace":  # create conditions for backspace press
                # NOTE: you need to be careful with backspaces because the value of the entry the code deals with is after the backspace has deleted a character

                # NOTE: WHEN THE USER BACKSPACES ON THE FIRST '-', THEY'RE ESSENTIALLY TRYING TO BACKSPACE THE NUMBER BEFORE IT, SO YOU NEED TO DELETE THE NUMBER BEFORE IT
                if cursor_pos == 3:  # cursor position is 3 if the user backspaces on the first '-' in the phone number
                    phone_number_entry.delete(2)  # this implies the user is trying to delete the number before the first '-', the number at index 2
                    if num_digits > 3:  # if the number of digits is greater than 3, insert a '-' at index 3 to replace the one that was just deleted
                        if phone_number_entry.get()[3] != "-":  # if there isn't already a '-' at index 3, insert one
                            phone_number_entry.insert(3, "-")  # insert a '-' at index 3 if there isn't one
                    if num_digits > 6:  # pressing backspace moves all the values once to the left, moving the '-' at index 7 to index 6, which might end up getting itself deleted by
                        # another checkmark so you need to insert a replacement at index 7 if it gets deleted
                        if phone_number_entry.get()[7] != "-":  # verify that there isn't already a '-' at index 7
                            phone_number_entry.insert(7, "-")  # insert a '-' at index 7 if there isn't one

                elif cursor_pos == 7:  # cursor position is 7 if the user backspaces on the second '-' in the phone number
                    phone_number_entry.delete(6)  # this implies the user is trying to delete the number before the second '-', the number at index 6

                    # NOTE: reason you don't need to create if statement for num_digits > 3 is cause backspacing only affects the characters to your right, so if you
                    # backspace on the second '-', the characters to the left of it won't be affected, so you don't need to check if there's a '-' at index 3
                    # if this ends up not being correct, just copy and past the if statement from above to here too
                    if num_digits > 6:  # pressing backspace moves all the values once to the left, moving the '-' at index 7 to index 6, which might end up getting itself deleted by
                        # another checkmark so you need to insert a replacement at index 7 if it gets deleted
                        if phone_number_entry.get()[7] != "-":  # verify that there isn't already a '-' at index 7
                            phone_number_entry.insert(7, "-")  # insert a '-' at index 7 if there isn't one

                else:
                    # conditions when the user backspaces on a number, not a '-',
                    # the conditions above needed you to do some deleting as well because the user was backspacing on a '-', not a number, so you needed to delete the number before it as well
                    # since that's what the user was trying to do when backspacing on a '-', here the user isnt backspacing on a '-', so you don't need to delete the number before it
                    # hence the fact that there is not delete statement here
                    if num_digits > 3:  # if the number of digits is greater than 3, insert a '-' at index 3 to replace the one that was just deleted
                        if phone_number_entry.get()[3] != "-":  # check if there isn't already a '-' at index 3
                            phone_number_entry.insert(3, "-")  # insert a '-' at index 3 if there isn't one
                    if num_digits > 6:  # triggered after a backspace on a number leaving you with more than 6 digits
                        if phone_number_entry.get()[7] != "-":  # check if there isn't already a '-' at index 7
                            phone_number_entry.insert(7, "-")  # insert a '-' at index 7 if there isn't one

            else:
                # condition if the user enters a number or a letter
                # basically the conditions if the user doesn't press backspace or space or arrow keys

                # checks if there's enough numbers to justify inserting a '-' at index 3, assuming there isn't already one there
                if len(phone_number_entry.get()) > 3:  # check if the length of the entry is greater than 3(this will include a '-' in the count)
                    if (
                        num_digits >= 3 and phone_number_entry.get()[3] != "-"
                    ):  # assuming it passes the first len requirement, you check now if there's actually enough digits to justify inserting a '-' at index 3
                        phone_number_entry.insert(3, "-")  # insert a '-' at index 3 if there isn't one

                # checks if there's enough numbers to justify inserting a '-' at index 7, assuming there isn't already one there
                if len(phone_number_entry.get()) > 7:  # check if the length of the entry is greater than 7(this will include a '-' in the count)
                    if (
                        num_digits >= 7 and phone_number_entry.get()[7] != "-"
                    ):  # assuming it passes the first len requirement, you check now if there's actually enough digits to justify inserting a '-' at index 7
                        phone_number_entry.insert(7, "-")  # insert a '-' at index 7 if there isn't one

                # after inserting the necessary '-'s, you need to delete any '-'s that aren't at index 3 or 7
                for index, char in enumerate(phone_number_entry.get()):  # enumerate through the entry
                    if char == "-":  # check if the current character is a '-'
                        if index != 3 and index != 7:  # and if the current index of the '-' is not 3 or 7
                            phone_number_entry.delete(index)  # delete it because a '-' should only be at index 3 or 7
