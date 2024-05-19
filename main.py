import flet as ft

from contact_manager import ContactManager


class Form(ft.UserControl):
    def __init__(self, page):
        super().__init__( expand= True)
        self.page = page
        self.data = ContactManager()
        self.selected_row = None

        self.name = ft.TextField(label= "Nombre", border_color= "purple")

        self.age = ft.TextField(label="Edad", border_color= "purple",
                                input_filter= ft.NumbersOnlyInputFilter(),
                                max_length= 2)
        self.email = ft.TextField(label= "Correo", border_color= "purple")

        self.phone = ft.TextField(label="Telefono", border_color= "purple",
                                input_filter= ft.NumbersOnlyInputFilter(),
                                max_length= 10)
        
        self.search_filed = ft.TextField(
            label= "Buscar por nombre",
            suffix_icon= ft.icons.SEARCH,
            border= ft.InputBorder.UNDERLINE,
            border_color= "white",
            label_style= ft.TextStyle(color= "white"),
            on_change = self.search_data,
        )

        self.data_table = ft.DataTable(
            expand= True,
            border= ft.border.all(2, "purple"),
            data_row_color= {ft.MaterialState.SELECTED: "purple",
                             ft.MaterialState.PRESSED: "black"},
            border_radius=10,
            show_checkbox_column= True,

            columns=[
                ft.DataColumn(ft.Text("Nombre", color="purple", weight="bold")),
                ft.DataColumn(ft.Text("Edad", color="purple", weight="bold"), numeric=True),
                ft.DataColumn(ft.Text("Correo", color="purple", weight="bold")),
                ft.DataColumn(ft.Text("Telefono", color="purple", weight="bold"), numeric=True),

            ]

        )

        self.show_data()

        self.form = ft.Container(
        bgcolor= "#222222",
        border_radius=10,
        col = 4,
        content= ft.Column(
            alignment= ft.MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Ingrese sus datos",
                        size= 40,
                        text_align= "center",
                        font_family= "vivaldi",),

                self.name,
                self.age,
                self.email,
                self.phone,
                ft.Container(
                    content= ft.Row(
                        spacing=5,
                        alignment=ft.MainAxisAlignment.CENTER, 
                        controls=[
                            ft.TextButton(text="Guardar",
                                          icon= ft.icons.SAVE,
                                          style= ft.ButtonStyle(
                                              color="white", bgcolor="purple",
                                          ),
                                          on_click= self.add_data
                                          ),
                            ft.TextButton(text="Actualizar",
                                          icon= ft.icons.UPDATE,
                                          style= ft.ButtonStyle(
                                              color= "white", bgcolor= "purple"
                                          ),
                                          on_click= self.update_data
                                          ),
                            ft.TextButton(text="Borrar",
                                          icon= ft.icons.DELETE,
                                          style= ft.ButtonStyle(
                                              color= "white", bgcolor= "purple",
                                          ),
                                          on_click= self.delete_data,
                                          ),
                        ]
                    )
                )
            ]

        )
    )
        self.table = ft.Container(
            bgcolor= "#222222",
            border_radius=10,
            col = 8,
            content= ft.Column(
                controls=[
                    ft.Container(
                        padding= 10,
                        content=ft.Row(
                            controls=[
                                self.search_filed,
                                ft.IconButton(tooltip= "Editar",
                                              icon= ft.icons.EDIT,
                                              icon_color= "white",
                                              on_click=self.edit_filed_text),

                                ft.IconButton(tooltip="Descargar en PDF",
                                              icon= ft.icons.PICTURE_AS_PDF,
                                              icon_color= "white"),

                                ft.IconButton(tooltip="Descargar en EXCEL",
                                              icon= ft.icons.SAVE_ALT,
                                              icon_color= "white"),
                            ]
                        )
                    ),
                    ft.Column(
                        expand=True,
                        scroll="auto",
                        controls=[
                            ft.ResponsiveRow([
                                self.data_table,
                            ])
                        ]
                    )
                ]
            )
        )

        self.conent = ft.ResponsiveRow(
            controls= [
                self.form,
                self.table,
            ]
        )


    def show_data(self):
        self.data_table.rows = []
        for x in self.data.get_contact():
            self.data_table.rows.append(
                ft.DataRow(
                    on_select_changed= self.get_index,
                    cells=[
                        ft.DataCell(ft.Text(x[1])),  
                        ft.DataCell(ft.Text(str(x[2]))),  
                        ft.DataCell(ft.Text(x[3])),
                        ft.DataCell(ft.Text(str(x[4]))),  
                    ]
                )
            )
        self.update()

    def add_data(self, e):
        name = self.name.value
        age = str(self.age.value)
        email = self.email.value
        phone = str(self.phone.value ) 

        if len(name) and len(age) and len(email) and len(phone)>0:
            contact_exsists = False
            for row in self.data.get_contact():
                if row[1] == name:
                    contact_exsists = True
                    break
        if not contact_exsists:
            self.clean_fileds()
            self.data.add_contact(name, age, email, phone)
            self.show_data()

    def get_index(self, e):
        if e.control.selected:
            e.control.selected = False
        else:
            e.control.selected = True

        name = e.control.cells[0].content.value
        for row in self.data.get_contact():
            if row[1] == name:
                self.selected_row = row
                break

        self.update()

    def edit_filed_text(self, e):
        try:
            self.name.value = self.selected_row[1]
            self.age.value = self.selected_row[2]
            self.email.value = self.selected_row[3]
            self.phone.value = self.selected_row[4]
            self.update()
        except TypeError:
            print("Error")

    def update_data(self, e):
        name = self.name.value
        age = str(self.age.value)
        email = self.email.value
        phone = str(self.phone.value ) 

        if len(name) and len(age) and len(email) and len(phone)>0:
            self.clean_fileds()
            self.data.update_contact(self.selected_row[0], name, age,email, phone)
            self.show_data()

    def delete_data(self, e):
        self.data.delete_contact(self.selected_row[1])
        self.show_data()

    def search_data(self, e):
        search = self.search_filed.value.lower()
        name = list(filter(lambda x: search in x[1].lower(), self.data.get_contact()))
        self.data_table.rows = []
        if not self.search_field.value == "":
            if len(name) >0:
                for x in name:
                    self.data_table.rows.append(
                        ft.DataRow(
                            on_select_changed= self.get_index,
                            cells= [
                                ft.DataCell(ft.Text(x[1])),
                                ft.DataCell(ft.Text(str(x[2]))),
                                ft.DataCell(ft.Text(x[3])),
                                ft.DataCell(ft.Text(str(x[4]))),

                            ]
                        )
                    )
                    self.update()
        else:
            self.show_data()


    def clean_fileds(self):
        self.name.value = ""
        self.age.value = ""
        self.email.value = ""
        self.phone.value = ""





    def build(self):
        return self.conent
    

def main(page: ft.page):
    page.bgcolor = "black"
    page.title = "CRUD SQLite"
    page.window_min_heigt =500
    page.window_min_width = 100

    page.add(Form(page))



ft.app(main) 