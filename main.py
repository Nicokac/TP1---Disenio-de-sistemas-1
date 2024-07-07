import tkinter as tk
from forms.login import LoginApp
from persistance.persistance import Base, user_engine, registros_engine

# Crear las tablas en las bases de datos
Base.metadata.create_all(user_engine)
Base.metadata.create_all(registros_engine)

if __name__ == "__main__":
    main_window = tk.Tk()
    app = LoginApp(main_window)
    main_window.mainloop()











