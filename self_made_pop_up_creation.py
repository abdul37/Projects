from tkinter import *  # important almost everything from the tkinter module
from widget_creation.button_creator import CreateButtons  # import the button creator class


class SelfMadePopUp:  # create a class for the pop up window
    # initialize the class
    def __init__(
        self,
        title=None,
        message=None,
        height=None,
        width=None,
        font=None,
        row=None,
        col=None,
        cspan=None,
        padx=None,
        pady=None,
        yes_command=None,  # the command for the yes button if the class utilizes its original form
        no_command=None,  # the command for the no button if the class utilizes its original form
        bg_color=None,
        okay_command=None,  # the command for the okay button if the class utilizes its alternate form
        okay_button_version=False,  # this boolean is used to determine which version of the pop up window to use, the yes/no version or the okay version
    ):
        # initialize the class attributes
        self.title = title  # the title of the pop up window
        self.bg_color = bg_color  # the background color of the pop up window
        self.message = message  # the message to be displayed in the pop up window
        self.height = height  # the height of the pop up window
        self.width = width  # the width of the pop up window
        self.font = font  # the font of the pop up window
        self.row = row  # the row of the pop up window
        self.col = col  # the column of the pop up window
        self.cspan = cspan  # the column span of the pop up window
        self.padx = padx  # the padx of the pop up window
        self.pady = pady  # the pady of the pop up window
        self.yes_command = yes_command  # the command for the yes button if the class utilizes its original form
        self.no_command = no_command  # the command for the no button if the class utilizes its original form
        self.okay_command = okay_command  # the command for the okay button if the class utilizes its alternate form
        self.okay_button_version = okay_button_version  # this boolean is used to determine which version of the pop up window to use, the yes/no version or the okay version

        self.popup = Toplevel()  # #NOTE: Toplevel is a class of the tkinter module, it is used to create a pop up window independent of the main window the program is running on
        self.create_pop_up()  # call the create pop up method, this will create the contents of the pop up window

        self.last_focused = None  # this will be used to keep track of which button has the focus

        # bind the restore focus method to the pop up window, this will be used to restore focus to the last focused button when the pop up window regains focus
        self.popup.bind("<FocusIn>", lambda event: self.restore_focus(event=event))

    def create_pop_up(self):  # method to create the contents of the pop up window
        self.popup.config(background=self.bg_color)  # configure the background color of the pop up window

        self.popup.title(self.title)  # set the title of the pop up window

        # Create the text widget that will display the message
        text_widget = Text(
            self.popup,  # the parent of the text widget is the pop up window
            height=self.height,
            width=self.width,
            font=self.font,
            background=self.bg_color,
            highlightthickness=0,  # this is used to remove the border around the text widget
        )
        # now place the text widget on the grid of the pop up window
        text_widget.grid(
            row=self.row,  # the row of the text widget on the pop up window
            column=self.col,  # the column of the text widget on the pop up window
            columnspan=self.cspan,  # the column span of the text widget on the pop up window, would be 2 if the pop up window is using the yes/no version, 1 otherwise
            padx=self.padx,
            pady=self.pady,
        )

        text_widget.tag_configure(CENTER, justify=CENTER)  # configure the text widget to be centered so the message is centered on the pop up window

        text_widget.insert(END, self.message, CENTER)  # Insert the table into the text widget

        text_widget.configure(state="disabled")  # Disable editing in the text widget cause you don't want the user to be able to edit the message

        # Create the buttons for the pop up window
        if not self.okay_button_version:  # create the yes/no buttons if the self.okay_button_version attribute is False
            self.yes_button = CreateButtons.create_button(  # create the yes button
                frame=self.popup,  # place the button on the pop up window
                font=self.font,
                text="YES",  # the text of the button
                command=self.yes_command,  # the method to be called when the button is pressed
                row=1,  # place it on the second row of the pop up window since the message is on the first row
                column=1,  # place it on the second column of the pop up window since the no button is on the first column
                padx=None,
                pady=15,
                sticky=None,
            )
            self.no_button = CreateButtons.create_button(  # create the no button
                frame=self.popup,  # place the button on the pop up window
                font=self.font,
                text="NO",  # the text of the button
                command=self.no_command,  # the method to be called when the button is pressed
                row=1,  # place it on the second row of the pop up window since the message is on the first row
                column=0,  # place it on the first column of the pop up window since the yes button is on the second column
                padx=None,
                pady=15,
                sticky=None,
            )

            # now bind the buttons to the appropriate methods
            self.yes_button.bind("<Return>", lambda event: self.yes_command(event=event))  # a yes button focused return key press will call the yes command
            self.no_button.bind("<Return>", lambda event: self.no_command(event=event))  # a no button focused return key press will call the no command

            self.yes_button.bind("<Button-1>", lambda event: self.yes_command(event=event))  # a yes button mouse click will call the yes command
            self.no_button.bind("<Button-1>", lambda event: self.no_command(event=event))  # a no button mouse click will call the no command

            self.yes_button.bind("<KP_Enter>", lambda event: self.yes_command(event=event))  # a yes button focused keypad enter key press will call the yes command
            self.no_button.bind("<KP_Enter>", lambda event: self.no_command(event=event))  # a no button focused keypad enter key press will call the no command


            # NOTE: DUE TO THE NATURE OF TKINTER USING EVENTS FOR PRETTY MUCH EVERYTHING, EVEN WHEN YOU'RE USING A METHOD LIKE FOCUS_SET() WHICH DOESNT TAKE THAT EVENT VARIABLE, YOU STILL SHOULD USE THE LAMBDA EVENT EXPRESSION
            # so doing self.yes_button.bind("<Tab>", self.no_button.focus_set()) will not work, you have to do self.yes_button.bind("<Tab>", lambda event: self.no_button.focus_set())
            self.yes_button.bind("<Tab>", lambda event: self.no_button.focus_set())  # a yes button focused tab key press will set the focus to the no button
            self.no_button.bind("<Tab>", lambda event: self.yes_button.focus_set())  # a no button focused tab key press will set the focus to the yes button

            self.yes_button.bind("<Shift-Tab>", lambda event: self.no_button.focus_set())  # a yes button focused shift tab key press will set the focus to the no button
            self.no_button.bind("<Shift-Tab>", lambda event: self.yes_button.focus_set())  # a no button focused shift tab key press will set the focus to the yes button

            self.yes_button.bind("<Up>", lambda event: self.no_button.focus_set())  # a yes button focused up arrow key press will set the focus to the no button
            self.no_button.bind("<Up>", lambda event: self.yes_button.focus_set())  # a no button focused up arrow key press will set the focus to the yes button

            self.yes_button.bind("<Down>", lambda event: self.no_button.focus_set())  # a yes button focused down arrow key press will set the focus to the no button
            self.no_button.bind("<Down>", lambda event: self.yes_button.focus_set())  # a no button focused down arrow key press will set the focus to the yes button

            self.no_button.bind("<FocusIn>", lambda event: self.on_focus_in(event=event))  # the no button being focused on will call the on_focus_in method
            self.yes_button.bind("<FocusIn>", lambda event: self.on_focus_in(event=event))  # the yes button being focused on will call the on_focus_in method

            self.no_button.bind("<FocusOut>", lambda event: self.on_focus_out(event=event))  # the no button losing focus will call the on_focus_out method
            self.yes_button.bind("<FocusOut>", lambda event: self.on_focus_out(event=event))  # the yes button losing focus will call the on_focus_out method

            self.popup.bind("<Escape>", lambda event: self.no_command(event=event))  # an escape key press will call the no command

            self.no_button.focus_set()  # set the initial focus to the no button when the pop up window is created

        else:  # create the okay button if the self.okay_button_version attribute is True of the pop up window
            self.okay_button = CreateButtons.create_button(  # create the okay button
                frame=self.popup,  # place the button on the pop up window
                font=self.font,
                text="OKAY",  # the text of the button
                row=1,  # place it on the second row of the pop up window since the message is on the first row
                column=0,  # place it on the first column of the pop up window since there is only one column with the okay button version
                padx=None,
                pady=15,
                sticky=None,
            )

            self.okay_button.bind("<Return>", lambda event: self.okay_command(event=event))  # an okay button focused return key press will call the okay command
            self.okay_button.bind("<KP_Enter>", lambda event: self.okay_command(event=event))  # an okay button focused keypad enter key press will call the okay command
            self.okay_button.bind("<Button-1>", lambda event: self.okay_command(event=event))  # an okay button mouse click will call the okay command

            self.popup.bind("<Escape>", lambda event: self.okay_command(event=event))  # an escape key press will call the okay command
            self.popup.bind("<Return>", lambda event: self.okay_command(event=event))  # a return key press will call the okay command
            self.popup.bind("<KP_Enter>", lambda event: self.okay_command(event=event))  # a keypad enter key press will call the okay command

            self.okay_button.bind("<FocusIn>", lambda event: self.on_focus_in(event=event))  # the okay button being focused on will call the on_focus_in method
            self.okay_button.bind("<FocusOut>", lambda event: self.on_focus_out(event=event))  # the okay button losing focus will call the on_focus_out method

            # do not put event in focus_set bindings
            self.okay_button.focus_set()  # set the initial focus to the okay button when the pop up window is created

        return self.popup  # return the pop up window

    def on_focus_in(self, event):  # method to be called when a button is focused on
        event.widget.config(bg="lightblue")  # change the background color of the button to light blue
        # Update the last_focused attribute based on which button has the focus
        if not self.okay_button_version:  # if the pop up window is using the yes/no version
            if event.widget == self.no_button:  # if the no button is focused on
                self.last_focused = "no_button"  # set the last_focused attribute to "no_button"
            elif event.widget == self.yes_button:  # if the yes button is focused on
                self.last_focused = "yes_button"  # set the last_focused attribute to "yes_button"
        else:  # if the pop up window is using the okay version
            if event.widget == self.okay_button:  # if the okay button is focused on
                self.last_focused = "okay_button"  # set the last_focused attribute to "okay_button"

    def on_focus_out(self, event):  # method to be called when a button loses focus
        event.widget.config(bg="gray75")  # change the background color of the button to gray75

    def restore_focus(self, event):  # method to restore focus to the last focused button when the pop up window regains focus
        if self.last_focused == "no_button":  # if the last focused button was the no button
            self.no_button.focus_set()  # set the focus to the no button
        elif self.last_focused == "yes_button":  # if the last focused button was the yes button
            self.yes_button.focus_set()  # set the focus to the yes button
        elif self.last_focused == "okay_button":  # if the last focused button was the okay button
            self.okay_button.focus_set()  # set the focus to the okay button
