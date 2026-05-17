from pathlib import Path
from rembg import remove


class BackgroundRemover:

    Supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp')

    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def remove_background(self, input_folder, output_folder):
        with open(input_folder, 'rb') as inp, open(output_folder, 'wb') as out:
            output = remove(inp.read())
            out.write(output)
        # Aquí iría la lógica para eliminar el fondo de la imagen
        # Esto es solo un ejemplo y no una implementación real
        print("El fondo ha sido eliminado de la imagen.")


eliminador = BackgroundRemover(
    'ruta/a/carpeta/entrada', 'ruta/a/carpeta/salida')
eliminador.remove_background(
    "E:\ProyectosVisualStudio\AplicacionesFlet\Trespiés.jpg", "trespies_sinfondo.png")
