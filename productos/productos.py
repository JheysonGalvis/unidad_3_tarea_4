import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def create_database():
    # Conexión a la base de datos y creación de la tabla
    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            NombresApellidos TEXT NOT NULL,
            NoCelular TEXT NOT NULL,
            CargoActual TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_record():
    # Inserta un registro en la base de datos
    nombres_apellidos = entry_nombres.get()
    no_celular = entry_celular.get()
    cargo_actual = entry_cargo.get()

    if nombres_apellidos and no_celular and cargo_actual:
        conn = sqlite3.connect("productos.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (NombresApellidos, NoCelular, CargoActual) VALUES (?, ?, ?)",
                       (nombres_apellidos, no_celular, cargo_actual))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Registro insertado correctamente.")
        clear_entries()
        refresh_table()
    else:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

def fetch_records():
    # Obtiene todos los registros de la base de datos
    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    records = cursor.fetchall()
    conn.close()
    return records

def refresh_table():
    # Actualiza la tabla en la GUI
    for row in table.get_children():
        table.delete(row)
    for record in fetch_records():
        table.insert("", tk.END, values=record)

def clear_entries():
    # Limpia los campos de entrada
    entry_nombres.delete(0, tk.END)
    entry_celular.delete(0, tk.END)
    entry_cargo.delete(0, tk.END)

def delete_record():
    # Elimina el registro seleccionado
    selected_item = table.selection()
    if selected_item:
        record_id = table.item(selected_item)['values'][0]
        conn = sqlite3.connect("productos.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE Id = ?", (record_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
        refresh_table()
    else:
        messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar.")

def update_record():
    # Actualiza el registro seleccionado
    selected_item = table.selection()
    if selected_item:
        record_id = table.item(selected_item)['values'][0]
        nombres_apellidos = entry_nombres.get()
        no_celular = entry_celular.get()
        cargo_actual = entry_cargo.get()

        if nombres_apellidos and no_celular and cargo_actual:
            conn = sqlite3.connect("productos.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE productos SET NombresApellidos = ?, NoCelular = ?, CargoActual = ? WHERE Id = ?
            """, (nombres_apellidos, no_celular, cargo_actual, record_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
            clear_entries()
            refresh_table()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
    else:
        messagebox.showwarning("Advertencia", "Seleccione un registro para actualizar.")

# Crear base de datos y tabla al iniciar
create_database()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestión de Productos")
root.geometry("700x500")

# Etiquetas y entradas
frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Nombres y Apellidos:").grid(row=0, column=0, padx=5, pady=5)
entry_nombres = tk.Entry(frame_form, width=30)
entry_nombres.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="No. Celular:").grid(row=1, column=0, padx=5, pady=5)
entry_celular = tk.Entry(frame_form, width=30)
entry_celular.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Cargo Actual:").grid(row=2, column=0, padx=5, pady=5)
entry_cargo = tk.Entry(frame_form, width=30)
entry_cargo.grid(row=2, column=1, padx=5, pady=5)

# Botones
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Insertar", command=insert_record).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Actualizar", command=update_record).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Eliminar", command=delete_record).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Limpiar", command=clear_entries).grid(row=0, column=3, padx=5)

# Tabla
frame_table = tk.Frame(root)
frame_table.pack(pady=10)

columns = ("Id", "NombresApellidos", "NoCelular", "CargoActual")
table = ttk.Treeview(frame_table, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150)

table.pack()
refresh_table()

root.mainloop()
