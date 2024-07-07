# Importación de librerías
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as MessageBox
import time

# Importación de librerías
from persistance.persistance import user_session
from models.models import Usuario as UsuarioModel
from forms.validador import es_password_debil, es_password_valido
from forms.archivo import Archivo

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as MessageBox

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login usuario")

        self.nombreUsuario = tk.StringVar()
        self.passwordUsuario = tk.StringVar()
        self.intentos_fallidos = 0

        self.create_gui()

    def create_gui(self):
        mainFrame = tk.Frame(self.root)
        mainFrame.pack()
        mainFrame.config(width=480, height=320)

        titulo = tk.Label(mainFrame, text="Inicio de sesión", font=("Arial", 24))
        titulo.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        subtitulo1 = tk.Label(mainFrame, text="Trabajo Práctico", font=("Arial", 16))
        subtitulo1.grid(column=0, row=1, padx=10, pady=5, columnspan=2)

        subtitulo2 = tk.Label(mainFrame, text="Diseño de sistemas 1", font=("Arial", 16))
        subtitulo2.grid(column=0, row=2, padx=10, pady=5, columnspan=2)

        nombreLabel = tk.Label(mainFrame, text="Nombre: ")
        nombreLabel.grid(column=0, row=3, pady=10)
        passwordLabel = tk.Label(mainFrame, text="Contraseña: ")
        passwordLabel.grid(column=0, row=4, pady=10)

        nombreEntry = tk.Entry(mainFrame, textvariable=self.nombreUsuario)
        nombreEntry.grid(column=1, row=3, pady=10)

        passwordEntry = tk.Entry(mainFrame, textvariable=self.passwordUsuario, show="*")
        passwordEntry.grid(column=1, row=4, pady=10)

        iniciarSesionButton = ttk.Button(mainFrame, text="Iniciar Sesión", command=self.iniciar_sesion)
        iniciarSesionButton.grid(column=1, row=5, ipadx=5, ipady=5, padx=10, pady=10)

        registrarButton = ttk.Button(mainFrame, text="Registrar", command=self.registrar_usuario)
        registrarButton.grid(column=0, row=5, ipadx=5, ipady=5, padx=10, pady=10)

    def iniciar_sesion(self):
        user = user_session.query(UsuarioModel).filter_by(nombre=self.nombreUsuario.get()).first()
        if user and user.password == self.passwordUsuario.get():
            MessageBox.showinfo("Conectado", f"Se inició sesión en [{user.nombre}] con éxito.")
            self.intentos_fallidos = 0
            self.open_archivo()
        else:
            self.intentos_fallidos += 1
            MessageBox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")
            print(f"Tiempo de espera: {self.intentos_fallidos * 2} segundos")
            time.sleep(self.intentos_fallidos * 2)

    def registrar_usuario(self):
        name = self.nombreUsuario.get()
        password = self.passwordUsuario.get()

        if es_password_debil(password):
            MessageBox.showerror("Error", "La contraseña es demasiado débil. Elija otra.")
            return

        if not es_password_valido(password):
            MessageBox.showerror("Error", "La contraseña debe tener al menos 8 caracteres, incluir letras mayúsculas, minúsculas, números y caracteres especiales.")
            return

        if user_session.query(UsuarioModel).filter_by(nombre=name).first():
            MessageBox.showerror("Error", "El nombre de usuario ya existe. Elija otro.")
            return

        nuevoUsuario = UsuarioModel(nombre=name, password=password)
        user_session.add(nuevoUsuario)
        user_session.commit()
        MessageBox.showinfo("Registro exitoso", f"Se registró el usuario [{name}] con éxito.")
        self.nombreUsuario.set("")
        self.passwordUsuario.set("")

    def open_archivo(self):
        self.root.withdraw()
        archivo = tk.Toplevel(self.root)
        Archivo(archivo, self)

    def clear_fields(self):
        self.nombreUsuario.set("")
        self.passwordUsuario.set("")
