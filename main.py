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
    with open(".config", "w") as config_file:
        config_file.write(str(position[0])+","+str(position[1])+"\n")
        config_file.write(certificate_path+"\n")
        config_file.write(file_path+"\n")
        config_file.write(output_path)


def format_print(pos_x, pos_y, file_path, certificate_path, output_path, file_fromat, start_button):
    global font_path, font_size, text_color, alignment
    df = pd.read_excel(file_path)
    for i in df.iloc[:, 0].tolist():
        print("Generating certificate for: ", i)
        print_certificate(certificate_path, str(i), font_path, font_size, (pos_x, pos_y), text_color, output_path,
                          alignment, file_fromat)
    write_config((pos_x, pos_y), file_path, certificate_path, output_path)
    start_button.config(text=" Done ")


def app_window(default_position, default_certificate, default_file, default_output):
    def check_args():
        try:
            pos_x, pos_y = position.get().split(",")
            pos_x, pos_y = int(pos_x), int(pos_y)
        except ValueError as ve:
            messagebox.showerror("Value Error", "Position should be in the formate: \nint,int")
            return
        if not os.path.isfile(certificate_path.get()):
            messagebox.showerror("Path Error", "Certificate path is invalid.")
            return
        elif not os.path.isfile(file_path.get()):
            messagebox.showerror("Path Error", "Input File path is invalid.")
            return
        elif not os.path.isdir(output_path.get()):
            messagebox.showerror("Path Error", "Output path is invalid.")
            return

        else:
            start_button.config(text=" Generating ", command="")
            printing_thread = threading.Thread(target=format_print, args=(
                pos_x, pos_y, file_path.get(), certificate_path.get(), output_path.get(), selected_format.get(),
                start_button))
            printing_thread.start()

    def ask_for_file_path():
        usr_def_path = filedialog.askopenfilename(title="Select a file")
        if usr_def_path:
            file_path.set(usr_def_path)

    def ask_for_certificate_path():
        usr_def_path = filedialog.askopenfilename(title="Select a file")
        if usr_def_path:
            certificate_path.set(usr_def_path)

    def ask_for_output_path():
        usr_def_path = filedialog.askdirectory(title="Select a file")
        if usr_def_path:
            output_path.set(usr_def_path)

    root = tk.Tk()
    root.title("Certificate Generator")

    position = tk.StringVar()
    position.set(default_position)

    certificate_path = tk.StringVar()
    certificate_path.set(default_certificate)

    file_path = tk.StringVar()
    file_path.set(default_file)

    output_path = tk.StringVar()
    output_path.set(default_output)

    title_frame = tk.Frame(root)
    title_frame.pack(pady=10)

    options = ["PDF", "PNG", "JPEG"]
    selected_format = tk.StringVar()
    selected_format.set(options[0])

    tk.Label(title_frame, text="Certificate Generator", font=("Arial Bold", 20)).pack()

    frame_1 = tk.Frame(root)
    frame_1.pack(pady=10)

    tk.Label(frame_1, text="Certificate Path: ").grid(column=0, row=0)
    certificate_path_new = tk.Entry(frame_1, textvariable=certificate_path)
    certificate_path_new.grid(column=1, row=0)
    tk.Button(frame_1, text="Browse", command=ask_for_certificate_path).grid(column=2, row=0)

    tk.Label(frame_1, text="File Path: ").grid(column=0, row=1)
    file_path_new = tk.Entry(frame_1, textvariable=file_path)
    file_path_new.grid(column=1, row=1)
    tk.Button(frame_1, text="Browse", command=ask_for_file_path).grid(column=2, row=1)

    tk.Label(frame_1, text="Text position: ").grid(column=0, row=2)
    position_new = tk.Entry(frame_1, textvariable=position)
    position_new.grid(column=1, row=2)

    tk.Label(frame_1, text="Output Path: ").grid(column=0, row=3)
    output_path_new = tk.Entry(frame_1, textvariable=output_path)
    output_path_new.grid(column=1, row=3)
    tk.Button(frame_1, text="Browse", command=ask_for_output_path).grid(column=2, row=3)

    tk.Label(frame_1, text="Output Formate: ").grid(column=0, row=4)
    dropdown = tk.OptionMenu(frame_1, selected_format, *options)
    dropdown.grid(column=1, row=4)

    start_button = tk.Button(root, text=" Generate ", width=20, command=check_args)
    start_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    with open(".config", "r") as config_file:
        configuration = config_file.read().split("\n")
    default_position, default_certificate, default_file, default_output = configuration
    app_window(default_position, default_certificate, default_file, default_output)
