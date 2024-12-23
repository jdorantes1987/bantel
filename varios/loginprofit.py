# Importamos las librerías necesarias
import tkinter as tk
from tkinter import messagebox, ttk

from autentic import aut_user

name_app = "DataProfit"
# Creamos la ventana principal
window = tk.Tk()
window.title("Login")
window.geometry("300x250")

# Creamos los widgets para el ID, el usuario y la contraseña
user_label = tk.Label(window, text="Usuario:")
user_label.pack()
user_entry = tk.Entry(window)
user_entry.pack()
pass_label = tk.Label(window, text="Contraseña:")
pass_label.pack()
pass_entry = tk.Entry(window, show="*")
pass_entry.pack()


def mostrar_main():
    # Abrimos la ventana principal de la aplicación
    main_window = tk.Tk()
    main_window.title(name_app)
    # main_window.geometry("400x300")
    main_window.state("zoomed")
    # Iniciamos el bucle principal de la ventana
    main_window.mainloop()


def men_bienv(user):
    # Mostramos un mensaje de bienvenida
    tk.messagebox.showinfo(f"Login - {name_app}", message=f"Bienvenido {user}")


def men_error():
    # Mostramos un mensaje de error
    tk.messagebox.showerror(
        f"Login - {name_app}", message="Usuario o contraseña incorrectos"
    )


def login():
    # Obtenemos el usuario y la contraseña de los campos de entrada
    user = user_entry.get()
    password = pass_entry.get()
    # Verificamos si el usuario y la contraseña son válidos
    data_autentificacion = aut_user(user, password)
    is_valid = data_autentificacion["idlogin"].count() > 0
    # Si el resultado es válido, cerramos la ventana actual y abrimos la principal
    if is_valid:
        men_bienv(data_autentificacion["nombre"].iloc[0])
        window.destroy()
        mostrar_main()
    # Si el resultado no es válido, mostramos un mensaje de error y vaciamos los campos de entrada
    else:
        men_error()
        # user_entry.delete(0, tk.END)
        # user_entry.insert(0, "")
        pass_entry.delete(0, tk.END)
        pass_entry.insert(0, "")


# Creamos un botón para iniciar sesión
login_button = tk.Button(window, text="Iniciar sesión", command=login)
login_button.pack()
window.mainloop()
