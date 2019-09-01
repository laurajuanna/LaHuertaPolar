from datetime import datetime
import sqlite3
base = sqlite3.connect('huertapolar.db')
conn = base.cursor()

conn.execute('''CREATE TABLE if not exists productos
	 (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	  NOMBRE TEXT NOT NULL,
	  TIPO TEXT NOT NULL,
	  PRECIO FLOAT NOT NULL );''')

conn.execute('''CREATE TABLE if not exists pedidos
	 (IDCliente INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	  Cliente TEXT NOT NULL,
	  Direccion TEXT NOT NULL,
	  Telefono INTEGER NOT NULL,
	  IDPedido TEXT NOT NULL,
	  Precio FLOAT NOT NULL,
	  Fecha INTEGER NOT NULL,
	  Estado TEXT NOT NULL );''')

conn.execute('''CREATE TABLE if not exists encargados
	 (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	  IDCliente INTEGER NOT NULL,
	  PRODUCTO TEXT NOT NULL,
	  TIPO TEXT NOT NULL,
	  IDProducto INTEGER NOT NULL,
	  Estado TEXT NOT NULL,
	  FOREIGN KEY (IDCliente) REFERENCES pedidos(IDCliente),
	  FOREIGN KEY (IDProducto) REFERENCES productos(ID),
	  FOREIGN KEY (PRODUCTO) REFERENCES productos(NOMBRE),
	  FOREIGN KEY (Tipo) REFERENCES productos(TIPO) );''')

def ingresarEnProducto(nombre, tipo, precio):
	conn.execute("INSERT INTO productos VALUES (?, ?, ?, ?)",
                  (None, nombre, tipo, precio))
	base.commit()


def ingresarProducto():
    while True:
        nombre= input("Ingrese el nombre del producto: ")
        tipo= input("Ingrese el tipo: ")
        precio= input("Ingrese el precio: ")
        ingresarEnProducto(nombre, tipo, precio)
        dec=input("Desea continuar?\nPresione Enter para continuar, 1 para Terminar.")
        if dec == "1":
            return False

def fechaActual(): # devuelve la fecha actual.
    dt = datetime.now()    # Fecha y hora actual
    fecha = ("{}/{}/{}".format(dt.day, dt.month, dt.year))
    return fecha

def buscarProducto(idProducto):
    sentencia = ('SELECT "NOMBRE" FROM productos WHERE ID = ?;')
    conn.execute(sentencia, [idProducto])
    busqueda = conn.fetchall()
    producto = busqueda[0][0]
    base.commit()
    return producto

def buscarIdCliente(cliente):
    sentencia = ('SELECT "IDCliente" FROM pedidos WHERE Cliente = ?;')
    conn.execute(sentencia, [cliente])
    busqueda = conn.fetchall()
    idCliente = busqueda[0][0]
    base.commit()
    return idCliente

def buscarIdPedidos(idCliente):
    sentencia = ('SELECT "IDProducto" FROM encargados WHERE IDCliente = ?;')
    conn.execute(sentencia, [idCliente])
    busqueda = conn.fetchall()
    idPedido = busqueda
    base.commit()
    return idPedido


def getPrecio(id):
	sentencia=("SELECT precio FROM productos WHERE ID = ?;")
	conn.execute(sentencia, [id])
	busqueda=conn.fetchall()
	precio= busqueda[0][0]
	base.commit()
	return precio


def precioTotal(idPedido):
    listaPrecio=[]
    suma=0
    for id in range(len(idPedido)):
        id=idPedido[id][0]
        precio=getPrecio(id)
        listaPrecio.append(precio)
    for nro in range(len(listaPrecio)):
        precio = listaPrecio[nro]
        suma = suma+precio
    return suma


def ingresarPedidos():
    cliente= input("Nombre del Cliente: ")
    direccion= input("Dirección: ")
    telefono= input("Teléfono: ")
    idPedido=""
    precio =""
    estado="Hacer"
    fecha=fechaActual()
    conn.execute("INSERT INTO pedidos VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                 (None, cliente, direccion, telefono, idPedido, precio, fecha, estado))
    base.commit()
    idCliente=buscarIdCliente(cliente)
    return idCliente


def ingresarEncargue(idCliente):
    print("\nMENÚ:\n-1 Brócoli\n-2 Calabaza\n-3 Acelga\n"
          "-4 Espinaca\n-5 Chaucha\n-6 Zapallito\n-7 Zanahoria\n-8 Cebolla\n-9 Morrón\n"
          "-10 Remolacha\n-11 Sopa Chica\n-12 Sopa Grande")
    while True:
        idCliente=idCliente
        idProducto=int(input("\nIngrese el Número del Producto deseado: "))
        producto = buscarProducto(idProducto)
        tipo=int(input("\nIngrese 1 para bolsa Chica, 2 para bolsa Grande: "))
        if tipo == 1:
            tipo="Chico"
        if tipo == 2:
            tipo="Grande"
        estado="Hacer"
        cantidad= int(input("\n¿Que cantidad? Ingrese un Número: "))
        for x in range(0,cantidad):
            conn.execute("INSERT INTO encargados VALUES (?, ?, ?, ?, ?, ?)",
                         (None, idCliente, producto, tipo, idProducto, estado))
            base.commit()
        dec=input("\nDesea agregar otro producto?\nPresione Enter para continuar, 1 para Terminar: ")
        if dec == "1":
            return False

def idPedidoAtxt(idPedido):
    texto=""
    for id in range(len(idPedido)):
        id=idPedido[id][0]
        id=str(id)
        texto=(texto+id+", ")
    texto=texto[:-2]
    return texto



def agregarPrecioTotal(idCliente):
    idPedido = buscarIdPedidos(idCliente)
    texto=idPedidoAtxt(idPedido)
    precio = precioTotal(idPedido)
    sentencia = ("UPDATE pedidos SET IDPedido = ?, PRECIO = ? WHERE IDCliente = ?;")
    conn.execute(sentencia, [texto, precio, idCliente])
    base.commit()


#---------------------------------

# PARA INGRESAR NUEVOS PRODUCTOS A LA BD
#ingresarProducto()

# --------------------------------

# PARA AGREGAR PEDIDOS A LA BD
idCliente=ingresarPedidos()
ingresarEncargue(idCliente)
agregarPrecioTotal(idCliente)
