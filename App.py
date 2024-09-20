"""
An extended version of main.py implemented with oop.
"""

from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import pandas as pd
import threading

font_path = 'GreatVibes-Regular.ttf'
font_size = 110
text_color = "#283361"
alignment = 'center'


def print_certificate(image_path, text, font_path, font_size, position, text_color, output_path, alignment,
                      file_format):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    text_width = draw.textlength(text, font=font)

    if alignment == 'center':
        position = (position[0] - text_width // 2, position[1])

    elif alignment == 'right':
        position = (position[0] - text_width, position[1])

    draw.text(position, text, fill=text_color, font=font)
    image.convert('RGB').save(output_path + "/" + text + "." + str(file_format).lower(), format=file_format,
                              resolution=100.0)


def write_config(position, file_path, certificate_path, output_path):
    with open(".config", "w") as conf_file:
        conf_file.write(str(position[0]) + "," + str(position[1]) + "\n")
        conf_file.write(certificate_path + "\n")
        conf_file.write(file_path + "\n")
        conf_file.write(output_path)


class AppWindow:
    def __init__(self, default_position: str, default_certificate: str, default_file: str, default_output: str):
        self.default_output = default_output
        self.default_file = default_file
        self.default_certificate = default_certificate
        self.default_position = default_position

        self.root = tk.Tk()
        self.file_path = tk.StringVar()
        self.certificate_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.position = tk.StringVar()
        self.selected_format = tk.StringVar()
        self.start_button = None
        self.root.title("Certificate Generator")

        self.config_interface()

        self.root.mainloop()

    def config_interface(self):

        self.position.set(self.default_position)
        self.certificate_path.set(self.default_certificate)
        self.file_path.set(self.default_file)
        self.output_path.set(self.default_output)

        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=10)

        options = ["PDF", "PNG", "JPEG"]

        self.selected_format.set(options[0])

        tk.Label(title_frame, text="Certificate Generator", font=("Arial Bold", 20)).pack()

        frame_1 = tk.Frame(self.root)
        frame_1.pack(pady=10)

        tk.Label(frame_1, text="Certificate Path: ").grid(column=0, row=0)
        certificate_path_new = tk.Entry(frame_1, textvariable=self.certificate_path)
        certificate_path_new.grid(column=1, row=0)
        tk.Button(frame_1, text="Browse", command=self.ask_for_certificate_path).grid(column=2, row=0)

        tk.Label(frame_1, text="File Path: ").grid(column=0, row=1)
        file_path_new = tk.Entry(frame_1, textvariable=self.file_path)
        file_path_new.grid(column=1, row=1)
        tk.Button(frame_1, text="Browse", command=self.ask_for_file_path).grid(column=2, row=1)

        tk.Label(frame_1, text="Text position: ").grid(column=0, row=2)
        position_new = tk.Entry(frame_1, textvariable=self.position)
        position_new.grid(column=1, row=2)

        tk.Label(frame_1, text="Output Path: ").grid(column=0, row=3)
        output_path_new = tk.Entry(frame_1, textvariable=self.output_path)
        output_path_new.grid(column=1, row=3)
        tk.Button(frame_1, text="Browse", command=self.ask_for_output_path).grid(column=2, row=3)

        tk.Label(frame_1, text="Output Formate: ").grid(column=0, row=4)
        dropdown = tk.OptionMenu(frame_1, self.selected_format, *options)
        dropdown.grid(column=1, row=4)

        self.start_button = tk.Button(self.root, text=" Generate ", width=20, command=self.check_args)
        self.start_button.pack(pady=10)

    def ask_for_file_path(self):
        usr_def_path = filedialog.askopenfilename(title="Select a file")
        if usr_def_path:
            self.file_path.set(usr_def_path)

    def ask_for_certificate_path(self):
        usr_def_path = filedialog.askopenfilename(title="Select a file")
        if usr_def_path:
            self.certificate_path.set(usr_def_path)

    def ask_for_output_path(self):
        usr_def_path = filedialog.askdirectory(title="Select a file")
        if usr_def_path:
            self.output_path.set(usr_def_path)

    def check_args(self):
        try:
            pos_x, pos_y = self.position.get().split(",")
            pos_x, pos_y = int(pos_x), int(pos_y)

        except ValueError:
            messagebox.showerror("Value Error", "Position should be in the formate: \nint,int")
            return

        if not os.path.isfile(self.certificate_path.get()):
            messagebox.showerror("Path Error", "Certificate path is invalid.")
            return

        elif not os.path.isfile(self.file_path.get()):
            messagebox.showerror("Path Error", "Input File path is invalid.")
            return

        elif not os.path.isdir(self.output_path.get()):
            messagebox.showerror("Path Error", "Output path is invalid.")
            return

        else:
            self.start_button.config(text=" Generating... ", command="")
            printing_thread = threading.Thread(target=self.format_print, args=(
                pos_x, pos_y, self.file_path.get(), self.certificate_path.get(), self.output_path.get(),
                self.selected_format.get()))
            printing_thread.start()

    def format_print(self, pos_x, pos_y, file_path, certificate_path, output_path, file_format):
        global font_path, font_size, text_color, alignment

        df = pd.read_excel(file_path)

        for i in df.iloc[:, 0].tolist():
            print("Generating certificate for: ", i)
            print_certificate(certificate_path, str(i), font_path, font_size, (pos_x, pos_y), text_color,
                              output_path,
                              alignment, file_format)

        write_config((pos_x, pos_y), file_path, certificate_path, output_path)
        self.start_button.config(text=" Open Output Folder ", command=self.open_output_folder)

    def open_output_folder(self, *_):
        os.system(f"open {self.output_path.get()}")


if __name__ == "__main__":
    with open(".config", "r") as config_file:
        configuration = config_file.read().split("\n")
    def_position, def_certificate, def_file, def_output = configuration
    AppWindow(def_position, def_certificate, def_file, def_output)
