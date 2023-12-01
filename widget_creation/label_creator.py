from tkinter import Label  # import label class from tkinter package


class CreateLabels:
    # staticmethod is used to call the method without instantiating the class

    # DO NOT USE SELF AS THE PARAMETER NAME FOR STATIC METHODS
    # CAUSE WHEN YOU ENTER THE FRAME ARGUMENT IN ANOTHER CLASS, YOU MIGHT GET AN ERROR DOING SELF=SELF, PYTHON WILL GET CONFUSED ON WHICH SELF TO USE
    def create_label(
        frame,  # frame to put the label in
        text=None,  # text to put on the label
        font=None,  # font to use for the text
        row=None,  # row to put the label in
        column=None,  # column to put the label in
        padx=None,  # x padding to put around the label
        pady=None,  # y padding to put around the label
        background=None,  # background color for the label
        sticky=None,  # which side of the cell to stick the label to
        columnspan=None,  # how many columns the label will span
        width=None,  # width of the label
        height=None,  # height of the label
        highlightthickness=None,  # set to 0 if you want to remove the border of the label
    ):
        # Create a Label widget with the specified parameters
        label = Label(frame, text=text, font=font, background=background, width=width, height=height, highlightthickness=highlightthickness)

        # Grid the label within the specified row and column with padding
        label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, columnspan=columnspan)

        # Return the created label
        return label
