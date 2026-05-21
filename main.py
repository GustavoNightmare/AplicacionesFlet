import flet as ft


def main(page: ft.Page):
    page.title = "Background Remover Pro"
    page.bgcolor = "#1a1a2e"
    page.window.height = 1080
    page.window.width = 1920
    page.theme_mode = ft.ThemeMode.DARK

    btn_simple = ft.Button(
        content=ft.Text("Seleccionar Imagenes"),
        on_click=lambda p: print("Boton presionado")
    )
    page.add(btn_simple)
    page.update
    page.add(
        ft.Text("Hola adrentro", color="white")
    )

    btn_con_estilo = ft.Button(
        content=ft.Text("Seleccionar Imagenes"),
        bgcolor="#0f3460",
        color="#ffffff",
        width=250,
        height=50,
    )
    page.add(btn_con_estilo)

    btn_profesional = ft.Button(
        content=ft.Row([
            ft.Icon(ft.Icons.CLOUD_UPLOAD, color="#ffffff"),
            ft.Text("Seleccionar Imagenes", color="#ffffff",
                    weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.CENTER),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            elevation=5,
        ),
        bgcolor="#0f3460",
        color="#ffffff",
        width=250,
        height=50,
    )
    page.add(btn_profesional)


ft.run(main)
