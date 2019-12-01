from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import funciones as fun
import sqlite3
base = sqlite3.connect('base_de_datos.db')
conn = base.cursor()

# VENTANA PRINCIPAL
mainWind = Tk()
mainWind.title("La Huerta Polar")
bit = mainWind.iconbitmap('icono.ico')
mainWind.geometry('350x510')
mainWind.resizable(width=False, height=False)
mainWind.configure(background='light blue')

# IMAGEN DEL LOGO
canvas = Canvas(mainWind, width = 350, height = 115,bg="light blue")
canvas.pack()
logo = PhotoImage(file="logo.gif")
canvas.create_image(185,60, anchor=CENTER, image=logo)

# PESTAÑAS
tab_control = ttk.Notebook(mainWind)
tomarPedido = ttk.Frame(tab_control)
verPedidos = ttk.Frame(tab_control)
verPendientes = ttk.Frame(tab_control)
verProductos = ttk.Frame(tab_control)
tab_control.add(tomarPedido, text='Tomar Pedido')
tab_control.add(verPedidos, text='Pedidos Pendientes')
tab_control.add(verPendientes, text= 'Ver Clientes')
tab_control.add(verProductos, text= 'Ver Productos')
tab_control.pack(expand=1, fill='both')

# PIE DE MENÚ
foot = Label(mainWind,text="Instagram @LAHUERTAPOLAR - © github.com/ Laurajuanna")
foot.place(x=0,y=482,width=350,height=28)

# ------------------- VARIABLES -------------------------------------------

productos= fun.buscarProductos()

clientes = fun.buscarClientes()

tamanio= StringVar()

# ---------------------------- FUNCIONES ---------------------------------------

def getTamanio():
    tamanio.get()
    return tamanio

def agregarProductos():
    elegido = lstProductos.get(lstProductos.curselection())
    cant = int(cantCaja.get())
    tipo = (tamanio.get())
    try:
        esto=buscaIDprecio(elegido,tipo)
        id=esto[0]
        precio=esto[1]
        suma = (float(precio))*(float(cant))
        cadena = (elegido,'-',tipo,'x',cant,'-',(str(suma)))
        print(cadena)
        lstAdd.insert(END, cadena)
        sumaTotal= sumarAgregados()
        mostrarPrecio(suma, sumaTotal)
    except:
        messagebox.showwarning("Error","El precio de ese producto no está disponible.")

def borrarLista():
    itemEntero= lstAdd.get(lstAdd.curselection())
    indexItem = lstAdd.curselection()
    aBorrar=itemEntero[6]
    if(indexItem != ""):
        valor = sumarAgregados()
        total = float(valor)-float(aBorrar)
        mostrarPrecio(00.00, total)
        lstAdd.delete(indexItem)


def mostrarPrecio(individual,total):
    precioInd.config(text=("$",str(individual)))
    nroTotal.config(text=("$",str(total)))

def sumarAgregados():
    sumaTotal=0.0
    paraSumar=lstAdd.get(0,END)
    for x in range(len(paraSumar)):
        numero=float(paraSumar[x][6])
        sumaTotal=sumaTotal+numero
    return sumaTotal

def fechaActual(): # devuelve la fecha actual.
    dt = datetime.now()    # Fecha y hora actual
    fecha = ("{}/{}/{}".format(dt.day, dt.month, dt.year))
    return fecha



def polola():
    fecha=fechaActual()
    agregados=lstAdd.get(0, END)
    print(agregados)
    sumar=00.00
    idProductos=""
    for x in range(len(agregados)):
        elegido=agregados[x][0]
        tipo=agregados[x][2]
        cantidad=agregados[x][4]
        precio=agregados[x][6]
        getId=buscaIDprecio(elegido,tipo)
        id=getId[0]
        idProductos=idProductos+str(id)+", "
        sumar=sumar+(float(precio))
    precioTotal=sumar
    idProductos=idProductos[:-2]
    try:
        idCliente=(searchFor()[0])
        guardarPedido(idCliente,idProductos,precioTotal,fecha)
    except:
        if messagebox.showwarning("Error","El cliente no figura en la Base de datos."):
            insertNew()
            idCliente = (searchFor()[0])
            guardarPedido(idCliente, idProductos, precioTotal, fecha)


def guardarPedido(idcliente,idproductos,precio,fecha):
    if messagebox.askyesno("Confirmación","¿Desea guardar el pedido?"):
        conn.execute("INSERT INTO pedidos VALUES (?, ?, ?, ?, ?, ?)",
                     (None, idcliente, idproductos, precio, fecha, "HACER"))
        base.commit()

def buscaIDprecio(elegido,tipo):
    sentencia = ('SELECT "IDProducto","PRECIO" FROM productos WHERE NOMBRE = ? AND TIPO = ?;')
    conn.execute(sentencia, [elegido,tipo])
    busqueda = conn.fetchall()
    idProd = busqueda[0]
    base.commit()
    return idProd

def insertNew():
    nombre = clienteEntry.get()
    dire = direEntry.get()
    tel = telEntry.get()
    if messagebox.askyesno("Confirmación","¿Desea guardar un nuevo cliente?"):
        conn.execute("INSERT INTO clientes VALUES (?, ?, ?, ?)",
                     (None, nombre, dire, tel))
        base.commit()

def searchFor():
    nombre = clienteEntry.get()
    sentencia=('SELECT "IDCliente" FROM clientes WHERE NOMBRE = ?;')
    conn.execute(sentencia,[nombre])
    busqueda= conn.fetchall()
    idCliente = busqueda[0]
    base.commit()
    if not idCliente:
        insertNew()
        return idCliente
    else:
        return idCliente


def buscarAuto():
    clienteEntry.delete(0,END)
    direEntry.delete(0,END)
    telEntry.delete(0,END)
    nombb = clientesLoad.get()
    sentencia = ("SELECT NOMBRE, DIRE, TEL FROM clientes WHERE NOMBRE = ?;")
    conn.execute(sentencia, [nombb])
    busqueda = conn.fetchall()
    base.commit()
    try:
        n = busqueda[0][0]
        d = busqueda[0][1]
        t = busqueda[0][2]
        autoCliente(n,d,t)
    except:
        messagebox.showwarning("Error", "Seleccione un cliente para Autocompletar sus datos.")


def autoCliente(n,d,t):
    clienteEntry.insert(0,n)
    direEntry.insert(0,d)
    telEntry.insert(0,t)


# --------------- CONTENIDO DE PESTAÑA "TOMAR PEDIDO" --------------------------

# LABEL DE TXT PARA ELEGIR PRODUCTO
elegir = Label(tomarPedido,text="Elegir Producto")
elegir.place(x=0, y=32, width=160, height=18)

# LISTA DE PRODUCTOS A ELEGIR Y SU SCROLL
scrolProd = Scrollbar(tomarPedido, orient=VERTICAL)
lstProductos = Listbox(tomarPedido, yscrollcommand=scrolProd.set)
scrolProd.config(command=lstProductos.yview)
scrolProd.place(x=152, y=53, height=196)
lstProductos.place(x=8, y=53, width=145, height=196)
# AGREGAR PRODUCTOS
for item in productos:
    lstProductos.insert(END, item)

# TITULO DE LA PESTAÑA
titulo = Label(tomarPedido,text="TOMAR PEDIDOS",font=("bold",15))
titulo.place(x=0, y=8, width=350, height=20)

# LABEL DE TXT Y RADIOBUTTONS PARA ELEGIR EL TAMAÑO
lblTamanio = Label(tomarPedido,text="Tamaño")
lblTamanio.place(x=196,y=53,width=50,height=18)
chico = Radiobutton(tomarPedido, text='Chico', variable=tamanio, value= "Chico", command=getTamanio)
chico.place(x=180, y=74)
chico.select()
grande = Radiobutton(tomarPedido, text='Grande', variable=tamanio, value="Grande", command=getTamanio)
grande.place(x=180, y=103)
grande.deselect()

# LABEL DE CANTIDAD Y SPINBOX
cantidad = Label(tomarPedido,text="Cantidad")
cantidad.place(x=274,y=53,width=50,height=18)
cantCaja = Spinbox(tomarPedido, from_=1, to=30, width=10)
cantCaja.place(x=264, y=76)

# LABEL DE PRECIO INDIVIDUAL
precioInd = Label(tomarPedido,text="", anchor="center", fg="green", bg="white")
precioInd.place(x=264,y=105,width=75,height=20)

# BOTONES AGREGAR Y BORRAR PRODUCTO AL PEDIDO
btnAgregar = Button(tomarPedido,text="Agregar", command=agregarProductos)
btnAgregar.place(x=180, y=132, width=78)
btnBorrar = Button(tomarPedido,text="Borrar", command=borrarLista)
btnBorrar.place(x=264, y=132, width=75)

# LISTA DE PRODUCTOS AÑADIDOS Y SU SCROLLBAR
scrolPedido = Scrollbar(tomarPedido, orient=VERTICAL)
lstAdd = Listbox(tomarPedido, yscrollcommand=scrolPedido.set)
scrolPedido.config(command=lstAdd.yview)
scrolPedido.place(x=323, y=165, height=52)
lstAdd.place(x=180, y=165, width=143, height=52)

# LABEL DE TEXTO DEL PRECIO TOTAL
preTotal = Label(tomarPedido,text="TOTAL:",anchor="w",font="bold")
preTotal.place(x=180,y=226,width=53,height=20)
nroTotal = Label(tomarPedido,text="", anchor="center", fg="green",font="bold")
nroTotal.place(x=264,y=226,width=75,height=20)

# FORMULARIO DE NUEVO CLIENTE
clienteNuevo = Label(tomarPedido,text="Cliente", anchor="center")
clienteNuevo.place(x=5,y=260,height=20)
clienteEntry = Entry(tomarPedido)
clienteEntry.place(x=62,y=260,width=108)
direNuevo = Label(tomarPedido,text="Dirección", anchor="center")
direNuevo.place(x=5,y=288,height=20)
direEntry = Entry(tomarPedido)
direEntry.place(x=62,y=288,width=108)
telNuevo = Label(tomarPedido,text="Teléfono", anchor="center")
telNuevo.place(x=5,y=316,height=20)
telEntry = Entry(tomarPedido)
telEntry.place(x=62,y=316,width=108)

# OPCIONES PARA AUTOCOMPLETAR CLIENTES VIEJOS
clientesLoad = ttk.Combobox(tomarPedido, state="readonly")
clientesLoad.place(x=217,y=260, width=123)
clientesLoad['values'] = clientes
clientesLoad.current(0)  # set the selected item

# BOTON PARA AUTOCOMPLETAR CLIENTES VIEJOS
btnAuto = Button(tomarPedido,text="<",command=lambda:buscarAuto())
btnAuto.place(x=180, y=259, width=30, height=22)

# BOTON AGREGAR NUEVO CLIENTE
btnAddNew = Button(tomarPedido,text="Agregar\nCliente",command=insertNew)
btnAddNew.place(x=180, y=288, width=78, height=50)

# BOTON GUARDAR PEDIDO
btnSave = Button(tomarPedido,text="Guardar\nPedido",command=polola)
btnSave.place(x=264, y=288, width=75,height=50)


# REPRODUCIR
mainloop()