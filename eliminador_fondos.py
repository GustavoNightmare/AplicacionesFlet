from pathlib import Path
from rembg import remove


class BackgroundRemover:

    Supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp')

    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder
