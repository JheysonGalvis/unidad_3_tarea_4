import sqlite3
from tkinter import Tk, Label, Entry, Button, Listbox, END, messagebox

# 1. Crear y conectar la base de datos
def create_database():
    conn = sqlite3.connect("municipios.db")
    cursor = conn.cursor()
    # Crear la tabla Municipios si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Municipios (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            NombreApellido TEXT NOT NULL,
            NoCelular TEXT NOT NULL,
            CargoActual TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 3. Funciones CRUD

def insertar_registro(nombre, celular, cargo):
    conn = sqlite3.connect("municipios.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Municipios (NombreApellido, NoCelular, CargoActual) VALUES (?, ?, ?)", (nombre, celular, cargo))
    conn.commit()
    conn.close()
    mostrar_registros()

def mostrar_registros():
    conn = sqlite3.connect("municipios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Municipios")
    registros = cursor.fetchall()
    conn.close()
    lista.delete(0, END)  # Limpiar la lista
    for registro in registros:
        lista.insert(END, registro)

def modificar_registro(id, nombre, celular, cargo):
    conn = sqlite3.connect("municipios.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Municipios SET NombreApellido = ?, NoCelular = ?, CargoActual = ? WHERE Id = ?", (nombre, celular, cargo, id))
    conn.commit()
    conn.close()
    mostrar_registros()

def eliminar_registro(id):
    conn = sqlite3.connect("municipios.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Municipios WHERE Id = ?", (id,))
    conn.commit()
    conn.close()
    mostrar_registros()

# Eventos de la interfaz

def agregar_registro():
    nombre = entrada_nombre.get()
    celular = entrada_celular.get()
    cargo = entrada_cargo.get()
    if nombre and celular and cargo:
        insertar_registro(nombre, celular, cargo)
        entrada_nombre.delete(0, END)
        entrada_celular.delete(0, END)
        entrada_cargo.delete(0, END)
    else:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

def seleccionar_registro(event):
    try:
        index = lista.curselection()[0]
        seleccionado = lista.get(index)
        entrada_id.delete(0, END)
        entrada_id.insert(0, seleccionado[0])
        entrada_nombre.delete(0, END)
        entrada_nombre.insert(0, seleccionado[1])
        entrada_celular.delete(0, END)
        entrada_celular.insert(0, seleccionado[2])
        entrada_cargo.delete(0, END)
        entrada_cargo.insert(0, seleccionado[3])
    except IndexError:
        pass

def actualizar_registro():
    id_ = entrada_id.get()
    nombre = entrada_nombre.get()
    celular = entrada_celular.get()
    cargo = entrada_cargo.get()
    if id_ and nombre and celular and cargo:
        modificar_registro(id_, nombre, celular, cargo)
    else:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

def borrar_registro():
    id_ = entrada_id.get()
    if id_:
        eliminar_registro(id_)
    else:
        messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar.")

# 4. Crear la interfaz gráfica

# Crear la ventana principal
root = Tk()
root.title("Gestión de Municipios")

# Crear etiquetas y entradas
Label(root, text="ID").grid(row=0, column=0)
entrada_id = Entry(root)
entrada_id.grid(row=0, column=1)
entrada_id.config(state="readonly")

Label(root, text="Nombre y Apellido").grid(row=1, column=0)
entrada_nombre = Entry(root)
entrada_nombre.grid(row=1, column=1)

Label(root, text="No. Celular").grid(row=2, column=0)
entrada_celular = Entry(root)
entrada_celular.grid(row=2, column=1)

Label(root, text="Cargo Actual").grid(row=3, column=0)
entrada_cargo = Entry(root)
entrada_cargo.grid(row=3, column=1)

# Botones
Button(root, text="Agregar", command=agregar_registro).grid(row=4, column=0)
Button(root, text="Actualizar", command=actualizar_registro).grid(row=4, column=1)
Button(root, text="Eliminar", command=borrar_registro).grid(row=5, column=0)

# Lista
lista = Listbox(root, width=50, height=10)
lista.grid(row=6, column=0, columnspan=2)
lista.bind("<Double-1>", seleccionar_registro)

# Inicializar la base de datos y mostrar registros
create_database()
mostrar_registros()

# Ejecutar el loop de la interfaz
def run():
    root.mainloop()

if __name__ == "__main__":
    run()