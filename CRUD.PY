# Importar Bibliotecas
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Desarrollo de la Interfaz Gráfica
root=Tk()                                           # Creando la ventana con tkinder
root.title("Aplicación CRUD con Base de Datos")     # Nombre de la aplicación "Aplicación CRUD con Base de Datos"
root.geometry("600x350")                            # Las dimensiones de la aplicación

# Definiendo Variables (todas son tipo string)
miId=StringVar()            # Inicializa en 1 y sube +1
miNombre=StringVar()        # Nombre del empleado
miCargo=StringVar()         # Cargo del empleado
miSalario=StringVar()       # Salario del empleado

def conexionBBDD():                         # Hacer conexión con la base de datos o crear una base de datos
    miConexion=sqlite3.connect("base")
    miCursor=miConexion.cursor()

    try:
        miCursor.execute('''
            CREATE TABLE empleado (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE VARCHAR(50) NOT NULL,
            CARGO VARCHAR(50) NOT NULL,
            SALARIO INT NOT NULL)
        ''')
        messagebox.showinfo("CONEXIÓN","Base de Datos Creada exitosamente")
    except:
        messagebox.showinfo("CONEXIÓN", "Conexión exitosa con la base de datos")

def eliminarBBDD():                         # Eliminar toda la base de datos
    miConexion=sqlite3.connect("base")
    miCursor=miConexion.cursor()
    if messagebox.askyesno(message="¿Los datos se perderán definitivamente, Desea continuar?", title="ADVERTENCIA"):
        miCursor.execute("DROP TABLE empleado")
    else:
        pass
    limpiarCampos()
    mostrar()

def salirAplicacion():                      # Para salir de la aplicación
    valor=messagebox.askquestion("Salir","¿Está seguro que desea salir de la Aplicación?")
    if valor=="yes":
        root.destroy()

def limpiarCampos():                        # Para limpiar todos los campos pero sin borrar el registro de la base de datos
    miId.set("")
    miNombre.set("")
    miCargo.set("")
    miSalario.set("")

def mensaje():                              # Info de la aplicación
    acerca='''
    Aplicación CRUD
    Versión 1.0
    Tecnología Python Tkinter
    Creado Por Cristian Larios
    '''
    messagebox.showinfo(title='INFORMACIÓN', message=acerca)

############################ Métodos CRUD ####################

def crear():                                # Crear un nuevo registro
    miConexion=sqlite3.connect("base")
    miCursor=miConexion.cursor()
    try:
        datos=miNombre.get(),miCargo.get(),miSalario.get()
        miCursor.execute("INSERT INTO empleado VALUES(NULL,?,?,?)", (datos))
        miConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrió un error al crear el registro, verifique conexión con BBDD")
        pass
    limpiarCampos()
    mostrar()

def mostrar():                              # Para mostrar todos los registros
    miConexion=sqlite3.connect("base")
    miCursor=miConexion.cursor()
    registros=tree.get_children()
    for elemento in registros:
        tree.delete(elemento)
    
    try:
        miCursor.execute("SELECT * FROM empleado")
        for row in miCursor:
            tree.insert("",0,text=row[0], values=(row[1],row[2],row[3]))
    except:
        pass

######################### Tabla ###########################################################
tree=ttk.Treeview(height=10, columns=('#0','#1','#2'))              # Creando columnas vacías
tree.place(x=0,y=130)                                               # Posición de columnas vacías
tree.column('#0',width=100)                                         # Posición de columna 1
tree.heading('#0', text="ID", anchor=CENTER)                        # Nombre de la columna 1 y su anchura
tree.heading('#1', text="Nombre del Empleado", anchor=CENTER)       # Nombre de la columna 2 y su posición
tree.heading('#2', text="Cargo", anchor=CENTER)                     # Nombre de .a columna 3 y su posición
tree.column('#3', width=100)                                        # Anchura de la columna 4
tree.heading('#3', text="Salario", anchor=CENTER)                   # Nombre y posición de la columna 4

def seleccionarUsandoClick(event):          # Para desplegar la información de todos los campos de el registro dando dos clicks
    item=tree.identify('item',event.x,event.y)
    miId.set(tree.item(item,"text"))
    miNombre.set(tree.item(item,"values")[0])
    miCargo.set(tree.item(item,"values")[1])
    miSalario.set(tree.item(item,"values")[2])

tree.bind("<Double-1>", seleccionarUsandoClick)     # Llamar a la función seleccionarUsandoClick para que se active

def actualizar():                           # Para modificar los campos de un registro
    miConexion=sqlite3.connect("base")
    miCursor=miConexion.cursor()
    try:
        datos=miNombre.get(),miCargo.get(),miSalario.get()
        miCursor.execute("UPDATE empleado SET NOMBRE=?, CARGO=?, SALARIO=? WHERE ID="+miId.get(), (datos))
        miConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrió un error al actualizar el registro")
        pass
    limpiarCampos()
    mostrar()

def borrar():                               # Para borrar un registro
    miConexion=sqlite3.connect("base")
    miCursor=miConexion.cursor()    
    try:
        if messagebox.askyesno(message="¿Realmente desea eliminar el registro?", title="ADVETENCIA"):
            miCursor.execute("DELETE FROM empleado WHERE ID="+miId.get())
            miConexion.commit()
    except:
        messagebox.showwarning("ADVETENCIA", "Ocurrió un error al tratar de eliminar el registro")
        pass    
    limpiarCampos()
    mostrar()

########################## Colocar widgets en la VISTA (ventana)############################
################ Creando los menús #######################
menubar=Menu(root)      # Crear un menú
menubasedat=Menu(menubar, tearoff=0)    # Crear la barra del menú (Inicio)
menubasedat.add_command(label="Crear/Conectar Base de Datos", command=conexionBBDD)     # Crear opción de (Crear/Conectar a la Base de Datos )para que se muestre en el menú Inicio
menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)           # Crear opción de ( Eliminar Base de Datos )para que se muestre en el menú Inicio
menubasedat.add_command(label="Salir", command=salirAplicacion)                         # Crear opción de ( Salir ) para que se muestre en el menú Inicio
menubar.add_cascade(label="Inicio",menu=menubasedat)                                    # Crear una cascada que se llame (Inicio) como nombre del menú Inicio

ayudamenu=Menu(menubar,tearoff=0)           # Crear la barra del menú (Ayuda)
ayudamenu.add_command(label="Resetear Campos", command=limpiarCampos)       # Crear la opción de ( Resetear Campos ) para que se muestre en el menú de Ayuda
ayudamenu.add_command(label="Acerca", command=mensaje)                      # Crear la opción de ( Acerca ) para que se muestre en el menú de Ayuda
menubasedat.add_cascade(label="Ayuda",menu=ayudamenu)                       # Crear una cascada que se llame (Ayuda) como nombre del menú Ayuda

######################Creando etiquetas y cajas de texto ####################
e1=Entry(root, textvariable=miId)                   # Crear el cuadro de texto de la columna ID

l2=Label(root, text="Nombre")                       # Crear el cuadro de texto de la columna Nombre
l2.place(x=50,y=10)                                 # Lugar donde se generará
e2=Entry(root, textvariable=miNombre, width=50)     # Crear el cuadro de introducción de valores a la columna Nombre
e2.place(x=101, y=10)                               # Lugar donde se generará

l3=Label(root, text="Cargo")                        # Crear cuadro de texto de la columna Cargo
l3.place(x=50,y=40)                                 # Lugar donde se generará
e3=Entry(root, textvariable=miCargo)                # Crear cuadro de introducción de valores a la columna Cargo
e3.place(x=100, y=40)                               # Lugar donde se generará

l4=Label(root, text="Salario")                      # Crear cuadro de texto e la columna Salario
l4.place(x=292,y=40)                                # Lugar donde se generará
e4=Entry(root, textvariable=miSalario, width=10)    # Crear cuadro de introduccción de valores a la columna Salario
e4.place(x=340, y=40)                               # Lugar donde se generará

l5=Label(root, text="USD")                          # Crear cuadro de texto de USD
l5.place(x=440,y=40)                                # Lugar donde se generará

################ Creando botones #######################

b1=Button(root, text="Crear Registro", command=crear)       #Crear el botón de Crear Registro que llama a la función de crear()
b1.place(x=8,y=90)                                          # Lugar donde se generará
b2=Button(root, text="Modificar Registro", command=actualizar)      # Crear el botón de Modificar Registro que llama a la función de actualizar()
b2.place(x=130,y=90)                                                # Lugar donde se generará
b3=Button(root, text="Mostrar lista empleados", command=mostrar)        # Crear el botón de Mostrar lista empleados que llama a la función de mostrar()
b3.place(x=276,y=90)                                                    # Lugar donde se generará
b4=Button(root, text="Eliminar Registro",bg="red", command=borrar)      # Crear el botón de Eliminar Registro que llama a la fucnión de borrar()
b4.place(x=455,y=90)                                                    # Lugar donde se generará

root.config(menu=menubar)                               # Configura a la ventana como un menú


root.mainloop()                                 # Mostra a la aplicación en una ventana