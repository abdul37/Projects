from tkinter import Entry  # import entry class from tkinter package


class CreateEntries:  # class to create entries
    # staticmethod is used to call the method without instantiating the class

    # DO NOT USE SELF AS THE PARAMETER NAME FOR STATIC METHODS
    # CAUSE WHEN YOU ENTER THE FRAME ARGUMENT IN ANOTHER CLASS,
    # YOU MIGHT GET AN ERROR DOING SELF=SELF, PYTHON WILL GET CONFUSED ON WHICH SELF TO USE
    def create_entry(
        frame,  # frame to put the entry in
        row=None,  # row to put the entry in
        column=None,  # column to put the entry in
        padx=None,  # x padding for the entry
        pady=None,  # y padding for the entry
        sticky=None,  # sticky for the entry
        columnspan=None,  # columnspan for the entry
        width=None,  # width for the entry
        font=None,  # font for the entry
        justify=None,  # justify for the entry, this moves the text to the left, right, or center
        highlightthickness=None,  # will remove the border of the entry if set to 0
        background=None,  # background color for the entry
        take_focus=None,  # if set to True, the entry will be focused when the program starts
    ):
        # Create a entry widget with the specified parameters
        entry = Entry(frame, width=width, takefocus=take_focus, font=font, justify=justify, highlightthickness=highlightthickness, background=background)

        # Grid the entry within the specified row and column with padding
        entry.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, columnspan=columnspan)

        # Return the created entry
        return entry
