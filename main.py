import flet as ft


def main(page: ft.Page):
    page.title = "Background Remover Pro"
    page.bgcolor = "#1a1a2e"
    page.window.height = 1080
    page.window.width = 1920
    page.theme_mode = ft.ThemeMode.DARK
    page.update
    page.add(
        ft.Text("Hola adrentro", color="white")
    )
    btn_simple = ft.ElevatedButton(
        text="Seleccionar Imagen"
    )


ft.app(target=main)
