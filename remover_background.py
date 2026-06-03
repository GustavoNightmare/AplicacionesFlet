import flet as ft
import os


class BackgroundRemoverApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.directory_path = None
        self.filename_list = []
        self._setup_page()
        self._create_components()

    def _setup_page(self):

        # -----------------------------------------------------------------
        # CONFIGURACIÓN DE LA PANTALLA (Ventana de la aplicación)
        # -----------------------------------------------------------------
        # El título que se muestra en la barra superior.
        self.page.title = "Background Remover Pro"
        # Color de fondo oscuro y moderno (código hexadecimal).
        self.page.bgcolor = "#1a1a2e"

        # Ajustamos el tamaño a uno estándar. Si usamos 1920x1080, la ventana se
        # saldrá de la pantalla en muchas laptops. 800x600 es perfecto para empezar.
        # Alto de la ventana en píxeles.
        self.page.window.height = 800
        # Ancho de la ventana en píxeles.
        self.page.window.width = 800

        # Forzamos a que la interfaz use el tema oscuro.
        self.page.theme_mode = ft.ThemeMode.DARK

    def _create_components(self):

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
            # Conectado a la función asíncrona
            on_click=lambda _: print("Extract button clicked"),
            disabled=False,
            bgcolor="#e94560",
            color="#ffffff",
            width=300,
            height=60,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=15),
                elevation=8
            )
        )

        self.page.services.append(self.file_picker)

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
                    ft.Text("Configuración", weight=ft.FontWeight.BOLD,
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
                    ft.Text("Configuración", weight=ft.FontWeight.BOLD,
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
