import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def connect_to_db():
    """Establishes a connection to the database and creates the Pacientes table."""
    conn = sqlite3.connect("pacientes.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pacientes (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            NombresApellidos TEXT NOT NULL,
            NoCelular TEXT NOT NULL,
            CargoActual TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_record():
    """Inserts a new record into the Pacientes table."""
    nombres = entry_name.get()
    celular = entry_phone.get()
    cargo = entry_position.get()

    if not nombres or not celular or not cargo:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    conn = sqlite3.connect("pacientes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Pacientes (NombresApellidos, NoCelular, CargoActual) VALUES (?, ?, ?)",
                   (nombres, celular, cargo))
    conn.commit()
    conn.close()

    messagebox.showinfo("Éxito", "Registro insertado correctamente.")
    clear_entries()
    fetch_records()

def fetch_records():
    """Fetches all records from the Pacientes table and displays them in the treeview."""
    conn = sqlite3.connect("pacientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pacientes")
    rows = cursor.fetchall()
    conn.close()

    for row in tree.get_children():
        tree.delete(row)

    for row in rows:
        tree.insert("", tk.END, values=row)

def delete_record():
    """Deletes the selected record from the Pacientes table."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Seleccione un registro para eliminar.")
        return

    record_id = tree.item(selected_item, "values")[0]
    conn = sqlite3.connect("pacientes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Pacientes WHERE Id = ?", (record_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
    fetch_records()

def update_record():
    """Updates the selected record in the Pacientes table."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Seleccione un registro para actualizar.")
        return

    record_id = tree.item(selected_item, "values")[0]
    nombres = entry_name.get()
    celular = entry_phone.get()
    cargo = entry_position.get()

    if not nombres or not celular or not cargo:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    conn = sqlite3.connect("pacientes.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Pacientes SET NombresApellidos = ?, NoCelular = ?, CargoActual = ? WHERE Id = ?", 
                   (nombres, celular, cargo, record_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
    clear_entries()
    fetch_records()

def clear_entries():
    """Clears the input fields."""
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_position.delete(0, tk.END)

# Initialize the database
connect_to_db()

# Create the main window
root = tk.Tk()
root.title("Gestión de Pacientes")
root.geometry("600x400")

# Input fields
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Nombres y Apellidos:").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_inputs)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="No. Celular:").grid(row=1, column=0, padx=5, pady=5)
entry_phone = tk.Entry(frame_inputs)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Cargo Actual:").grid(row=2, column=0, padx=5, pady=5)
entry_position = tk.Entry(frame_inputs)
entry_position.grid(row=2, column=1, padx=5, pady=5)

# Buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Insertar", command=insert_record).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Actualizar", command=update_record).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Eliminar", command=delete_record).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Limpiar", command=clear_entries).grid(row=0, column=3, padx=5)

# Treeview for displaying records
tree = ttk.Treeview(root, columns=("Id", "Nombres y Apellidos", "No. Celular", "Cargo Actual"), show="headings")
tree.heading("Id", text="Id")
tree.heading("Nombres y Apellidos", text="Nombres y Apellidos")
tree.heading("No. Celular", text="No. Celular")
tree.heading("Cargo Actual", text="Cargo Actual")
tree.column("Id", width=50, anchor=tk.CENTER)
tree.pack(pady=10, fill=tk.X)

fetch_records()

# Run the main loop
root.mainloop()