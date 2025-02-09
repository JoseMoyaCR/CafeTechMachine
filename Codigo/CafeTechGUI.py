import tkinter as tk
from tkinter import messagebox
from CafeTechBL import LogicaMaquinaCafe
from time import sleep
from threading import Thread

class InterfazMaquinaCafe:
    def __init__(self):
        self.logica = LogicaMaquinaCafe()
        self.root = tk.Tk()
        self.root.title("CafeTech Machine")
        self.root.geometry("400x600")
        self.root.configure(bg="#f0f0f0")
        self.crearInterfaz()
        self.listaCafes.select_set(0)
        self.listaCafes.event_generate("<<ListboxSelect>>")
        self.logica.conectarBotones(self)
        
        self.root.protocol("WM_DELETE_WINDOW", self.salir)

    def crearInterfaz(self):
        lblTitulo = tk.Label(self.root, text="Bienvenido a CafeTech", font=("Arial", 16, "bold"), bg="#f0f0f0")
        lblTitulo.pack(pady=10)

        self.lblSeleccion = tk.Label(self.root, text="Seleccione su bebida:", font=("Arial", 14), bg="#f0f0f0")
        self.lblSeleccion.pack()

        self.listaCafes = tk.Listbox(self.root, font=("Arial", 12), height=8)
        for cafe in self.logica.recetas.keys():
            self.listaCafes.insert(tk.END, cafe)
        self.listaCafes.pack(pady=5)

        self.lblPrecio = tk.Label(self.root, text="Precio: $0.00", font=("Arial", 12), bg="#f0f0f0")
        self.lblPrecio.pack(pady=5)

        frmBotones = tk.Frame(self.root, bg="#f0f0f0")
        frmBotones.pack(pady=10)

        self.btnSubir = tk.Button(frmBotones, text="Subir", font=("Arial", 12), command=self.subirSeleccion)
        self.btnSubir.grid(row=0, column=0, padx=10)

        self.btnBajar = tk.Button(frmBotones, text="Bajar", font=("Arial", 12), command=self.bajarSeleccion)
        self.btnBajar.grid(row=0, column=1, padx=10)

        self.btnSeleccionar = tk.Button(frmBotones, text="Seleccionar bebida", font=("Arial", 12), command=self.seleccionarBebida)
        self.btnSeleccionar.grid(row=1, column=0, columnspan=2, pady=5)

        self.btnPagar = tk.Button(self.root, text="Pagar", font=("Arial", 12), command=self.pagar, state=tk.DISABLED)
        self.btnPagar.pack(pady=5)

        self.btnIniciar = tk.Button(self.root, text="Iniciar", font=("Arial", 12), command=self.iniciarPreparacion, state=tk.DISABLED)
        self.btnIniciar.pack(pady=5)

        self.lblEstado = tk.Label(self.root, text="Estado: Seleccione una bebida.", font=("Arial", 12), bg="#f0f0f0", fg="blue")
        self.lblEstado.pack(pady=10)

        self.barraProgreso = tk.Label(self.root, text="", font=("Arial", 12), bg="white", width=30, height=2, relief="sunken", anchor="w")
        self.barraProgreso.pack(pady=10)
        
    def setGUInicio(self):
        self.btnSubir.config(state=tk.NORMAL)
        self.btnBajar.config(state=tk.NORMAL)
        self.btnSeleccionar.config(state=tk.NORMAL)
        self.btnPagar.config(state=tk.DISABLED)
        self.btnIniciar.config(state=tk.DISABLED)
        self.lblEstado.config(text="Estado: Seleccione una bebida.", fg="blue")
        self.logica.actualizarLCD("Bebida:", self.listaCafes.get(self.listaCafes.curselection()[0]))
        self.barraProgreso.config(bg="white", text="")
        self.root.update()
        
    def setGUIPagando(self):
        self.btnSubir.config(state=tk.DISABLED)
        self.btnBajar.config(state=tk.DISABLED)
        self.btnSeleccionar.config(state=tk.DISABLED)
        self.btnPagar.config(state=tk.NORMAL)
        self.btnIniciar.config(state=tk.DISABLED)
        self.lblEstado.config(text="Estado: Cafe seleccionado. Proceda con el pago.", fg="blue")
        self.logica.actualizarLCD("Cafe seleccionado", "Proceda a pagar")
        self.barraProgreso.config(bg="white", text="")
        self.root.update()
        
    def setGUIPreparandoBebida(self):
        self.btnSubir.config(state=tk.DISABLED)
        self.btnBajar.config(state=tk.DISABLED)
        self.btnSeleccionar.config(state=tk.DISABLED)
        self.btnPagar.config(state=tk.DISABLED)
        self.btnIniciar.config(state=tk.DISABLED)
        self.lblEstado.config(text="Estado: Preparacion en curso.", fg="orange")
        self.logica.actualizarLCD("Preparando", "bebida...")
        self.root.update()

    def actualizarProgresoTemp(self, temperatura):
        self.barraProgreso.config(bg="red", text=f"0% - Calentando el agua Temp: {temperatura:.1f} C")
        self.logica.actualizarLCD("Calentando agua", f"Temp: {temperatura:.1f} C")
        self.root.update()
        
    def actualizarProgreso(self, porcentaje, temperatura):
        if porcentaje != 100:
            self.barraProgreso.config(bg="orange", text=f"{porcentaje}% - Preparando bebida")
            self.logica.actualizarLCD("Preparando", f"bebida {porcentaje}%")
        else:
            self.barraProgreso.config(bg="green", text=f"{porcentaje}% - Preparacion finalizada")
            self.logica.actualizarLCD("Preparacion", f"finalizada {porcentaje}%")
        self.root.update()
        
    def finalizarPreparacion(self, exito, mensaje):
        if exito:
            self.logica.activarSonido("servida")
            self.lblEstado.config(text=f"Estado: {mensaje}", fg="green")
            self.mostrarMessageBox(tk.messagebox.showinfo, "Bebida lista", "Su bebida esta lista para disfrutar.")
            self.setGUInicio()
        else:
            self.logica.activarSonido("error")
            self.logica.actualizarLCD("Error", "Intente de nuevo")
            self.lblEstado.config(text="Estado: Intente de nuevo.", fg="red")
            self.mostrarMessageBox(tk.messagebox.showerror, "Error", mensaje)
            self.btnIniciar.config(state=tk.NORMAL)

    def subirSeleccion(self):
        if self.logica.procesoEnCurso:
            print("Proceso en curso. Accion ignorada.")
            return
            
        self.logica.activarSonido("desplazar")
        seleccion = self.listaCafes.curselection()
        if seleccion:
            indice = seleccion[0]
            if indice > 0:
                self.listaCafes.select_clear(indice)
                self.listaCafes.select_set(indice - 1)
                self.listaCafes.activate(indice - 1)
                self.logica.actualizarLCD("Bebida:", self.listaCafes.get(indice - 1))

    def bajarSeleccion(self):
        if self.logica.procesoEnCurso:
            print("Proceso en curso. Accion ignorada.")
            return
        
        self.logica.activarSonido("desplazar")
        seleccion = self.listaCafes.curselection()
        if seleccion:
            indice = seleccion[0]
            if indice < self.listaCafes.size() - 1:
                self.listaCafes.select_clear(indice)
                self.listaCafes.select_set(indice + 1)
                self.listaCafes.activate(indice + 1)
                bebida = self.listaCafes.get(indice + 1)
                self.logica.actualizarLCD("Bebida:", self.listaCafes.get(indice + 1))

    def seleccionarBebida(self):
        if self.logica.procesoEnCurso:
            print("Proceso en curso. Accion ignorada.")
            return
            
        self.logica.activarSonido("seleccionar")
        seleccion = self.listaCafes.get(tk.ACTIVE)
        if seleccion:
            precio = self.logica.recetas[seleccion]['precio']
            self.lblPrecio.config(text=f"Precio: ${precio:.2f}")
            self.setGUIPagando()
            self.pagar()

    def pagar(self):
        def callback(exito, mensaje):
            if exito:
                self.logica.activarSonido("pagado")
                self.lblEstado.config(text="Estado: Pagado. Presione Iniciar.", fg="green")
                self.logica.actualizarLCD("Pago exitoso", "Presione iniciar")
                self.btnPagar.config(state=tk.DISABLED)
                self.btnIniciar.config(state=tk.NORMAL)
            else:
                self.logica.activarSonido("error")
                self.logica.procesoEnCurso = False
                self.logica.actualizarLCD("Error", "Pago fallido")
                self.lblEstado.config(text="Estado: No pagado. Intente de nuevo.", fg="red")
                self.mostrarMessageBox(tk.messagebox.showerror, "Error", mensaje)
                self.setGUInicio()

        self.logica.validarTarjetaAsync(callback)

    def iniciarPreparacion(self):
        if self.logica.procesoEnCurso:
            print("Proceso en curso. Accion ignorada.")
            return
            
        self.logica.activarSonido("preparando")
        seleccion = self.listaCafes.get(tk.ACTIVE)
        if seleccion:
            self.setGUIPreparandoBebida()
            self.logica.prepararCafeAsync(seleccion, self.actualizarProgreso, self.actualizarProgresoTemp, self.finalizarPreparacion)

    def mostrarMessageBox(self, message_func, title, message):
        msgAlert = tk.Toplevel(self.root)
        msgAlert.title(title)
        msgAlert.geometry("300x150")
        msgAlert.configure(bg="#f0f0f0")

        lblMensaje = tk.Label(msgAlert, text=message, font=("Arial", 12), bg="#f0f0f0")
        lblMensaje.pack(pady=20)

        btnCerrar = tk.Button(msgAlert, text="Cerrar", font=("Arial", 12), command=msgAlert.destroy)
        btnCerrar.pack(pady=10)

        msgAlert.after(3000, msgAlert.destroy)
        
    def iniciar(self):
        self.root.mainloop()
        
    def salir(self):
        self.logica.apagarComponentes()
        self.root.destroy()

if __name__ == "__main__":
    app = InterfazMaquinaCafe()
    app.iniciar()
