import flet as ft



def main(page: ft.Page):
    page.title = "Background Remover Pro"
    page.bgcolor = "#1a1a2e"
    page.window.height = 1080
    page.window.width = 1920
    page.theme_mode = ft.ThemeMode.DARK

    select_files_info = ft.Text(
        "Ningun Archivo Seleccionado",
        color="#a0a0a0",
        size = 14 ,


    )
    page.add(select_files_info)



    btn_profesional = ft.ElevatedButton(
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
