import sqlite3
from tkinter import Tk, Label, Entry, Button, ttk, messagebox

# Crear y configurar la base de datos
def setup_database():
    connection = sqlite3.connect("estudiantes.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Estudiantes (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            NombresApellidos TEXT NOT NULL,
            NoCelular TEXT NOT NULL,
            CargoActual TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

# Funciones para la gestión de la base de datos
def insertar_registro():
    nombres = entry_nombres.get()
    celular = entry_celular.get()
    cargo = entry_cargo.get()

    if not (nombres and celular and cargo):
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    connection = sqlite3.connect("estudiantes.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Estudiantes (NombresApellidos, NoCelular, CargoActual) VALUES (?, ?, ?)",
                   (nombres, celular, cargo))
    connection.commit()
    connection.close()
    messagebox.showinfo("Éxito", "Registro insertado correctamente")
    mostrar_registros()
    limpiar_campos()

def mostrar_registros():
    for row in tree.get_children():
        tree.delete(row)

    connection = sqlite3.connect("estudiantes.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Estudiantes")
    records = cursor.fetchall()
    connection.close()

    for record in records:
        tree.insert("", "end", values=record)

def eliminar_registro():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Seleccione un registro para eliminar")
        return

    record_id = tree.item(selected_item, "values")[0]

    connection = sqlite3.connect("estudiantes.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Estudiantes WHERE Id = ?", (record_id,))
    connection.commit()
    connection.close()

    messagebox.showinfo("Éxito", "Registro eliminado correctamente")
    mostrar_registros()

def actualizar_registro():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Seleccione un registro para actualizar")
        return

    record_id = tree.item(selected_item, "values")[0]
    nombres = entry_nombres.get()
    celular = entry_celular.get()
    cargo = entry_cargo.get()

    if not (nombres and celular and cargo):
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    connection = sqlite3.connect("estudiantes.db")
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Estudiantes
        SET NombresApellidos = ?, NoCelular = ?, CargoActual = ?
        WHERE Id = ?
    """, (nombres, celular, cargo, record_id))
    connection.commit()
    connection.close()

    messagebox.showinfo("Éxito", "Registro actualizado correctamente")
    mostrar_registros()
    limpiar_campos()

def limpiar_campos():
    entry_nombres.delete(0, "end")
    entry_celular.delete(0, "end")
    entry_cargo.delete(0, "end")

# Interfaz gráfica
setup_database()
root = Tk()
root.title("Gestión de Estudiantes")

Label(root, text="Nombres y Apellidos:").grid(row=0, column=0, padx=10, pady=5)
entry_nombres = Entry(root, width=30)
entry_nombres.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="No. Celular:").grid(row=1, column=0, padx=10, pady=5)
entry_celular = Entry(root, width=30)
entry_celular.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Cargo Actual:").grid(row=2, column=0, padx=10, pady=5)
entry_cargo = Entry(root, width=30)
entry_cargo.grid(row=2, column=1, padx=10, pady=5)

Button(root, text="Insertar", command=insertar_registro).grid(row=3, column=0, padx=10, pady=5)
Button(root, text="Actualizar", command=actualizar_registro).grid(row=3, column=1, padx=10, pady=5)
Button(root, text="Eliminar", command=eliminar_registro).grid(row=4, column=0, padx=10, pady=5)
Button(root, text="Limpiar", command=limpiar_campos).grid(row=4, column=1, padx=10, pady=5)

# Tabla para mostrar los registros
tree = ttk.Treeview(root, columns=("Id", "NombresApellidos", "NoCelular", "CargoActual"), show="headings")

for col in ("Id", "NombresApellidos", "NoCelular", "CargoActual"):
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

mostrar_registros()
root.mainloop()