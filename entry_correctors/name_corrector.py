from tkinter import *  # import all of tkinter


class NameCorrector:  # class to correct name entries
    # function to correct name entries, takes in name_entry and event to keep track of which entry is being corrected
    def name_entry_corrector(name_entry, event):
        cursor_pos = name_entry.index("insert")  # get the cursor index position
        current_name = name_entry.get()  # get the current name in the entry

        name_entry.delete(0, END)  # delete the current name in the entry
        name_entry.insert(0, current_name.title())  # insert the current name in the entry with the first letter of each word capitalized
        name_entry.icursor(cursor_pos)  # set the cursor back to the original position after inserting the new titled name

        # an entry over 20 characters triggers this
        if len(name_entry.get()) > 20:
            # Get the current contents of the entry widget
            current_text = name_entry.get()
            # Get the index of the last character entered
            last_char_index = name_entry.index(INSERT) - 1
            # Remove the last character from the text in the entry widget
            new_text = current_text[:last_char_index] + current_text[last_char_index + 1 :]
            name_entry.delete(0, END)  # Delete all the text in the entry widget
            name_entry.insert(0, new_text)  # Insert the new length appropriate text in the entry widget
            name_entry.icursor(cursor_pos - 1)  # Set the cursor to the position of the last character entered

        if name_entry.get().split():  # prevents empty string error by creating a list of the characters in the entry, returns none if empty
            index = 0  # index to keep track of which character is being checked
            while index <= len(name_entry.get()) - 1:  # while loop to check each character in the entry
                if not (name_entry.get()[index].isalpha() or name_entry.get()[index].isspace()):  # if the character is not a letter or a space, delete it
                    name_entry.delete(index)
                    index -= 1

                if name_entry.get().split():  # prevent just spaces from being entered as a name, split creates a list that removes all spaces, so if it's just spaces, it will return none
                    if name_entry.get()[index].isspace():  # check if current character is a space
                        if name_entry.get()[index - 1].isspace():  # check if the previous character is also a space, if so, delete it to prevent double spaces
                            if index != 0:  # when deleting spaces, you place the cursor one step back since you just decreased the length of the entry by one, this prevents
                                # the cursor from going into negative numbers, creating an error
                                name_entry.delete(index)  # delete the space
                                index -= 1  # decrease the index by one to keep track of the new length of the entry

                index += 1  # increment the overarching while loop index to check the next character
        else:
            name_entry.delete(0, END)  # if the entry is empty, delete it
