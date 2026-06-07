import flet as ft
import os
import asyncio
from eliminador_fondos import BackgroundRemover


class BackgroundRemoverApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.directory_path = None
        self.filename_list = []
        self.selected_files = []
        self._setup_page()
        self._create_components()
        self._build_ui()

    def _setup_page(self):
        # -----------------------------------------------------------------
        # CONFIGURACIÓN DE LA PANTALLA (Ventana de la aplicación)
        # -----------------------------------------------------------------
        # El título que se muestra en la barra superior.
        self.page.title = "Background Remover Pro"
        # Color de fondo oscuro y moderno (código hexadecimal).
        self.page.bgcolor = "#1a1a2e"

        # Ajustamos el tamaño a uno estándar.
        self.page.window.height = 800
        self.page.window.width = 800

        # Forzamos a que la interfaz use el tema oscuro.
        self.page.theme_mode = ft.ThemeMode.DARK

    def _create_components(self):
        # El FilePicker es el servicio que permite seleccionar archivos en el sistema.
        self.file_picker = ft.FilePicker()
        self.page.services.append(self.file_picker)

        self.default_folder_check = ft.Checkbox(
            label="Usar carpeta por defecto",
            value=False,
            on_change=self._checkbox_changed,
            check_color="#e94560",
            label_style=ft.TextStyle(color="#a0a0a0", size=14)
        )

        self.output_folder_textfield = ft.TextField(
            label="Carpeta de Salida Personalizada",
            autofocus=False,
            bgcolor="#16213e",
            color="#ffffff",
            border_color="#0f3460",
            focused_border_color="#e94560",
            width=350,
            height=60,
            border_radius=10,
            content_padding=ft.Padding.all(15)
        )

        self.btn_pick_files = ft.Button(
            content=ft.Row([
                ft.Icon(ft.Icons.CLOUD_UPLOAD, color="#ffffff"),
                ft.Text("Seleccionar Imágenes", color="#ffffff",
                        weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER),
            on_click=self.btn_pick_files_click,
            bgcolor="#0f3460",
            color="#ffffff",
            width=250,
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                elevation=5,
            ),
        )

        self.select_files_info = ft.Text(
            "Ningún Archivo Seleccionado",         # Texto inicial.
            color="#a0a0a0",                       # Color gris suave.
            size=14,                               # Tamaño de letra.
        )

        self.btn_extract = ft.Button(
            content=ft.Row([
                ft.Icon(ft.Icons.AUTO_FIX_HIGH, color="#ffffff"),
                ft.Text("Remover Fondo", color="#ffffff", size=16,
                        weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER),
            on_click=self.btn_extract_click,
            disabled=True,                         # Inicia deshabilitado porque no hay archivos seleccionados.
            bgcolor="#e94560",
            color="#ffffff",
            width=300,
            height=60,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=15),
                elevation=8
            )
        )

    def _build_ui(self):
        config_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.SETTINGS, color="#e94560", size=20),
                    ft.Text("Configuración", weight=ft.FontWeight.BOLD,
                            color="#ffffff", size=18)
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=10),
                self.default_folder_check,
                ft.Container(height=10),
                self.output_folder_textfield,
            ], spacing=5),
            bgcolor="#16213e",
            padding=ft.Padding.all(20),
            border_radius=15,
            border=ft.Border.all(1, "#0f3460"),
            width=600
        )

        files_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.IMAGE, color="#e94560", size=20),
                    ft.Text("Imágenes Seleccionadas", weight=ft.FontWeight.BOLD,
                            color="#ffffff", size=18)
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=15),
                ft.Row([
                    self.btn_pick_files,
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=10),
                self.select_files_info,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#16213e",
            padding=ft.Padding.all(20),
            border_radius=15,
            border=ft.Border.all(1, "#0f3460"),
            width=600
        )

        process_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PSYCHOLOGY, color="#e94560", size=20),
                    ft.Text("Procesamiento", weight=ft.FontWeight.BOLD,
                            color="#ffffff", size=18)
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=20),
                self.btn_extract,
                ft.Container(height=15),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#16213e",
            padding=ft.Padding.all(20),
            border_radius=15,
            border=ft.Border.all(1, "#0f3460"),
            width=600
        )

        self.page.add(config_card)
        self.page.add(files_card)
        self.page.add(process_card)

        # Finalmente, actualizamos la página completa para asegurarnos de que todo
        # se dibuje de forma perfecta en la ventana al iniciar.
        self.page.update()

    def _checkbox_changed(self, e: ft.ControlEvent):
        self.output_folder_textfield.disabled = e.control.value
        self.output_folder_textfield.bgcolor = "#2a2a40" if e.control.value else "#16213e"
        self.page.update()

    async def btn_pick_files_click(self, e):
        """
        Esta función abre el explorador de archivos y procesa lo que el usuario elija.
        """
        files = await self.file_picker.pick_files(
            allow_multiple=True,
            allowed_extensions=["png", "jpg", "jpeg", "bmp", "webp"]
        )

        if files:
            self.selected_files = files
            file_count = len(files)
            first_file_path = files[0].path
            directory = os.path.dirname(first_file_path)

            self.select_files_info.value = f" {file_count} Archivo(s) seleccionado(s)\n Carpeta: {directory}"
            self.select_files_info.color = "#148609"
            self.btn_extract.disabled = False  # Habilitamos el botón al tener imágenes
        else:
            self.selected_files = []
            self.select_files_info.value = "Selección Cancelada"
            self.select_files_info.color = "#f44336"
            self.btn_extract.disabled = True   # Lo deshabilitamos si no hay selección

        self.page.update()

    async def btn_extract_click(self, e):
        """
        Esta función ejecuta la eliminación de fondo de las imágenes seleccionadas
        utilizando la clase BackgroundRemover en un hilo de fondo.
        """
        if not self.selected_files:
            return

        # Deshabilitamos los controles durante el procesamiento para evitar doble clics o cambios
        self.btn_extract.disabled = True
        self.btn_pick_files.disabled = True
        self.default_folder_check.disabled = True
        self.output_folder_textfield.disabled = True
        self.select_files_info.value = "Iniciando procesamiento de imágenes..."
        self.select_files_info.color = "#ffb703"  # Color de procesamiento
        self.page.update()

        remover = BackgroundRemover("", "")
        total_files = len(self.selected_files)
        success_count = 0
        output_dir = ""

        for i, file in enumerate(self.selected_files):
            file_path = file.path
            self.select_files_info.value = f"Procesando imagen {i+1} de {total_files}...\nArchivo: {os.path.basename(file_path)}"
            self.page.update()

            # Determinar carpeta de salida
            if self.default_folder_check.value:
                output_dir = os.path.dirname(file_path)
            else:
                output_dir = self.output_folder_textfield.value.strip()
                if not output_dir:
                    output_dir = os.path.dirname(file_path)

            # Asegurar que exista la carpeta
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as ex:
                self.select_files_info.value = f"Error al crear carpeta destino: {str(ex)}"
                self.select_files_info.color = "#f44336"
                break

            # Crear ruta del archivo final
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_file_path = os.path.join(output_dir, f"{base_name}_sinfondo.png")

            try:
                # Corremos la eliminación en un hilo secundario para no congelar la UI de Flet
                await asyncio.to_thread(remover.remove_background, file_path, output_file_path)
                success_count += 1
            except Exception as ex:
                print(f"Error procesando {file_path}: {ex}")

        # Restauramos controles
        self.btn_pick_files.disabled = False
        self.default_folder_check.disabled = False
        self.output_folder_textfield.disabled = self.default_folder_check.value

        if success_count == total_files:
            self.select_files_info.value = f"¡Completado con éxito! {success_count} de {total_files} procesados.\nDestino: {output_dir}"
            self.select_files_info.color = "#148609"
        else:
            self.select_files_info.value = f"Proceso finalizado. {success_count} de {total_files} procesados con éxito."
            self.select_files_info.color = "#ffb703"

        # Limpiamos la selección y dejamos el botón deshabilitado
        self.selected_files = []
        self.btn_extract.disabled = True
        self.page.update()


async def main(page: ft.Page):
    obj = BackgroundRemoverApp(page)


if __name__ == "__main__":
    ft.run(main)
