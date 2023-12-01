# needed to use Button class from tkmacosx package because
# the tkinter Button class's background color wasn't working as expected on this program

# NOTE: when using Button class from tkmacosx package, their class is CANVAS, not BUTTON
# so when using winfo_classname() to get the class name of a tkmacosx Button widget, it
# will return CANVAS, not BUTTON
from tkmacosx import Button as Button


class CreateButtons:  # class to create buttons
    # staticmethod is used to call the method without instantiating the class
    def create_button(  # function to create a button
        frame=None,  # frame to put the button in
        text=None,  # text to put on the button
        font=None,  # font to use for the text
        row=None,  # row to put the button in
        column=None,  # column to put the button in
        padx=None,  # x padding for the button
        pady=None,  # y padding for the button
        background=None,  # background color for the button
        command=None,  # command to run when the button is clicked
        sticky=None,  # sticky for the button
        cspan=None,  # columnspan for the button
        highlightthickness=None,  # highlightthickness for the button
        highlightbackground=None,  # highlightbackground for the button
        fg=None,  # foreground color for the button
        width=None,  # width for the button
        height=None,  # height for the button
    ):
        # Create the button with the specified parameters
        button = Button(
            frame,
            focuscolor="",
            text=text,
            font=font,
            background=background,
            command=command,
            highlightthickness=highlightthickness,
            highlightbackground=highlightbackground,
            fg=fg,
            width=width,
            height=height,
        )

        # Grid the button within the specified row and column with padding
        button.grid(
            row=row,
            column=column,
            padx=padx,
            pady=pady,
            sticky=sticky,
            columnspan=cspan,
        )

        # Return the created button
        return button
