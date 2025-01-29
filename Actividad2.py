from tkinter import *
from tkinter import font
import re

class VentanaVerificador:

    def ventana(self):
        #Creación de la ventana
        self.ventanaVerificador = Tk()
        self.ventanaVerificador.title("Verificador de datos")
        self.ventanaVerificador.geometry("800x600+560+240")

        #Objetos para cambiar fuente
        self.fuenteGrande = font.Font(size=20)

        #Creación de etiquetas
        self.etiTitulo = Label(self.ventanaVerificador, text = "Datos a verificar")
        self.etiTelefono = Label(self.ventanaVerificador, text = "Telefono:")
        self.etiCURP = Label(self.ventanaVerificador, text = "CURP:")
        self.etiRFC = Label(self.ventanaVerificador, text = "RFC:")
        self.etiCorreo = Label(self.ventanaVerificador, text = "Correo:")
        self.etiIP = Label(self.ventanaVerificador, text = "IPv6:")
        self.etiCumpleaños = Label(self.ventanaVerificador, text = "Cumpleaños:")

        #Cambio de fuentes de etiquetas
        self.etiTitulo.config(font=self.fuenteGrande)

        #Creación de cajas
        self.cajaTelefono = Entry(self.ventanaVerificador, borderwidth=2, relief="solid", width=25)
        self.cajaCURP = Entry(self.ventanaVerificador, borderwidth=2, relief="solid", width=25)
        self.cajaRFC = Entry(self.ventanaVerificador, borderwidth=2, relief="solid", width=25)
        self.cajaCorreo = Entry(self.ventanaVerificador, borderwidth=2, relief="solid", width=25)
        self.cajaIP = Entry(self.ventanaVerificador, borderwidth=2, relief="solid", width=25)
        self.cajaCumpleaños = Entry(self.ventanaVerificador, borderwidth=2, relief="solid", width=25)

        self.cajaVTelefono = Entry(self.ventanaVerificador, borderwidth=2, relief="solid", width=25)
        self.cajaVCURP = Entry(self.ventanaVerificador, borderwidth=2, relief="solid", width=25)
        self.cajaVRFC = Entry(self.ventanaVerificador, borderwidth=2, relief="solid", width=25)
        self.cajaVCorreo = Entry(self.ventanaVerificador, borderwidth=2, relief="solid", width=25)
        self.cajaVIP = Entry(self.ventanaVerificador, borderwidth=2, relief="solid", width=25)
        self.cajaVCumpleaños = Entry(self.ventanaVerificador, borderwidth=2, relief="solid", width=25)

        #Creación de botones 
        self.evaluar = Button(self.ventanaVerificador, text = "Evaluar", command=lambda: self.verificadorDeDatos()) 
        self.limpiar = Button(self.ventanaVerificador, text = "Limpiar", command=lambda: self.limpiarCampos())

        #Posicionamiento de etiquetas
        self.etiTitulo.place(x=100, y=10)
        self.etiTelefono.place(in_=self.ventanaVerificador, x=80, y=90)
        self.etiTelefono.lift()
        self.etiCURP.place(in_=self.ventanaVerificador, x=80, y=130)
        self.etiCURP.lift()
        self.etiRFC.place(in_=self.ventanaVerificador, x=80, y=170)
        self.etiRFC.lift()
        self.etiCorreo.place(in_=self.ventanaVerificador, x=80, y=210)
        self.etiCorreo.lift()
        self.etiIP.place(in_=self.ventanaVerificador, x=80, y=250)
        self.etiIP.lift()
        self.etiCumpleaños.place(in_=self.ventanaVerificador, x=80, y=290)
        self.etiCumpleaños.lift()

        #Posicionamiento de cajas
        self.cajaTelefono.place(in_=self.ventanaVerificador, x=170, y=90)
        self.cajaCURP.place(in_=self.ventanaVerificador, x=170, y=130)
        self.cajaRFC.place(in_=self.ventanaVerificador, x=170, y=170)
        self.cajaCorreo.place(in_=self.ventanaVerificador, x=170, y=210)
        self.cajaIP.place(in_=self.ventanaVerificador, x=170, y=250)
        self.cajaCumpleaños.place(in_=self.ventanaVerificador, x=170, y=290)

        self.cajaVTelefono.place(in_=self.ventanaVerificador, x=360, y=90)
        self.cajaVCURP.place(in_=self.ventanaVerificador, x=360, y=130)
        self.cajaVRFC.place(in_=self.ventanaVerificador, x=360, y=170)
        self.cajaVCorreo.place(in_=self.ventanaVerificador, x=360, y=210)
        self.cajaVIP.place(in_=self.ventanaVerificador, x=360, y=250)
        self.cajaVCumpleaños.place(in_=self.ventanaVerificador, x=360, y=290)

        #Deshabilitar las cajas de resultado
        self.cajaVTelefono.config(state=DISABLED)
        self.cajaVCURP.config(state=DISABLED)
        self.cajaVRFC.config(state=DISABLED)
        self.cajaVCorreo.config(state=DISABLED)
        self.cajaVIP.config(state=DISABLED)
        self.cajaVCumpleaños.config(state=DISABLED)

        #Posicionamiento de botones
        self.evaluar.place(in_=self.ventanaVerificador, x=240, y=350)
        self.limpiar.place(in_=self.ventanaVerificador, x=340, y=350)

        #Desactivar botón de limpiar por defecto
        self.limpiar.config(state=DISABLED)
    
    def verificadorDeDatos(self):

        #Obtener los datos introducidos
        textoTelefono = self.cajaTelefono.get()
        textoCURP = self.cajaCURP.get()
        textoRFC = self.cajaRFC.get()
        textoCorreo = self.cajaCorreo.get()
        textoIP = self.cajaIP.get()
        textoCumpleaños = self.cajaCumpleaños.get()

        #Evaluación de cadenas

        #CURP
        muestraCURP = r"[A-Z]{1}[A|E|I|O|U]{1}[A-Z]{2}\d{2}(0[1-9]|1[0-2]){2}[H|M]{1}(AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS){1}[B|C|D|F|G|H|J|K|L|M|N|Ñ|P|Q|R|S|T|V|W|X|Y|Z]{3}([0-9]|[A-Z]){1}\d{1}"
        self.cajaVCURP.config(state=NORMAL)
        if re.match(muestraCURP, textoCURP.upper()):
            self.cajaVCURP.insert(0, "Texto bien escrito")
        else:
            self.cajaVCURP.insert(0, "Texto mal escrito")

        #RFC
        muestraRFC = r"[A-Z]{1}[A|E|I|O|U]{1}[A-Z]{2}\d{2}(0[1-9]|1[0-2]){2}[A-Z0-9]{3}$"
        self.cajaVRFC.config(state=NORMAL)
        if re.match(muestraRFC, textoRFC.upper()):
            self.cajaVRFC.insert(0, "Texto bien escrito")
        else:
            self.cajaVRFC.insert(0, "Texto mal escrito")

        #Telefono
        muestraTelefono = r"33[0-9]{8}"
        self.cajaVTelefono.config(state=NORMAL)
        if re.match(muestraTelefono, textoTelefono.upper()):
            self.cajaVTelefono.insert(0, "Texto bien escrito")
        else:
            self.cajaVTelefono.insert(0, "Texto bien escrito")

        #Correo
        muestraCorreo = r"\S{3,30}@gmail.com$"
        self.cajaVCorreo.config(state=NORMAL)
        if re.match(muestraCorreo, textoCorreo.lower()):
            self.cajaVCorreo.insert(0, "Texto bien escrito")
        else:
            self.cajaVCorreo.insert(0, "Texto mal escrito")

        #IPV6
        muestraIP = r"^([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4})$"
        self.cajaVIP.config(state=NORMAL)
        if re.match(muestraIP, textoIP.lower()):
            self.cajaVIP.insert(0, "Texto bien escrito")
        else:
            self.cajaVIP.insert(0, "Texto mal escrito") 

        #Cumpleaños
        muestraCumpleaños = r"(0[1-9]|1[0-9]|2[0-9]|3[0-1]){1}/(0[1-9]|1[0-2]){1}/(19[0-9]{2}|20[0-2][0-5])$"
        self.cajaVCumpleaños.config(state=NORMAL)
        if re.match(muestraCumpleaños, textoCumpleaños):
            self.cajaVCumpleaños.insert(0, "Texto bien escrito")
        else:
            self.cajaVCumpleaños.insert(0, "Texto mal escrito")

        #Deshabilitar las cajas de resultado
        self.cajaVTelefono.config(state=DISABLED)
        self.cajaVCURP.config(state=DISABLED)
        self.cajaVRFC.config(state=DISABLED)
        self.cajaVCorreo.config(state=DISABLED)
        self.cajaVIP.config(state=DISABLED)
        self.cajaVCumpleaños.config(state=DISABLED)

        #Habilitar y deshabilitar botones
        self.limpiar.config(state=NORMAL)
        self.evaluar.config(state=DISABLED)
    
    def limpiarCampos(self):
        #Habilitar las cajas de resultado
        self.cajaVTelefono.config(state=NORMAL)
        self.cajaVCURP.config(state=NORMAL)
        self.cajaVRFC.config(state=NORMAL)
        self.cajaVCorreo.config(state=NORMAL)
        self.cajaVIP.config(state=NORMAL)
        self.cajaVCumpleaños.config(state=NORMAL)

        #Limpiar campos
        self.cajaVTelefono.delete(0,END)
        self.cajaVCURP.delete(0,END)
        self.cajaVRFC.delete(0,END)
        self.cajaVCorreo.delete(0,END)
        self.cajaVIP.delete(0,END)
        self.cajaVCumpleaños.delete(0,END)

        self.cajaTelefono.delete(0,END)
        self.cajaCURP.delete(0,END)
        self.cajaRFC.delete(0,END)
        self.cajaCorreo.delete(0,END)
        self.cajaIP.delete(0,END)
        self.cajaCumpleaños.delete(0,END)

        #Habilitar y deshabilitar botones
        self.limpiar.config(state=DISABLED)
        self.evaluar.config(state=NORMAL)


    def run(self):
        #Mantener la ventana abierta
        self.ventana()
        self.ventanaVerificador.mainloop()

app =  VentanaVerificador()
app.run()