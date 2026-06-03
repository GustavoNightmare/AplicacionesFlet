import flet as ft
import os
import asyncio
from eliminador_fondos import BackgroundRemover

# =====================================================================
# ¿QUÉ ES UNA FUNCIÓN ASÍNCRONA (async)?
# En Python y Flet, una función asíncrona ("async def") permite realizar
# tareas que toman tiempo (como abrir un selector de archivos y esperar
# a que el usuario elija algo) sin congelar la interfaz de la aplicación.
# Permite que otros procesos sigan funcionando en segundo plano.
# =====================================================================


async def main(page: ft.Page):
    """
    Esta es la función principal de tu aplicación de Flet.

    'page' (de tipo ft.Page) representa la ventana del navegador o de
    escritorio donde dibujaremos todos nuestros botones, textos e imágenes.
    """

    # -----------------------------------------------------------------
    # CONFIGURACIÓN DE LA PANTALLA (Ventana de la aplicación)
    # -----------------------------------------------------------------
    # El título que se muestra en la barra superior.
    page.title = "Background Remover Pro"
    # Color de fondo oscuro y moderno (código hexadecimal).
    page.bgcolor = "#1a1a2e"

    # Ajustamos el tamaño a uno estándar. Si usamos 1920x1080, la ventana se
    # saldrá de la pantalla en muchas laptops. 800x600 es perfecto para empezar.
    # Alto de la ventana en píxeles.
    page.window.height = 800
    # Ancho de la ventana en píxeles.
    page.window.width = 800

    # Forzamos a que la interfaz use el tema oscuro.
    page.theme_mode = ft.ThemeMode.DARK

    selected_files = []

    output_folder_textfield = ft.TextField(
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

    def _checkbox_changed(e: ft.ControlEvent):
        output_folder_textfield.disabled = e.control.value
        output_folder_textfield.bgcolor = "#2a2a40" if e.control.value else "#16213e"
        page.update()

    default_folder_check = ft.Checkbox(
        label="Usar carpeta por defecto",
        value=False,
        on_change=_checkbox_changed,
        check_color="#e94560",
        label_style=ft.TextStyle(color="#a0a0a0", size=14)
    )
    # -----------------------------------------------------------------
    # ELEMENTOS VISUALES 1: TEXTO INFORMATIVO (ft.Text)
    # -----------------------------------------------------------------
    # Creamos un bloque de texto que usaremos para mostrar información sobre
    # los archivos que el usuario seleccione.
    select_files_info = ft.Text(
        "Ningún Archivo Seleccionado",         # Texto inicial.
        color="#a0a0a0",                       # Color gris suave.
        size=14,                               # Tamaño de letra.
    )

    # -----------------------------------------------------------------
    # FUNCIONES DE CONTROL Y EVENTOS
    # -----------------------------------------------------------------
    async def btn_pick_files_click(e):
        """
        Esta función abre el explorador de archivos y procesa lo que el usuario elija.
        """
        nonlocal selected_files
        # ABRIMOS EL DIÁLOGO:
        files = await file_picker.pick_files(
            allow_multiple=True,
            allowed_extensions=["png", "jpg", "jpeg", "bmp", "webp"]
        )

        if files:
            selected_files = files
            file_count = len(files)
            first_file_path = files[0].path
            directory = os.path.dirname(first_file_path)

            select_files_info.value = f" {file_count} Archivo(s) seleccionado(s)\n Carpeta: {directory}"
            select_files_info.color = "#148609"
            btn_extract.disabled = False  # Habilitamos el botón al tener imágenes
        else:
            selected_files = []
            select_files_info.value = "Selección Cancelada"
            select_files_info.color = "#f44336"
            btn_extract.disabled = True   # Lo deshabilitamos si no hay selección

        page.update()

    async def btn_extract_click(e):
        """
        Esta función ejecuta la eliminación de fondo de las imágenes seleccionadas
        utilizando la clase BackgroundRemover en un hilo de fondo.
        """
        nonlocal selected_files
        if not selected_files:
            return

        # Deshabilitamos los controles durante el procesamiento para evitar doble clics o cambios
        btn_extract.disabled = True
        btn_pick_files.disabled = True
        default_folder_check.disabled = True
        output_folder_textfield.disabled = True
        select_files_info.value = "Iniciando procesamiento de imágenes..."
        select_files_info.color = "#ffb703"  # Color de procesamiento
        page.update()

        remover = BackgroundRemover("", "")
        total_files = len(selected_files)
        success_count = 0
        output_dir = ""

        for i, file in enumerate(selected_files):
            file_path = file.path
            select_files_info.value = f"Procesando imagen {i+1} de {total_files}...\nArchivo: {os.path.basename(file_path)}"
            page.update()

            # Determinar carpeta de salida
            if default_folder_check.value:
                output_dir = os.path.dirname(file_path)
            else:
                output_dir = output_folder_textfield.value.strip()
                if not output_dir:
                    output_dir = os.path.dirname(file_path)

            # Asegurar que exista la carpeta
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as ex:
                select_files_info.value = f"Error al crear carpeta destino: {str(ex)}"
                select_files_info.color = "#f44336"
                break

            # Crear ruta del archivo final
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_file_path = os.path.join(
                output_dir, f"{base_name}_sinfondo.png")

            try:
                # Corremos la eliminación en un hilo secundario para no congelar la UI de Flet
                await asyncio.to_thread(remover.remove_background, file_path, output_file_path)
                success_count += 1
            except Exception as ex:
                print(f"Error procesando {file_path}: {ex}")

        # Restauramos controles
        btn_pick_files.disabled = False
        default_folder_check.disabled = False
        output_folder_textfield.disabled = default_folder_check.value

        if success_count == total_files:
            select_files_info.value = f"¡Completado con éxito! {success_count} de {total_files} procesados.\nDestino: {output_dir}"
            select_files_info.color = "#148609"
        else:
            select_files_info.value = f"Proceso finalizado. {success_count} de {total_files} procesados con éxito."
            select_files_info.color = "#ffb703"

        # Limpiamos la selección y dejamos el botón deshabilitado
        selected_files = []
        btn_extract.disabled = True
        page.update()

    # -----------------------------------------------------------------
    # ELEMENTOS VISUALES: BOTONES E INTERFAZ
    # -----------------------------------------------------------------
    btn_extract = ft.Button(
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

    # El FilePicker es la herramienta nativa que abre la ventana del sistema
    # operativo para buscar archivos.
    file_picker = ft.FilePicker()

    # Como el FilePicker no es un control visual sino un servicio del sistema en
    # Flet moderno (v0.80+), debemos agregarlo a 'page.services' en lugar de 'page.overlay'.
    page.services.append(file_picker)

    btn_pick_files = ft.Button(
        content=ft.Row([
            ft.Icon(ft.Icons.CLOUD_UPLOAD, color="#ffffff"),
            ft.Text("Seleccionar Imágenes", color="#ffffff",
                    weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.CENTER),
        on_click=btn_pick_files_click,
        bgcolor="#0f3460",
        color="#ffffff",
        width=250,
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            elevation=5,
        ),
    )
    config_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.SETTINGS, color="#e94560", size=20),
                ft.Text("Configuración", weight=ft.FontWeight.BOLD,
                        color="#ffffff", size=18)
            ], alignment=ft.MainAxisAlignment.START),
            ft.Container(height=10),
            default_folder_check,
            ft.Container(height=10),
            output_folder_textfield,
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
                btn_pick_files,
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=10),
            select_files_info,
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
            btn_extract,
            ft.Container(height=15),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#16213e",
        padding=ft.Padding.all(20),
        border_radius=15,
        border=ft.Border.all(1, "#0f3460"),
        width=600
    )

    # -----------------------------------------------------------------
    # CONSTRUCCIÓN DE LA INTERFAZ: Agregar elementos a la pantalla
    # -----------------------------------------------------------------
    # Usamos page.add() para "dibujar" nuestros elementos en el lienzo.
    # El orden en que los agregues define cómo se verán de arriba a abajo.
    # Primero el checkbox para usar carpeta por defecto.
    page.add(config_card)

    page.add(files_card)     # Debajo de este colocamos el botón.
    # Finalmente, el botón de extracción (inicialmente deshabilitado).
    page.add(process_card)  # Información sobre los archivos seleccionados

    # Finalmente, actualizamos la página completa para asegurarnos de que todo
    # se dibuje de forma perfecta en la ventana al iniciar.
    page.update()


# =====================================================================
# PUNTO DE ENTRADA: Ejecutar la aplicación
# =====================================================================
# ft.run() le dice a Flet que inicie el ciclo de vida de la aplicación
# utilizando nuestra función 'main' como el punto de inicio.
ft.run(main)
