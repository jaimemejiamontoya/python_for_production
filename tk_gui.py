import tkinter as tk
from tkinter import *

class CreateGUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self)

    # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

    # Create value lists
        self.option_menu_list = ["", "OptionMenu", "Option 1", "Option 2"]


    # Create control variables
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.IntVar(value=2)
        self.var_2 = tk.StringVar(value=self.option_menu_list[1])
        self.var_3 = tk.DoubleVar(value=50.0)

    # Create widgets :)
        self.setup_widgets()

    def setup_widgets(self):
        
     # Create a Frame for the Radiobuttons
        self.radio_frame = tk.LabelFrame(self, text="Radiobuttons", padx=20, pady=20)
        self.radio_frame.grid(row=0, column=0, padx=10, pady=20, sticky="nsew", rowspan=3)

    # Radiobuttons
        self.radio_1 = tk.Radiobutton(self.radio_frame, text="Unselected", variable=self.var_1, value=1)           
        self.radio_1.grid(row=0, column=0, padx=5, pady=10, sticky="W")

        self.radio_2 = tk.Radiobutton(self.radio_frame, text="Selected", variable=self.var_1, value=2)       
        self.radio_2.grid(row=1, column=0, padx=5, pady=10, sticky="W")

    # Checkbuttons
        self.check_1 = tk.Checkbutton(self.radio_frame, text="Toggle", variable=self.var_0)         
        self.check_1.grid(row=2, column=0, padx=5, pady=10, sticky="W")

     # Create a Frame for input widgets
        self.widgets_frame = tk.LabelFrame(self, text="Input Widgets", padx=0, pady=0)
        self.widgets_frame.grid(row=0, column=1, padx=0, pady=20, sticky="nsew", rowspan=3)
        self.widgets_frame.columnconfigure(index=0, weight=1)

    # Entry
        self.entry = tk.Entry(self.widgets_frame)
        self.entry.insert(0, "Text Entry")
        self.entry.grid(row=0, column=0, padx=5, pady=(10, 10), sticky="ew")

    # Spinbox
        self.spinbox = tk.Spinbox(self.widgets_frame, from_=0, to=100, increment=0.1)
        self.spinbox.insert(0, "Spinbox")
        self.spinbox.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

    # OptionMenu
        self.optionmenu = tk.OptionMenu(self.widgets_frame, self.var_2, *self.option_menu_list)
        self.optionmenu.config(width=20)
        self.optionmenu.grid(row=5, column=0, padx=5, pady=10, sticky="W")

    # Button
        self.button = tk.Button(self.widgets_frame, text="Button")
        self.button.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

    # Slider Label
        self.slider_label = Label(self.widgets_frame, text="Slider")
        self.slider_label.grid(row=7, column=0, sticky="W")  
    # Slider
        self.scale = tk.Scale(self.widgets_frame,from_=0,to=100,orient="horizontal", variable=self.var_3)
        self.scale.grid(row=8, column=0, padx=(0, 0), pady=(0, 0), sticky="ew")       


    # Panedwindow
        self.paned = tk.PanedWindow(self)
        self.paned.grid(row=0, column=2, padx=10, pady=20, sticky="nsew", rowspan=3)

    # Pane #1
        self.pane_1= tk.LabelFrame(self, text="Canvas", padx=20, pady=10)
        # self.pane_1 = tk.Frame(self.paned)
        self.paned.add(self.pane_1)

    # Canvas
        self.canvas = tk.Canvas(self.pane_1,width=200, height=200, highlightthickness=0, bg="grey")
        self.canvas.text = self.canvas.create_text(150, 75, width=200, text="", fill="#000000", font=("Arial", 20, "italic"))
        self.canvas.grid(row=0, column=0, columnspan=3, pady=10)



if __name__ == "__main__":
    root = tk.Tk()
    root.title("GUI Test Using Tkinter")

    app = CreateGUI(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()
