from tkinter import *
from tkinter import ttk


mainWind = Tk()
mainWind.title("La Huerta Polar")
mainWind.geometry('350x510')
mainWind.resizable(width=False, height=False)
mainWind.configure(background='light blue')

canvas = Canvas(mainWind, width = 350, height = 115,bg="light blue")
canvas.pack()
img = PhotoImage(file="logo2.gif")
canvas.create_image(185,60, anchor=CENTER, image=img)

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

texto1 = Label(mainWind,text="INSTAGRAM - @LAHUERTAPOLAR",bg="LIGHT BLUE")
texto1.place(x=0,y=485,width=350,height=30)

# ---------------

scrollbar1 = Scrollbar(tomarPedido, orient=VERTICAL)
lstProductos = Listbox(tomarPedido, yscrollcommand=scrollbar1.set)
scrollbar1.config(command=lstProductos.yview)
scrollbar1.place(x=152, y=53, height=196)
lstProductos.place(x=8, y=53, width=145, height=196)
for item in ["Acelga","Brócoli","Calabaza","Cebolla","Chaucha","Coliflor",
             "Espinaca","Morrón","Remolacha","Sopa","Zanahoria","Zapallito"]:
    lstProductos.insert(END, item)

texto1 = Label(tomarPedido,text="TOMAR PEDIDOS",font=("bold",14))
texto1.place(x=0, y=9, width=350, height=20)
texto2 = Label(tomarPedido,text="Elegir Producto")
texto2.place(x=0, y=33, width=175, height=18)

texto3 = Label(tomarPedido,text="Tamaño")
texto3.place(x=196,y=53,width=50,height=18)

chk_state = IntVar()
chk_state.set(0)  # set check state
chk_state.set(1)
chico = Radiobutton(tomarPedido, text='Chico', value=0)
chico.place(x=180, y=74)
grande = Radiobutton(tomarPedido, text='Grande', value=1)
grande.place(x=180, y=103)

texto4 = Label(tomarPedido,text="Cantidad")
texto4.place(x=274,y=53,width=50,height=18)
cantidad = Spinbox(tomarPedido, from_=0, to=30, width=10)
cantidad.place(x=264, y=76)

precioInd = Label(tomarPedido,text="$ 185.00", anchor="center", fg="green", bg="white")
precioInd.place(x=264,y=105,width=75,height=20)

btnAgregar = Button(tomarPedido,text="Agregar")
btnAgregar.place(x=180, y=132, width=78)
btnBorrar = Button(tomarPedido,text="Borrar")
btnBorrar.place(x=264, y=132, width=75)

scrollbar2 = Scrollbar(tomarPedido, orient=VERTICAL)
lstAdd = Listbox(tomarPedido, yscrollcommand=scrollbar2.set)
scrollbar2.config(command=lstAdd.yview)
scrollbar2.place(x=323, y=165, height=52)
lstAdd.place(x=180, y=165, width=143, height=52)
for item in [""]:
    lstAdd.insert(END, item)

texto4 = Label(tomarPedido,text="TOTAL:",anchor="w",font="bold")
texto4.place(x=180,y=226,width=53,height=20)

texto5 = Label(tomarPedido,text="$ 80.00", anchor="center", fg="green",font="bold")
texto5.place(x=264,y=226,width=75,height=20)

texto6 = Label(tomarPedido,text="Cliente", anchor="center")
texto6.place(x=5,y=260,height=20)
clienteEntry = Entry(tomarPedido)
clienteEntry.place(x=62,y=260,width=108)
texto7 = Label(tomarPedido,text="Dirección", anchor="center")
texto7.place(x=5,y=288,height=20)
direcEntry = Entry(tomarPedido)
direcEntry.place(x=62,y=288,width=108)
texto8 = Label(tomarPedido,text="Teléfono", anchor="center")
texto8.place(x=5,y=316,height=20)
telEntry = Entry(tomarPedido)
telEntry.place(x=62,y=316,width=108)

clientesLoad = ttk.Combobox(tomarPedido)
clientesLoad.place(x=217,y=260, width=123)
clientesLoad['values'] = ("Autocompletar...",1, 2, 3, 4, 5)
clientesLoad.current(0)  # set the selected item

btnAuto = Button(tomarPedido,text="<")
btnAuto.place(x=180, y=259, width=30, height=22)

btnAddNew = Button(tomarPedido,text="Agregar\nCliente")
btnAddNew.place(x=180, y=288, width=78, height=50)
btnSave = Button(tomarPedido,text="Guardar\nPedido")
btnSave.place(x=264, y=288, width=75,height=50)

mainloop()
