from datetime import datetime
import sqlite3
base = sqlite3.connect('nuevabd.db')
conn = base.cursor()

conn.execute('''CREATE TABLE if not exists productos
	 (IDProducto INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	  NOMBRE TEXT,
	  TIPO TEXT,
	  PRECIO FLOAT );''')

conn.execute('''CREATE TABLE if not exists clientes
	 (IDCliente INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	  NOMBRE TEXT,
	  DIRE TEXT,
	  TEL TEXT);''')

conn.execute('''CREATE TABLE if not exists pedidos
	 (IDPedido INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	  IDCliente INTEGER,
	  IDProductos TEXT,
	  Precio FLOAT,
	  Fecha TEXT,
	  Estado TEXT );''')

conn.execute('''CREATE TABLE if not exists pendientes
	 (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	  IDPedido INTEGER,
	  Producto TEXT,
	  Tipo TEXT,
	  Cantidad INTEGER,
	  IDProducto INTEGER,
	  Estado TEXT );''')

# --------------------------------------------------------

def buscarClientes():
    sentencia = ("SELECT NOMBRE FROM clientes ORDER BY NOMBRE ASC;")
    conn.execute(sentencia)
    busqueda = conn.fetchall()
    base.commit()
    listaNombres = busqueda
    people = []
    people.append("Autocompletar...")
    for nmb in range(len(listaNombres)):
        agregar=listaNombres[nmb][0]
        people.append(agregar)
    return people

def buscarProductos():
    sentencia = ("SELECT NOMBRE FROM productos ;")
    conn.execute(sentencia)
    busqueda = conn.fetchall()
    base.commit()
    listaProductos = busqueda
    prod = []
    for nmb in range(len(listaProductos)):
        agregar=listaProductos[nmb][0]
        if agregar not in prod:
            prod.append(agregar)
    return prod
