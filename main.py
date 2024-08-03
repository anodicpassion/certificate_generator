from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
import os

def add_text_to_image(image_path, text, font_path, font_size, position, text_color, output_path, alignment='left'):
    """
    Add custom text to an image with specified alignment.

    Parameters:
    - image_path (str): The path to the input image.
    - text (str): The text to be added to the image.
    - font_path (str): The path to the .ttf font file.
    - font_size (int): The size of the font.
    - position (tuple): The (x, y) position where the text will be placed.
    - text_color (tuple): The color of the text in RGB format, e.g., (255, 255, 255) for white.
    - output_path (str): The path to save the output image.
    - alignment (str): The alignment of the text. Options are 'left', 'center', 'right'.
    """
    # Open the image
    image = Image.open(image_path)

    # Initialize ImageDraw
    draw = ImageDraw.Draw(image)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text width and height
    text_width, text_height = draw.textsize(text, font=font)

    # Adjust position based on alignment
    if alignment == 'center':
        position = (position[0] - text_width // 2, position[1])
    elif alignment == 'right':
        position = (position[0] - text_width, position[1])

    # Add text to image
    draw.text(position, text, fill=text_color, font=font)

    # Save the image
    image.save(output_path)


# Example usage
image_path = 'demo_certificate.jpg'
text = 'Deepali Pawar'
font_path = 'GreatVibes-Regular.ttf'
font_size = 110
position = (1000, 660)
text_color = "#283361"
output_path = 'output_image.jpg'
alignment = 'center'


# add_text_to_image(image_path, text, font_path, font_size, position, text_color, output_path, alignment)


class CertificateGenerator:
    def __init__(self, default_position, default_certificate, default_file, default_output):
        self.root = tk.Tk()
        self.root.title = "Certificate Generator"
        self.root.geometry("500x300")
        self.place_frames()
        (self.default_position, self.default_certificate, self.default_file,
         self.default_output) = default_position, default_certificate, default_file, default_output
        self.root.mainloop()

    def place_frames(self):
        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Certificate Generator", font=("Arial", 15)).pack()
        frame_1 = tk.Frame(self.root)
        frame_1.pack(pady=10)
        tk.Label(frame_1, text="Certificate Path: ").grid(column=0, row=0)
        certificate_path = tk.Entry(frame_1)
        certificate_path.grid(column=1, row=0)
        tk.Button(frame_1, text="Browse").grid(column=2, row=0)

        tk.Label(frame_1, text="File Path: ").grid(column=0, row=1)
        file_path = tk.Entry(frame_1)
        file_path.grid(column=1, row=1)
        tk.Button(frame_1, text="Browse").grid(column=2, row=1)

        tk.Label(frame_1, text="Text position: ").grid(column=0, row=2)
        position_path = tk.Entry(frame_1)
        position_path.grid(column=1, row=2)

        tk.Label(frame_1, text="Output Path: ").grid(column=0, row=3)
        output_path = tk.Entry(frame_1)
        output_path.grid(column=1, row=3)
        tk.Button(frame_1, text="Browse").grid(column=2, row=3)



if __name__ == "__main__":
    default_position, default_certificate, default_file, default_output = "", "", "", ""
    with open(".config", "r") as config_file:
        configuration = config_file.read().split("\n")

    # if len(configuration):

    CertificateGenerator(default_position, default_certificate, default_file, default_output)
