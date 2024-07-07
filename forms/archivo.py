# Importación de librerías
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as MessageBox
from tkinter import filedialog

# Importación de módulos
from models import tratamientoArchivos as ta
from persistance.persistance import registros_session
from models.models import Registro

class Archivo:
    def __init__(self, root, login_app):
        self.root = root
        self.login_app = login_app
        self.root.title("Archivo")
        
        self.archivo_seleccionado = None
        self.df = None
        self.filas_seleccionadas = []

        # Crear la interfaz del dashboard
        label = tk.Label(self.root, text="Registros", font=("Arial", 24))
        label.pack(padx=10, pady=10)
        seleccionar_button = ttk.Button(self.root, text="Seleccionar Archivo", command=self.seleccionar_archivo)
        seleccionar_button.pack(padx=10, pady=10)
        cargar_button = ttk.Button(self.root, text="Cargar Archivo", command=self.cargar_archivo)
        cargar_button.pack(padx=10, pady=10)
        self.tree = ttk.Treeview(self.root, columns=("Nombre", "Apellido", "Nombre Materia", "Nota"), show='headings', selectmode='extended')
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Nombre Materia", text="Nombre Materia")
        self.tree.heading("Nota", text="Nota")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        guardar_button = ttk.Button(self.root, text="Guardar Selección", command=self.guardar_seleccion)
        guardar_button.pack(padx=10, pady=10)
        ver_registros_button = ttk.Button(self.root, text="Ver Registros Guardados", command=self.ver_registros_guardados)
        ver_registros_button.pack(padx=10, pady=10)
        logout_button = ttk.Button(self.root, text="Cerrar Sesión", command=self.logout)
        logout_button.pack(padx=10, pady=10)

    def seleccionar_archivo(self):
        self.archivo_seleccionado = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=(("Archivos PDF", "*.pdf"), ("Archivos Excel", "*.xlsx"), ("Archivos CSV", "*.csv"))
        )
        if self.archivo_seleccionado:
            MessageBox.showinfo("Archivo seleccionado", f"Has seleccionado el archivo: {self.archivo_seleccionado}")

    def cargar_archivo(self):
        if not self.archivo_seleccionado:
            MessageBox.showwarning("Advertencia", "Primero selecciona un archivo.")
        else:
            MessageBox.showinfo("Cargar archivo", f"Cargando archivo: {self.archivo_seleccionado}")
            self.mostrar_contenido_archivo()

    def mostrar_contenido_archivo(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            if self.archivo_seleccionado.endswith('.pdf'):
                texto = ta.extraer_datos_pdf(self.archivo_seleccionado)
                if texto:
                    self.df = ta.crear_dataframe(texto)
            elif self.archivo_seleccionado.endswith('.xlsx'):
                self.df = ta.extraer_datos_xlsx(self.archivo_seleccionado)
            elif self.archivo_seleccionado.endswith('.csv'):
                self.df = ta.extraer_datos_csv(self.archivo_seleccionado)

            if self.df is not None:
                for index, row in self.df.iterrows():
                    self.tree.insert("", tk.END, values=(row["Nombre"], row["Apellido"], row["Nombre Materia"], row["Nota"]))
        except Exception as e:
            MessageBox.showerror("Error", f"Ocurrió un error al cargar el archivo: {e}")

    def guardar_seleccion(self):
        selected_items = self.tree.selection()
        self.filas_seleccionadas = []
        for item in selected_items:
            row_values = self.tree.item(item, "values")
            self.filas_seleccionadas.append(row_values)
        
        self.guardar_en_bd()
        MessageBox.showinfo("Guardar Selección", f"Se han guardado {len(self.filas_seleccionadas)} filas seleccionadas.")

    def guardar_en_bd(self):
        for row in self.filas_seleccionadas:
            registro = Registro(nombre=row[0], apellido=row[1], nombre_materia=row[2], nota=row[3])
            registros_session.add(registro)
        registros_session.commit()

    def ver_registros_guardados(self):
        registros_ventana = tk.Toplevel(self.root)
        registros_ventana.title("Registros Guardados")

        tree = ttk.Treeview(registros_ventana, columns=("Nombre", "Apellido", "Nombre Materia", "Nota"), show='headings')
        tree.heading("Nombre", text="Nombre")
        tree.heading("Apellido", text="Apellido")
        tree.heading("Nombre Materia", text="Nombre Materia")
        tree.heading("Nota", text="Nota")
        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        registros = registros_session.query(Registro).all()
        for registro in registros:
            tree.insert("", tk.END, values=(registro.nombre, registro.apellido, registro.nombre_materia, registro.nota))

    def logout(self):
        self.root.destroy()
        self.login_app.clear_fields()
        self.login_app.root.deiconify()

        
    