import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Paso 1: Crear la base de datos y la tabla "Empleados"
def create_database():
    connection = sqlite3.connect("empleados.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Empleados (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            NombresApellidos TEXT NOT NULL,
            NoCelular TEXT NOT NULL,
            CargoActual TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

# Paso 2: Funciones para interactuar con la base de datos

def insert_employee(nombre_apellido, no_celular, cargo):
    connection = sqlite3.connect("empleados.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Empleados (NombresApellidos, NoCelular, CargoActual) VALUES (?, ?, ?)", 
                   (nombre_apellido, no_celular, cargo))
    connection.commit()
    connection.close()


def get_all_employees():
    connection = sqlite3.connect("empleados.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Empleados")
    records = cursor.fetchall()
    connection.close()
    return records


def update_employee(emp_id, nombre_apellido, no_celular, cargo):
    connection = sqlite3.connect("empleados.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE Empleados SET NombresApellidos = ?, NoCelular = ?, CargoActual = ? WHERE Id = ?", 
                   (nombre_apellido, no_celular, cargo, emp_id))
    connection.commit()
    connection.close()


def delete_employee(emp_id):
    connection = sqlite3.connect("empleados.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Empleados WHERE Id = ?", (emp_id,))
    connection.commit()
    connection.close()

# Paso 3: Crear la interfaz gráfica

def app():
    # Crear ventana principal
    root = tk.Tk()
    root.title("Gestión de Empleados")

    # Variables para los campos
    nombre_apellido_var = tk.StringVar()
    no_celular_var = tk.StringVar()
    cargo_var = tk.StringVar()

    # Función para recargar la tabla
    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        for row in get_all_employees():
            tree.insert("", "end", values=row)

    # Función para agregar un empleado
    def add_employee():
        nombre_apellido = nombre_apellido_var.get()
        no_celular = no_celular_var.get()
        cargo = cargo_var.get()

        if not nombre_apellido or not no_celular or not cargo:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        insert_employee(nombre_apellido, no_celular, cargo)
        messagebox.showinfo("Éxito", "Empleado agregado correctamente")
        refresh_table()

    # Función para eliminar un empleado
    def remove_employee():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor selecciona un empleado para eliminar")
            return

        emp_id = tree.item(selected_item[0], "values")[0]
        delete_employee(emp_id)
        messagebox.showinfo("Éxito", "Empleado eliminado correctamente")
        refresh_table()

    # Función para actualizar un empleado
    def edit_employee():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor selecciona un empleado para editar")
            return

        emp_id = tree.item(selected_item[0], "values")[0]
        nombre_apellido = nombre_apellido_var.get()
        no_celular = no_celular_var.get()
        cargo = cargo_var.get()

        if not nombre_apellido or not no_celular or not cargo:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        update_employee(emp_id, nombre_apellido, no_celular, cargo)
        messagebox.showinfo("Éxito", "Empleado actualizado correctamente")
        refresh_table()

    # Etiquetas y campos de entrada
    tk.Label(root, text="Nombres y Apellidos").grid(row=0, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=nombre_apellido_var).grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="No. Celular").grid(row=1, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=no_celular_var).grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Cargo Actual").grid(row=2, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=cargo_var).grid(row=2, column=1, padx=10, pady=5)

    # Botones
    tk.Button(root, text="Agregar", command=add_employee).grid(row=3, column=0, padx=10, pady=5)
    tk.Button(root, text="Eliminar", command=remove_employee).grid(row=3, column=1, padx=10, pady=5)
    tk.Button(root, text="Editar", command=edit_employee).grid(row=3, column=2, padx=10, pady=5)

    # Tabla para mostrar los datos
    tree = ttk.Treeview(root, columns=("Id", "NombresApellidos", "NoCelular", "CargoActual"), show="headings")
    tree.heading("Id", text="ID")
    tree.heading("NombresApellidos", text="Nombres y Apellidos")
    tree.heading("NoCelular", text="No. Celular")
    tree.heading("CargoActual", text="Cargo Actual")
    tree.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

    refresh_table()

    root.mainloop()

# Crear base de datos y lanzar aplicación
if __name__ == "__main__":
    create_database()
    app()