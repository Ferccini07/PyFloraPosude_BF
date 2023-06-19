# importing libraries
import random
import os
import sqlite3 as sql
import sys
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from Database.db import DB
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from weather_dhmz import get_current_weather

# storing images of plants in image list
image = []


# function for resizing image and store it in image list
def resize_image(img):
    try:
        img = Image.open(img)
        img = img.resize((150, 200))
        # converts image into a format that Tk can use to show it GUI
        img = ImageTk.PhotoImage(img)
        return image.append(img)
    except Exception as e:
        image.append("")
        print(str(e))


# function for opening a dialog box for choosing image at the time of adding/updating Pypot
def choose_image():
    file = askopenfilename(
        filetypes=[
            ("JPG", "*.jpg"),
            ("PNG", "*.png"),
            ("JPEG", "*.jpeg"),
            ("All", "*.*"),
        ],
        initialdir=os.getcwd(),
        title="Select Image",
    )
    if file:
        return file
    else:
        return None


# Main class that stores tkinter widgets and some functionalities
class Main(Tk):
    # basic variables for fonts
    bg_color = "Green1"
    font_name = "Calibri"
    font_size = 14
    font = (font_name, font_size)
    font_bold = (font_name, font_size, "bold")

    # Tkinter window variable
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # closing all programs / window when x icon clicked
        self.protocol("WM_DELETE_WINDOW", sys.exit)
        # list for holding multiple Pypot in Main window
        self.Pypot_frames_list = []
        # list for storing different data on same button "Show detail"
        self.show_detail_btn_list = []
        # variable for check user is inserting or updating Pypot
        self.insert_or_update = "insert"

        self.title("PyFloraPosude")
        self.geometry("880x780+150+30")

        # calling all GUI windows
        self.Header()
        self.login_window()
        self.register_window()
        self.weather_window()
        self.main_window()
        self.profile_window()
        self.Pypot_form()
        self.Pypot_details()

        # loop for getting the window of tkinter
        self.mainloop()

    def Header(self):
        # header main Frame
        header_frame = Frame(self, bg=self.bg_color, pady=15)
        header_frame.pack(fill=X)

        # header left side frame
        left_header = Frame(header_frame, bg=self.bg_color)
        left_header.pack(side=LEFT)

        # label left side
        Label(
            left_header,
            text="PyFloraPosude",
            font=(self.font_name, self.font_size + 10, "bold"),
            bg=self.bg_color,
        ).pack(side=LEFT, padx=130)

        # label left side - shows on mid
        self.label_plant = Label(
            left_header,
            text="Plants",
            font=(self.font_name, self.font_size + 10, "bold"),
            bg=self.bg_color,
        )

        # header right side frame
        right_header = Frame(header_frame, bg=self.bg_color)
        right_header.pack(side=RIGHT)

        # profile Button - right side
        self.profile_btn = Button(
            right_header,
            text="Profile",
            font=(self.font_name, self.font_size + 2, "bold"),
            command=lambda: self.load_profile_info(),
        )

    #  Login Window
    def login_window(self):
        # frame
        self.Login_frame = Frame(self)
        self.Login_frame.pack(fill=BOTH, expand=False)

        # Label
        Label(
            self.Login_frame,
            text="Login",
            font=(self.font_name, self.font_size + 10, "bold"),
        ).pack(pady=(120, 20))
        # label username -- text field /entry for username
        Label(self.Login_frame, text="Username", font=self.font_bold).pack(pady=2)
        self.username = Entry(self.Login_frame, width=30, font=self.font)
        self.username.pack(pady=(0, 15))

        # label password -- text field /entry for password
        Label(self.Login_frame, text="Password", font=self.font_bold).pack(pady=2)
        self.password_ = Entry(self.Login_frame, width=30, font=self.font, show="*")
        self.password_.pack(pady=(0, 20))

        # log in button
        Button(
            self.Login_frame,
            text="Login",
            font=self.font,
            width=22,
            command=lambda: self.login(),
        ).pack(pady=10)

    #  Login Window
    def register_window(self):
        # frame
        self.Register_frame = Frame(self)

        # Label
        Label(
            self.Register_frame,
            text="Register",
            font=(self.font_name, self.font_size + 10, "bold"),
        ).pack(pady=(120, 20))
        # label username -- text field /entry for username
        Label(self.Register_frame, text="Username", font=self.font_bold).pack(pady=2)
        self.username1 = Entry(self.Register_frame, width=30, font=self.font)
        self.username1.pack(pady=(0, 15))

        # label password -- text field /entry for password
        Label(self.Register_frame, text="Password", font=self.font_bold).pack(pady=2)
        self.password_add = Entry(
            self.Register_frame, width=30, font=self.font, show="*"
        )
        self.password_add.pack(pady=(0, 20))

        # log in button
        Button(
            self.Register_frame,
            text="Register",
            font=self.font,
            width=22,
            command=lambda: self.register(),
        ).pack(pady=10)

    # weather window
    def weather_window(self):
        self.Weather_frame = Frame(self)
        Label(
            self.Weather_frame,
            text="Current Weather - Zagreb, Croatia",
            font=(self.font_name, self.font_size + 12, "bold"),
        ).pack(pady=(50, 20))

        detail_frame = Frame(self.Weather_frame, pady=20, padx=40, bg=self.bg_color)
        detail_frame.pack()

        # displays each info from DHMZ site in separate row (Label)
        for row in get_current_weather():
            Label(
                detail_frame,
                text=row,
                font=(self.font_name, self.font_size + 2, "bold"),
                bg=self.bg_color,
            ).pack(pady=5)

        # continue button
        Button(
            self.Weather_frame,
            text="Continue",
            font=self.font,
            width=15,
            command=lambda: [
                self.Weather_frame.pack_forget(),
                self.Main_frame.pack(fill=BOTH, expand=True),
                self.profile_btn.pack(padx=60, side=LEFT),
                self.label_plant.pack(side=LEFT),
            ],
        ).pack(pady=20)

    # Main window
    def main_window(self):
        # Frame main
        self.Main_frame = Frame(self)

        # Frame for sync button
        sync_frame = Frame(self.Main_frame)
        sync_frame.pack(padx=150, pady=20, anchor=NE)

        # sync button
        Button(
            sync_frame,
            text="Sync",
            font=self.font,
            width=15,
            command=lambda: [
                messagebox.showinfo("success", "Data Synced Successfully."),
                self.refresh_Pypot(),
            ],
        ).pack(side=LEFT)

        # weather button
        Button(
            sync_frame,
            text="Weather",
            font=self.font,
            width=15,
            command=lambda: [
                self.Main_frame.pack_forget(),
                self.profile_btn.pack_forget(),
                self.label_plant.pack_forget(),
                self.Weather_frame.pack(fill=BOTH, expand=True),
            ],
        ).pack(pady=20)

        # frame for scroll view
        scroll_frame = Frame(self.Main_frame, padx=10, bg=self.bg_color)
        scroll_frame.bind("<Configure>", self.reset_scrollregion)
        scroll_frame.pack()

        # canvas
        self.t_canvas = Canvas(scroll_frame, width=740, height=530, bg=self.bg_color)

        # scrollbar
        scrollbar = ttk.Scrollbar(
            scroll_frame,
            orient=VERTICAL,
            command=self.t_canvas.yview,
        )

        # configure the scrollbar at canvas and binding it at canvas
        self.t_canvas.configure(yscrollcommand=scrollbar.set)
        self.t_canvas.bind(
            "<Configure>",
            lambda e: self.t_canvas.configure(scrollregion=self.t_canvas.bbox("all")),
        )

        # frame with scrollbar
        self.Pypot_frame = Frame(self.t_canvas, bg=self.bg_color)
        self.Pypot_frame.pack(side=TOP, anchor=CENTER)

        self.t_canvas.create_window((0, 0), window=self.Pypot_frame, anchor="nw")

        # packing the scroll canvas and scrollbar
        scrollbar.pack(side=RIGHT, fill=Y)
        self.t_canvas.pack(side=TOP, fill=X, anchor=CENTER)

        # call refresh Pypot to show existed Pypot
        self.refresh_Pypot()

    def reset_scrollregion(self, event):
        self.t_canvas.configure(scrollregion=self.t_canvas.bbox("all"))

    # Display/Refresh Pypot on window
    def refresh_Pypot(self):
        # removing all previous widgets from Pypot frame
        for widget in self.Pypot_frame.winfo_children():
            widget.destroy()

        # clearing show detail list button
        self.show_detail_btn_list.clear()

        # getting the Pypot data form database by call the get Pypot function from database.py
        self.Pypot_data = db.get_Pypot()

        # variable row_pot for getting the row number for Pypot
        row_pot = -1
        # column_pot for getting the column for Pypot in grid method
        column_pot = 0
        # variable count for getting the loop count
        count = 0
        # loop with Pypot data
        for row in self.Pypot_data:
            # if 2 Pypots are placed next to each other then reset the column to 0 and increment row_pot by 1
            if (count % 2) == 0:
                row_pot += 1
                column_pot = 0
            # if plant is planted in pot then
            if row[3] != "Empty":
                # get random status
                plant_status = random.choice(["Needs Watering", "OK", "Needs Light"])
            # if plant not planted then
            else:
                # plant status is empty
                plant_status = row[3]
            # if there is an image of plant then
            if row[-1] != "":
                # resize the image
                resize_image(row[-1])
                # and variable check image = true
                check_img = True
            else:
                # else False
                check_img = False
            # call function create Pypot with parameters
            self.create_PyPot(
                row[2], check_img, plant_status, row_pot, column_pot, count
            )
            # next column_pot
            column_pot = 1
            # increment count by 1
            count += 1

        # Frame for adding a new Pypot
        self.add_Pypot_frame = LabelFrame(self.Pypot_frame, width=350, height=200)
        # if total number of Pypots is dividable by 2 then column_pot = 0
        if len(self.Pypot_data) % 2 == 0:
            column_pot = 0
            # and row_pot increment by 1
            row_pot += 1
        else:
            # else column_pot =1
            column_pot = 1

        # placing or showing it on GUI
        self.add_Pypot_frame.grid(row=row_pot, column=column_pot, padx=(10, 20))
        # fixing size of frame
        self.add_Pypot_frame.propagate(False)
        # add new Pypot button and plus sign label
        Label(
            self.add_Pypot_frame,
            text="+",
            font=(self.font_name, self.font_size + 25, "bold"),
        ).pack(pady=(30, 10))
        Button(
            self.add_Pypot_frame,
            text="Add Pypot",
            font=self.font,
            command=lambda: self.open_add_Pypot_window(),
        ).pack(pady=(0, 30))

    #  Create Pypot in main page
    def create_PyPot(self, Pypot_name, plant_img, status, row_pot, column_pot, count):
        # if there is image then store it in img variable
        if plant_img:
            img = image[-1]
        else:
            # else image of plant not added
            img = None

        # Frame for one instance of Pypot in main_window
        Pypot = LabelFrame(self.Pypot_frame, width=350, height=200)
        Pypot.grid(row=row_pot, column=column_pot, padx=(10, 20), pady=15)
        # fixng size
        Pypot.propagate(False)

        # storing the frame in list
        self.Pypot_frames_list.append(Pypot)

        # adding Image frame
        image_frame = Frame(Pypot, width=130, height=200)
        image_frame.pack(side=LEFT)
        # fixing image frame size
        image_frame.propagate(False)

        # adding image label for plant image
        plant_image = Label(image_frame, image=img)
        plant_image.pack(side=LEFT)

        # detail frame
        detail_frame = Frame(Pypot)
        detail_frame.pack(side=LEFT, fill=BOTH, expand=1)

        # Label for Pypot name
        Label(
            detail_frame,
            text=Pypot_name,
            font=(self.font_name, self.font_size - 2),
            justify="left",
        ).pack(padx=(2, 0), pady=10, anchor=NW)

        # adding show detail btn in list
        self.show_detail_btn_list.append(
            Button(detail_frame, text="Show Detail", font=self.font)
        )

        # binding command for loading the data with right details
        self.show_detail_btn_list[count].config(
            command=lambda x=count: [
                # hiding main window and show Pypot detail window
                self.Main_frame.pack_forget(),
                self.Pypot_detail_frame.pack(fill=BOTH, expand=1),
                self.display_Pypot_details(self.Pypot_data[count], count),
            ]
        )
        # showing the button on window
        self.show_detail_btn_list[count].pack()
        # status label
        Label(detail_frame, text="Status: " + status, justify="left").pack(
            side=BOTTOM, anchor=NW, pady=5, padx=15
        )

    # Add & edit Pypot
    def Pypot_form(self):
        # Pypot form frame
        self.Pypot_form_frame = Frame(self)

        # Lable
        Label(
            self.Pypot_form_frame,
            text="PyPot & Plant info",
            font=(self.font_name, self.font_size + 12, "bold"),
        ).pack(pady=(40, 20))

        # Labelframe
        plant_info_frame = LabelFrame(
            self.Pypot_form_frame, padx=20, pady=10, bg=self.bg_color
        )
        plant_info_frame.pack(pady=10)

        # entry for holding Pypot id not showing it on GUI
        self.Pypot_id = Entry(plant_info_frame, width=22, font=self.font)

        # Pypot name label and text field entry
        Label(
            plant_info_frame, text="PyPot Name", font=self.font_bold, bg=self.bg_color
        ).grid(row=0, column=0, pady=10)
        self.Pypot_name = Entry(plant_info_frame, width=22, font=self.font)
        self.Pypot_name.grid(row=1, column=0, padx=30)

        # Planted label and dropdown option field
        Label(
            plant_info_frame,
            text="Planted Plant",
            font=self.font_bold,
            bg=self.bg_color,
        ).grid(row=0, column=1, padx=5, pady=10)
        self.planted_plant = ttk.Combobox(
            plant_info_frame,
            width=20,
            font=self.font,
            state="readonly",
            values=("Yes", "Empty"),
        )
        self.planted_plant.grid(row=1, column=1)
        # setting the second value in dropdown as default
        self.planted_plant.current(1)
        # binding function empty_Pypot for check the Pypot is empty or not
        self.planted_plant.bind("<<ComboboxSelected>>", self.empty_Pypot)

        # Plant name label and text field
        Label(
            plant_info_frame, text="Plant Name", font=self.font_bold, bg=self.bg_color
        ).grid(row=2, column=0, pady=10)
        self.plant_name = Entry(
            plant_info_frame, width=22, font=self.font, state="disabled"
        )
        self.plant_name.grid(row=3, column=0, padx=30)

        # watering label and drop down field
        Label(
            plant_info_frame,
            text="Watering timing",
            font=self.font_bold,
            bg=self.bg_color,
        ).grid(row=2, column=1, pady=10)
        self.watering = ttk.Combobox(
            plant_info_frame,
            width=20,
            font=self.font,
            state="disabled",
            values=("day", "week", "month"),
        )
        self.watering.grid(row=3, column=1)
        # setting the first value in dropdown as default
        self.watering.current(0)

        # plant place label and combobox
        Label(
            plant_info_frame, text="Place", font=self.font_bold, bg=self.bg_color
        ).grid(row=4, column=0, pady=10)
        self.place = ttk.Combobox(
            plant_info_frame,
            width=20,
            font=self.font,
            state="disabled",
            values=(
                "lighter & warmer",
                "lighter & colder",
                "darker & warmer",
                "darker & colder",
            ),
        )
        self.place.grid(row=5, column=0)
        # setting the first value in dropdown as default
        self.place.current(0)

        # moisture soil sensor label and combobox
        Label(
            plant_info_frame,
            text="Moisture Sensor",
            font=self.font_bold,
            bg=self.bg_color,
        ).grid(row=4, column=1, pady=10)
        self.moisture_sensor = ttk.Combobox(
            plant_info_frame,
            width=20,
            font=self.font,
            state="disabled",
            values=("Active", "Inactive"),
        )
        self.moisture_sensor.grid(row=5, column=1)
        # setting the second value in dropdown as default
        self.moisture_sensor.current(1)

        # ph sensor label and combobox
        Label(
            plant_info_frame,
            text="pH sensor",
            font=self.font_bold,
            bg=self.bg_color,
        ).grid(row=6, column=0, pady=10)
        self.pH_sensor = ttk.Combobox(
            plant_info_frame,
            width=20,
            font=self.font,
            state="disabled",
            values=("Active", "Inactive"),
        )
        self.pH_sensor.grid(row=7, column=0)
        # setting the second value in dropdown as default
        self.pH_sensor.current(1)

        # light sensor label and combobox
        Label(
            plant_info_frame, text="Light Sensor", font=self.font_bold, bg=self.bg_color
        ).grid(row=6, column=1, pady=10)
        self.light_sensor = ttk.Combobox(
            plant_info_frame,
            width=20,
            font=self.font,
            state="disabled",
            values=("Active", "Inactive"),
        )
        self.light_sensor.grid(row=7, column=1)
        # setting the second value in dropdown as default
        self.light_sensor.current(1)

        # path frame for photo
        path_frame = LabelFrame(
            self.Pypot_form_frame,
            text="Plant Image",
            padx=10,
            pady=10,
            bg=self.bg_color,
        )
        path_frame.pack(pady=5)
        # plant image label and path field
        self.path = Label(path_frame, width=40, font=self.font, bg=self.bg_color)
        self.path.pack(side=LEFT, padx=(0, 2))
        self.img_loc_btn = Button(
            path_frame,
            text="Browser",
            font=self.font,
            width=10,
            command=lambda: self.browser_image(),
        )
        self.img_loc_btn.pack(side=RIGHT, padx=(0, 0))
        # frame for buttons
        btn_frame = Frame(self.Pypot_form_frame)
        btn_frame.pack(pady=30)
        # save btn
        Button(
            btn_frame,
            text="Save",
            font=self.font,
            width=10,
            command=lambda: self.add_update_Pypot_data(self.insert_or_update),
        ).pack(side=LEFT, padx=40)
        # back btn
        Button(
            btn_frame,
            text="Back",
            font=self.font,
            width=10,
            command=lambda:
            # hiding Pypot form window and showing main window also refreshing Pypot
            [
                self.Pypot_form_frame.pack_forget(),
                self.Main_frame.pack(fill=BOTH, expand=1),
                self.refresh_Pypot(),
                self.clear_Pypot_fields(),
            ],
        ).pack(side=LEFT, padx=(50, 10))

    # Pypot detail page
    def Pypot_details(self):
        # detail frame
        self.Pypot_detail_frame = Frame(self)

        # frame for image and Pypot details
        middle_frame = Frame(self.Pypot_detail_frame)
        middle_frame.pack(pady=10)

        # label frame with PyPot name
        self.plant_info_frame = LabelFrame(
            middle_frame,
            text="PyPot Name",
            bg=self.bg_color,
            font=(self.font_name, self.font_size + 2, "bold"),
            width=300,
            height=260,
        )
        self.plant_info_frame.pack(side=LEFT, padx=(0, 100))
        # fixing size
        self.plant_info_frame.propagate(False)
        # label for plant name
        self.detail_plant_name = Label(
            self.plant_info_frame,
            text="Plant Name: Rose",
            font=self.font_bold,
            bg=self.bg_color,
        )
        self.detail_plant_name.pack(pady=(10, 5), anchor=NW, padx=10)
        # label for water
        self.detail_water = Label(
            self.plant_info_frame,
            text="Watering: Once a day",
            font=self.font_bold,
            bg=self.bg_color,
        )
        self.detail_water.pack(anchor=NW, padx=10)
        # label for place
        self.detail_plant_place = Label(
            self.plant_info_frame,
            text="Place: Dark & Warmer",
            font=self.font_bold,
            bg=self.bg_color,
        )
        self.detail_plant_place.pack(pady=5, anchor=NW, padx=10)
        # label for moisture sensor
        self.moisture_sensor_lb = Label(
            self.plant_info_frame,
            text="Moisture Sensor: Active",
            font=self.font_bold,
            bg=self.bg_color,
        )
        self.moisture_sensor_lb.pack(anchor=NW, padx=10)
        # label for pH sensor
        self.ph_sensor_lb = Label(
            self.plant_info_frame,
            text="pH Sensor: Active",
            font=self.font_bold,
            bg=self.bg_color,
        )
        self.ph_sensor_lb.pack(anchor=NW, padx=10)
        # label for light sensor
        self.light_sensor_lb = Label(
            self.plant_info_frame,
            text="Light Sensor: Active",
            font=self.font_bold,
            bg=self.bg_color,
        )
        self.light_sensor_lb.pack(pady=5, anchor=NW, padx=10)

        # frame for image
        d_image_frame = Frame(middle_frame, width=250, height=200)
        d_image_frame.pack(side=RIGHT)
        # size fixing
        d_image_frame.propagate(False)
        # image label
        self.d_image = Label(d_image_frame, image="")
        self.d_image.pack(side=RIGHT)

        # detail btn frame
        detail_buttons_frame = Frame(self.Pypot_detail_frame)
        detail_buttons_frame.pack(pady=10)
        # bluetooth btn
        self.bluetooth_btn = Button(
            detail_buttons_frame,
            text="Bluetooth ON",
            font=self.font,
            width=10,
            command=lambda: self.bluetooth(),
        )
        self.bluetooth_btn.grid(row=0, column=0, padx=5, pady=4)
        # back button
        Button(
            detail_buttons_frame,
            text="Back",
            font=self.font,
            width=10,
            command=lambda: [
                self.Pypot_detail_frame.pack_forget(),
                self.Main_frame.pack(fill=BOTH, expand=1),
            ],
        ).grid(row=0, column=1)
        # update btn
        Button(
            detail_buttons_frame,
            text="Update",
            font=self.font,
            width=10,
            command=lambda: self.Pypot_for_update(),
        ).grid(row=0, column=2)
        # update btn
        Button(
            detail_buttons_frame,
            text="Delete",
            font=self.font,
            width=10,
            command=lambda: self.delete_Pypot(),
        ).grid(row=0, column=3)

        # frame for graphs
        self.bottom_frame = Frame(self.Pypot_detail_frame, bg=self.bg_color)
        self.bottom_frame.pack(side=BOTTOM, pady=5)

        # adding tabs
        tabControl = ttk.Notebook(self.bottom_frame, width=650, height=240)
        # three  frames
        tab1 = Frame(tabControl, bg=self.bg_color)
        tab2 = Frame(tabControl, bg=self.bg_color)
        tab3 = Frame(tabControl, bg=self.bg_color)
        # adding text and tabs
        tabControl.add(tab1, text="Line")
        tabControl.add(tab2, text="Pie")
        tabControl.add(tab3, text="Histo")
        # show the tabs on GUI
        tabControl.pack(fill=X)
        # frame on first tab
        self.line_chart_plot = Frame(tab1)
        self.line_chart_plot.pack(fill=BOTH)
        # image label on 2nd tab
        self.pie_chart_plot = Frame(tab2)
        self.pie_chart_plot.pack(fill=BOTH)
        # image label on 3rd tab
        self.histo_chart_plot = Frame(tab3)
        self.histo_chart_plot.pack(fill=BOTH)

    # profile page
    def profile_window(self):
        # profile frame
        self.Profile_frame = Frame(self)

        # heading label
        Label(
            self.Profile_frame,
            text="Profile",
            font=(self.font_name, self.font_size + 12, "bold"),
        ).pack(pady=(120, 20))

        # frame
        profile_info_frame = Frame(
            self.Profile_frame, bg=self.bg_color, pady=20, padx=40
        )
        profile_info_frame.pack(pady=10)

        # firstname label and text field
        Label(
            profile_info_frame, text="First Name", font=self.font_bold, bg=self.bg_color
        ).grid(row=0, column=0, sticky=W, padx=5, pady=10)
        self.first_name = Entry(profile_info_frame, width=20, font=self.font)
        self.first_name.grid(row=0, column=1)

        # lastname label and text field
        Label(
            profile_info_frame, text="Last Name", font=self.font_bold, bg=self.bg_color
        ).grid(row=1, column=0, sticky=W, padx=5, pady=10)
        self.last_name = Entry(profile_info_frame, width=20, font=self.font)
        self.last_name.grid(row=1, column=1)

        # Username label and text field
        Label(
            profile_info_frame, text="User Name", font=self.font_bold, bg=self.bg_color
        ).grid(row=2, column=0, sticky=W, padx=5, pady=10)
        self.user_name = Entry(profile_info_frame, width=20, font=self.font)
        self.user_name.grid(row=2, column=1)

        # password label and text field
        Label(
            profile_info_frame, text="Password", font=self.font_bold, bg=self.bg_color
        ).grid(row=3, column=0, sticky=W, padx=5, pady=10)
        self.password = Entry(profile_info_frame, width=20, font=self.font, show="*")
        self.password.grid(row=3, column=1)

        # btn frame
        btn_frame = Frame(self.Profile_frame)
        btn_frame.pack(pady=10)

        # save btn
        Button(
            btn_frame,
            text="Save",
            font=self.font,
            width=10,
            command=lambda: self.update_profile_info(),
        ).pack(side=LEFT, padx=5)

        # back btn
        Button(
            btn_frame,
            text="Back",
            font=self.font,
            width=10,
            command=lambda: [
                self.Profile_frame.pack_forget(),
                self.Main_frame.pack(fill=BOTH, expand=1),
            ],
        ).pack(side=RIGHT, padx=5)

        self.logout_btn = Button(
            self.Profile_frame,
            text="Log out",
            fg="white",
            bg="red",
            font=self.font,
            width=20,
            command=lambda: [
                self.Login_frame.pack(fill=BOTH, expand=True),
                self.Main_frame.pack_forget(),
                self.Pypot_detail_frame.pack_forget(),
                self.Pypot_form_frame.pack_forget(),
                self.Profile_frame.pack_forget(),
                self.profile_btn.pack_forget(),
                self.label_plant.pack_forget(),
            ],
        )
        self.logout_btn.pack(pady=5)


# class which contain all logic code of program like insert, update, delete data or other operations
class Logic(Main):
    # login function for user validation
    def login(self):
        # getting username and password from text fileds
        username = self.username.get()
        password = self.password_.get()
        # if not empty
        if username != "" and password != "":
            # get user data form db
            self.user_info = db.get_user(username)
            res = self.user_info
            # if there is data and username and password equal to entered username and password
            if res is not None and (username == res[3] and password == res[4]):
                # hide login window
                self.Login_frame.pack_forget()
                # self.logout_btn.pack(padx=(10, 60), side=LEFT)
                self.password_.delete(0, END)
                # show main window
                self.Weather_frame.pack(expand=True, fill=BOTH)
            else:
                # if login failed show this msg
                messagebox.showwarning("Failed", "InValid Username or Password")
        else:
            # if username and password fields are empty
            messagebox.showwarning("Failed", "Username or password missing...")

    def register(self):
        # getting username and password from text fileds
        username = self.username1.get()
        password = self.password_add.get()
        # if not empty
        if username != "" and password != "":
            # get user data form db
            self.user_info = db.insert_profile(username)
            res = self.user_info
            # if there is data and username and password equal to entered username and password
            if res is not None and (username == res[3] and password == res[4]):
                # hide login window
                self.Register_frame.pack_forget()
                # self.logout_btn.pack(padx=(10, 60), side=LEFT)
                self.password_add.delete(0, END)
                # show main window
                self.Register_frame.pack(fill=BOTH, expand=True)
            else:
                # if login failed show this msg
                messagebox.showwarning("Failed", "2 InValid Username or Password")
        else:
            # if username and password fields are empty
            messagebox.showwarning("Failed", "2 Username or password missing...")

    # load profile data function
    def load_profile_info(self):
        # clearing profile text fields
        self.first_name.delete(0, END)
        self.last_name.delete(0, END)
        self.user_name.delete(0, END)
        self.password.delete(0, END)
        # loading user profile info on text fields
        self.first_name.insert(0, self.user_info[1])
        self.last_name.insert(0, str(self.user_info[2]))
        self.user_name.insert(0, self.user_info[3])
        self.password.insert(0, self.user_info[4])
        # hiding main page
        self.Main_frame.pack_forget()
        self.Pypot_form_frame.pack_forget()
        self.Pypot_detail_frame.pack_forget()
        # showing profile page
        self.Profile_frame.pack(fill=BOTH, expand=1)

    # update profile data function
    def update_profile_info(self):
        # get values from fields
        f_name = self.first_name.get()
        l_name = self.last_name.get()
        u_name = self.user_name.get()
        u_pass = self.password.get()
        # if first name, username and password is not empty
        if f_name != "" and u_name != "" and u_pass != "":
            # update profile data by calling the update profile function from database.py file
            result = db.update_profile(
                data=[f_name, l_name, u_name, u_pass, self.user_info[0]]
            )
            # show message
            messagebox.showinfo("Info", result)
            # update user data info in user_info variable
            self.user_info = db.get_user(u_name)
            # call load_profile_info function
            self.load_profile_info()
        else:
            # if fields are empty show this message
            messagebox.showwarning("Warning", "Some fields data are missing...")

    # function for show Pypot form window
    def open_add_Pypot_window(self):
        # set the variable to insert
        self.insert_or_update = "insert"
        self.Main_frame.pack_forget()
        self.Pypot_form_frame.pack(fill=BOTH, expand=1)

    # clearing Pypot fields functions
    def clear_Pypot_fields(self):
        self.Pypot_id.delete(0, END)
        self.Pypot_name.delete(0, END)
        self.planted_plant.current(1)
        self.plant_name.delete(0, END)
        self.watering.current(0)
        self.place.current(0)
        self.moisture_sensor.current(1)
        self.pH_sensor.current(1)
        self.light_sensor.current(1)
        self.path.config(text="")
        self.empty_Pypot(None)

    # enabling and disabling Pypot form fields based on the planted plant state
    def empty_Pypot(self, event):
        # it selected empty
        if self.planted_plant.get() == "Empty":
            # disable these fields
            self.plant_name.config(state="disabled")
            self.watering.config(state="disabled")
            self.place.config(state="disabled")
            self.moisture_sensor.config(state="disabled")
            self.pH_sensor.config(state="disabled")
            self.light_sensor.config(state="disabled")
            # self.path.config(state='disabled')
            self.img_loc_btn.config(state="disabled")
        else:
            # if yes then enabled
            self.plant_name.config(state="normal")
            self.watering.config(state="readonly")
            self.place.config(state="readonly")
            self.moisture_sensor.config(state="readonly")
            self.pH_sensor.config(state="readonly")
            self.light_sensor.config(state="readonly")
            # self.path.config(state='normal')
            self.img_loc_btn.config(state="normal")

    # adding/updating Pypot data
    def add_update_Pypot_data(self, state):
        # get data from fields
        id = self.Pypot_id.get()
        pot_name = self.Pypot_name.get()
        plant_State = self.planted_plant.get()
        plant_name = self.plant_name.get()
        water = self.watering.get()
        plant_place = self.place.get()
        sensor_1 = self.moisture_sensor.get()
        sensor_2 = self.pH_sensor.get()
        sensor_3 = self.light_sensor.get()
        path = self.path.cget("text")
        result = ""
        # fields not empty and planted plant is Yes or empty
        if pot_name != "" and (
            (plant_name != "" and plant_State == "Yes") or plant_State == "Empty"
        ):
            # get current date
            date = datetime.now()
            # change format of date
            date = date.strftime("%Y-%m-%d %H:%M:%S")
            # if plant planted
            if plant_State == "Yes":
                # list plant and Pypot info
                data = [
                    str(date),
                    pot_name,
                    plant_State,
                    plant_name,
                    water,
                    plant_place,
                    sensor_1,
                    sensor_2,
                    sensor_3,
                    path,
                ]
            else:
                # if planted plant is empty
                # list of Pypot info only
                data = [str(date), pot_name, plant_State, "", "", "", "", "", "", ""]
            # if inserting
            if state == "insert":
                # call dml queries function from database.py file
                result = db.dml_queries(state, data, None)
            # else if updating
            elif state == "update":
                # call dml queries function from database.py file
                result = db.dml_queries(state, data, id)
            # show success msg
            messagebox.showinfo("Success", result)
            # clear fields
            self.clear_Pypot_fields()
            # refresh Pypot on GUI
            self.refresh_Pypot()
            # hide form window
            self.Pypot_form_frame.pack_forget()
            # show main widow
            self.Main_frame.pack(fill=BOTH, expand=1)
        else:
            # Pypot or plant field is empty show this msg
            messagebox.showwarning("Missing", "Pypot name or Plant name can't be null.")

    # delete Pypot function
    def delete_Pypot(self):
        # getting data
        data = self.Pypot_data[int(self.Pypot_index)]
        id = data[0]
        # run dml queries function from database.py for deleting Pypot
        res = db.dml_queries("delete", None, id)
        # show msg
        messagebox.showinfo("Success", res)
        # refresh Pypot data
        self.refresh_Pypot()
        # hide Pypot detail window
        self.Pypot_detail_frame.pack_forget()
        # show main window
        self.Main_frame.pack(fill=BOTH, expand=1)

    # load Pypot details function
    def display_Pypot_details(self, data, index):
        # storing index
        self.Pypot_index = index
        # if there is image show image
        try:
            global new_image
            # open and resize it 250x250
            new_image = Image.open(data[-1]).resize(
                (250, 200), Image.Resampling.LANCZOS
            )
            new_image = ImageTk.PhotoImage(new_image)
            # show it on GUI
            self.d_image.config(image=new_image)
        except:
            # if no image now no Image text
            self.d_image.config(image="", text="No Image")
        # if plant planted in Pypot call graphs
        if data[3] == "Yes":
            # line
            self.line_chart()
            # pie
            self.pie_chart()
            # histo
            self.histo_chart()
        else:
            # else if Pypot is empty remove graphs
            try:
                self.line_chart_canvas.get_tk_widget().destroy()
                self.pie_chart_canvas.get_tk_widget().destroy()
                self.histo_chart_canvas.get_tk_widget().destroy()
            except Exception as e:
                print(e)
        # change data on Pypot detail GUI window
        self.plant_info_frame.config(text=str(data[2]))
        self.detail_plant_name.config(text="Plant Name: " + str(data[4]))
        self.detail_water.config(text="Watering: " + str(data[5]))
        self.detail_plant_place.config(text="Place: " + str(data[6]))
        if data[7] == "Active":
            moisture_sensor_lb_value = self.moisture
        else:
            moisture_sensor_lb_value = data[7]
        if data[8] == "Active":
            ph_sensor_lb_value = self.ph
        else:
            ph_sensor_lb_value = data[8]
        if data[9] == "Active":
            light_sensor_lb_value = self.light
        else:
            light_sensor_lb_value = data[9]

        self.moisture_sensor_lb.config(
            text="Moisture Sensor: " + str(moisture_sensor_lb_value)
        )
        self.ph_sensor_lb.config(text="pH Sensor: " + str(ph_sensor_lb_value))
        self.light_sensor_lb.config(text="Light Sensor: " + str(light_sensor_lb_value))

    # function for updating Pypot info
    def Pypot_for_update(self):
        # set variable for update
        self.insert_or_update = "update"
        # get data from list
        data = self.Pypot_data[int(self.Pypot_index)]

        # load data in Pypot form window
        self.Pypot_id.insert(0, data[0])
        self.Pypot_name.insert(0, data[2])
        self.planted_plant.set(data[3])
        self.empty_Pypot(None)
        self.plant_name.insert(0, data[4])
        self.watering.set(data[5])
        self.place.set(data[6])
        self.moisture_sensor.set(data[7])
        self.pH_sensor.set(data[8])
        self.light_sensor.set(data[9])
        self.path.config(text=data[10])

        # hide Pypot detail window
        self.Pypot_detail_frame.pack_forget()

        # show Pypot form frame
        self.Pypot_form_frame.pack(fill=BOTH, expand=True)

    def browser_image(self):
        image_path = choose_image()
        if image_path:
            self.path.config(text=image_path)

    # graphs functions
    def line_chart(self):
        # s
        self.generate_sensor_values()
        # plotting/creating graph
        fig = Figure(figsize=(8, 3.1), dpi=80)
        pl = fig.add_subplot(111)
        pl.plot(self.sensors, self.values)
        # Using canvas for showing graph on window

        # creating canvas containing the Matplotlib graph
        self.line_chart_canvas = FigureCanvasTkAgg(fig, master=self.line_chart_plot)
        self.line_chart_canvas.draw()

        # placing the canvas on the window
        self.line_chart_canvas.get_tk_widget().grid(row=0, column=0)

    def pie_chart(self):
        # Plotting/Creating plot
        fig = plt.figure(figsize=(8, 3.1), dpi=80)
        plt.pie(self.values, labels=self.sensors)

        self.pie_chart_canvas = FigureCanvasTkAgg(fig, master=self.pie_chart_plot)
        self.pie_chart_canvas.draw()

        # placing the canvas on the window
        self.pie_chart_canvas.get_tk_widget().grid(row=0, column=0)

    def histo_chart(self):
        fig = plt.figure(figsize=(8, 3.1), dpi=80)
        # plot graph
        plt.bar(self.sensors, self.values)
        # Showing graph
        self.histo_chart_canvas = FigureCanvasTkAgg(fig, master=self.histo_chart_plot)
        self.histo_chart_canvas.draw()

        # placing the canvas on the window
        self.histo_chart_canvas.get_tk_widget().grid(row=0, column=0)

    def generate_sensor_values(self):
        # simulate data for water level (from 0 to 10)
        self.water_level = round(random.uniform(0, 10), 2)
        # simulate data for light level (from 0 to 10)
        self.light = round(random.uniform(0, 10), 2)
        # simulate data for soil moisture (from 0.5 to 5.5)
        self.moisture = round(random.uniform(0.5, 5.5), 2)
        # simulate soil moisture data (from 10% to 20%)
        self.humidity = round(random.uniform(10, 20), 2)
        # simulate soil pH data
        self.ph = round(random.uniform(0, 14), 2)
        # x and y variable data
        self.sensors = ["Water", "Light", "Moisture", "Humidity", "pH"]
        self.values = [
            self.water_level,
            self.light,
            self.moisture,
            self.humidity,
            self.ph,
        ]

    def bluetooth(self):
        if self.bottom_frame.winfo_ismapped():
            self.bottom_frame.pack_forget()
            self.bluetooth_btn.configure(text="Bluetooth Off")
        else:
            self.bottom_frame.pack(side=BOTTOM, pady=5)
            self.bluetooth_btn.configure(text="Bluetooth On")


# calling DB and Logic classes
db = DB()
lg = Logic()
