import flet as ft
import os

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
    page.window.height = 600                   # Alto de la ventana en píxeles.
    # Ancho de la ventana en píxeles.
    page.window.width = 800

    # Forzamos a que la interfaz use el tema oscuro.
    page.theme_mode = ft.ThemeMode.DARK

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
    # ELEMENTOS NO VISUALES: SELECTOR DE ARCHIVOS (ft.FilePicker)
    # -----------------------------------------------------------------
    # El FilePicker es la herramienta nativa que abre la ventana del sistema
    # operativo para buscar archivos.
    file_picker = ft.FilePicker()

    # Como el FilePicker no es un control visual sino un servicio del sistema en
    # Flet moderno (v0.80+), debemos agregarlo a 'page.services' en lugar de 'page.overlay'.
    # Si usamos overlay, Flet no lo reconocerá y dará el error: "Unknown control: FilePicker".
    page.services.append(file_picker)

    # -----------------------------------------------------------------
    # FUNCIONES DE CONTROL: ¿Qué pasa cuando hacemos clic?
    # -----------------------------------------------------------------
    # Definimos la función que se ejecutará cuando el usuario presione el botón.
    # Usamos 'async' porque usaremos 'await' adentro.
    async def btn_pick_files_click(e):
        """
        Esta función abre el explorador de archivos y procesa lo que el usuario elija.
        """
        # ABRIMOS EL DIÁLOGO:
        # Usamos 'await' para decirle a Python: "Pausa esta función aquí y espera
        # a que el usuario termine de elegir sus archivos en la ventana emergente".
        files = await file_picker.pick_files(
            # Permite seleccionar varias imágenes a la vez.
            allow_multiple=True,
            # Solo permite estos formatos.
            allowed_extensions=["png", "jpg", "jpeg", "bmp", "webp"]
        )

        # PROCESAMOS EL RESULTADO:
        # Si la lista de archivos no está vacía (el usuario no canceló la selección):
        if files:
            # Contamos cuántos archivos seleccionó.
            file_count = len(files)
            # Obtenemos la ruta completa de la primera imagen.
            first_file_path = files[0].path
            # Extraemos la carpeta contenedora.
            directory = os.path.dirname(first_file_path)

            # Actualizamos el texto informativo con un color verde éxito (#acaf50)
            select_files_info.value = f" {file_count} Archivo(s) seleccionado(s)\n Carpeta: {directory}"
            select_files_info.color = "#148609"
        else:
            # Si el usuario cerró la ventana o canceló la selección:
            select_files_info.value = "Selección Cancelada"
            select_files_info.color = "#f44336"  # Color rojo error (#f44336)

        # Actualizamos la pantalla para que los cambios en 'select_files_info' se visualicen de inmediato.
        page.update()

    # -----------------------------------------------------------------
    # ELEMENTOS VISUALES 2: EL BOTÓN DE ACCIÓN (ft.Button)
    # -----------------------------------------------------------------
    # Creamos el botón interactivo. Usamos 'ft.Button' ya que 'ElevatedButton'
    # está obsoleto en las últimas versiones de Flet.
    btn_pick_files = ft.Button(
        # 'content' define lo que hay dentro del botón.
        # Colocamos un 'ft.Row' (una fila horizontal) para tener un ícono y un texto juntos.
        content=ft.Row([
            # Ícono de una nube con flecha arriba.
            ft.Icon(ft.Icons.CLOUD_UPLOAD, color="#ffffff"),
            # Texto en negrita.
            ft.Text("Seleccionar Imágenes", color="#ffffff",
                    weight=ft.FontWeight.BOLD)
            # Centramos el contenido dentro del botón.
        ], alignment=ft.MainAxisAlignment.CENTER),

        # VINCULACIÓN DEL EVENTO:
        # Al hacer clic ('on_click'), llamamos a nuestra función asíncrona de arriba.
        on_click=btn_pick_files_click,

        # ESTILIZACIÓN DEL BOTÓN:
        bgcolor="#0f3460",       # Color de fondo azul oscuro elegante.
        color="#ffffff",         # Color del texto/ícono.
        width=250,               # Ancho del botón.
        height=50,               # Alto del botón.
        style=ft.ButtonStyle(
            # Bordes redondeados modernos.
            shape=ft.RoundedRectangleBorder(radius=12),
            # Efecto de sombra para darle profundidad.
            elevation=5,
        ),
    )

    # -----------------------------------------------------------------
    # CONSTRUCCIÓN DE LA INTERFAZ: Agregar elementos a la pantalla
    # -----------------------------------------------------------------
    # Usamos page.add() para "dibujar" nuestros elementos en el lienzo.
    # El orden en que los agregues define cómo se verán de arriba a abajo.
    page.add(select_files_info)  # Primero mostramos el texto informativo.
    page.add(btn_pick_files)     # Debajo de este colocamos el botón.

    # Finalmente, actualizamos la página completa para asegurarnos de que todo
    # se dibuje de forma perfecta en la ventana al iniciar.
    page.update()


# =====================================================================
# PUNTO DE ENTRADA: Ejecutar la aplicación
# =====================================================================
# ft.run() le dice a Flet que inicie el ciclo de vida de la aplicación
# utilizando nuestra función 'main' como el punto de inicio.
ft.run(main)
