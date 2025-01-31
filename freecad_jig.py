import tkinter as tk
from tkinter import ttk

def get_variables(event=None): # function to get variables from entry boxes
    trim_width_str = width_entry.get() # get the width of trim from the entry box
    reveal_sixteenths_str = reveal_entry.get() # get the reveal in sixteenths from the entry box
    if trim_width_str and reveal_sixteenths_str:
        # make sure the input is a float for trim_width and integer for reveal_sixteenths
        try:
            trim_width = float(trim_width_str)
            reveal_sixteenths = int(reveal_sixteenths_str)
        except ValueError:
            print("Please enter a valid number")
            return
        print(trim_width, reveal_sixteenths)
        global trim_width_global, reveal_sixteenths_global
        trim_width_global = trim_width
        reveal_sixteenths_global = reveal_sixteenths

def create_ui(root):
    root.columnconfigure(0, weight=1) # make the column expandable
    root.rowconfigure(0, weight=1) # make the row expandable

    frame = ttk.Frame(root) # create a frame
    frame.grid(row=0, column=0, sticky="ewns") # add the frame to the root window, stick to the edges (east, west, north, south)
    frame.columnconfigure(0, weight=1) # make the column expandable inside the frame
    frame.rowconfigure(1, weight=1) # make the row expandable inside the frame  

    # make label for width
    width_label = ttk.Label(frame, text="Width of trim in inches.thousandths:") # create a label for the width entry box
    width_label.grid(row=0, column=0, padx=5, pady=5, sticky="w") # add the label to the frame

    # make field for width
    width_entry = ttk.Entry(frame) # create an entry box for the width
    width_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew") # add the entry box to the frame

    # make label for reveal
    reveal_label = ttk.Label(frame, text="No. of sixteenths in Reveal:") # create a label for the reveal entry box
    reveal_label.grid(row=1, column=0, padx=5, pady=5, sticky="w") # add the label to the frame

    # make field for reveal
    reveal_entry = ttk.Entry(frame) # create an entry box for the reveal
    reveal_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew") # add the entry box to the frame

    # make button to finish and exit
    entry_btn = ttk.Button(frame, text="Finish", command=root.quit) # create a button that quits the dialog.
    entry_btn.grid(row=2, column=1, padx=5, pady=5, sticky="e") # add the button to the frame

    # send inputs to get_variables
    entry_btn.bind("<Button-1>", get_variables) # bind the button to the get_variables function

    return width_entry, reveal_entry

if __name__ == "__main__":
    root = tk.Tk() # create the root window
    root.title("Test") # set the title
    width_entry, reveal_entry = create_ui(root)
    root.mainloop() # start the main event loop
