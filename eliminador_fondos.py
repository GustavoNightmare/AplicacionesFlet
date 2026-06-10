from pathlib import Path
from rembg import remove


class BackgroundRemover:

    Supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp')

    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def process_images(self, filename_list, process_callback=None):
        pass

    def _is_supported_image(self, filename: str):
        filename.lower().endswith(self.Supported_extensions)
        return

    def _remove_background(self, input_path, output_path):
        try:
            input_image = Path(input_path)
            output_image = Path(output_path)

            if not self._is_supported_image(input_image.name):
                print(f"Archivo no soportado: {input_image.name}")
                return

            output_image.parent.mkdir(parents=True, exist_ok=True)

            with input_image.open('rb') as input_file:
                input_data = input_file.read()
                output_data = remove(input_data)

            with output_image.open('wb') as output_file:
                output_file.write(output_data)

            print(
                f"Fondo eliminado: {input_image.name} -> {output_image.name}")
        except Exception as e:
            print(f"Error procesando {input_path}: {e}")

    def _move_original(self, input_path):
        try:
            input_image = Path(input_path)
            if not self._is_supported_image(input_image.name):
                print(f"Archivo no soportado para mover: {input_image.name}")
                return

            trash_folder = self.input_folder / 'trash'
            trash_folder.mkdir(parents=True, exist_ok=True)

            destination = trash_folder / input_image.name
            input_image.rename(destination)
            print(
                f"Archivo movido a la papelera: {input_image.name} -> {destination}")
        except Exception as e:
            print(f"Error moviendo {input_path}: {e}")
