import tkinter as tk
from tkinter import messagebox

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.izquierdo = None
        self.derecho = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def agregar_nodo(self, valor, valor_padre=None, direccion=None):
        nuevo = Nodo(valor)
        if not self.raiz:
            self.raiz = nuevo
            return True
        padre = self.buscar(self.raiz, valor_padre)
        if padre:
            direccion = direccion.lower()
            if direccion in ["izquierdo", "i"] and padre.izquierdo is None:
                padre.izquierdo = nuevo
            elif direccion in ["derecho", "d"] and padre.derecho is None:
                padre.derecho = nuevo
            else:
                return False
            return True
        return False

    def buscar(self, nodo, valor):
        if not nodo or nodo.dato == valor:
            return nodo
        return self.buscar(nodo.izquierdo, valor) or self.buscar(nodo.derecho, valor)

    def recorrido(self, tipo):
        if tipo == 'InOrden':
            return self.inorden(self.raiz, [])
        elif tipo == 'PreOrden':
            return self.preorden(self.raiz, [])
        elif tipo == 'PostOrden':
            return self.postorden(self.raiz, [])

    def inorden(self, nodo, recorrido):
        if nodo:
            self.inorden(nodo.izquierdo, recorrido)
            recorrido.append(nodo.dato)
            self.inorden(nodo.derecho, recorrido)
        return recorrido

    def preorden(self, nodo, recorrido):
        if nodo:
            recorrido.append(nodo.dato)
            self.preorden(nodo.izquierdo, recorrido)
            self.preorden(nodo.derecho, recorrido)
        return recorrido

    def postorden(self, nodo, recorrido):
        if nodo:
            self.postorden(nodo.izquierdo, recorrido)
            self.postorden(nodo.derecho, recorrido)
            recorrido.append(nodo.dato)
        return recorrido

    def animar_recorrido(self, canvas, tipo, label_resultado):
        recorrido = self.recorrido(tipo)
        label_resultado.config(text=f"Recorrido {tipo}: " + " ".join(map(str, recorrido)))
        self._animar_nodos(canvas, recorrido, 0)

    def _animar_nodos(self, canvas, recorrido, index):
        if index < len(recorrido):
            nodo_actual = recorrido[index]
            self.resaltar_nodo(canvas, nodo_actual, "yellow")
            canvas.after(500, lambda: self.resaltar_nodo(canvas, nodo_actual, "#00FF7F"))
            canvas.after(600, lambda: self._animar_nodos(canvas, recorrido, index + 1))

    def resaltar_nodo(self, canvas, valor, color):
        items = canvas.find_withtag(f"nodo-{valor}")
        if items:
            for item in items:
                canvas.itemconfig(item, fill=color)

    def mostrar_arbol(self, canvas, x=400, y=50, distancia=100, nodo=None, delay=500):
        if nodo is None:
            nodo = self.raiz
        if nodo:
            canvas.create_oval(x-20, y-20, x+20, y+20, fill="#00FF7F", outline="white", width=2, tags=f"nodo-{nodo.dato}")
            canvas.create_text(x, y, text=str(nodo.dato), font=("Poppins", 12, "bold"), fill="white", tags=f"texto-{nodo.dato}")

            if nodo.izquierdo:
                canvas.after(delay, lambda: self.animar_linea(canvas, x, y+20, x-distancia, y+distancia-20))
                self.mostrar_arbol(canvas, x-distancia, y+distancia, distancia-10, nodo.izquierdo, delay)

            if nodo.derecho:
                canvas.after(delay, lambda: self.animar_linea(canvas, x, y+20, x+distancia, y+distancia-20))
                self.mostrar_arbol(canvas, x+distancia, y+distancia, distancia-10, nodo.derecho, delay)

    def animar_linea(self, canvas, x1, y1, x2, y2):
        canvas.create_line(x1, y1, x2, y2, fill="white", width=2)

def crear_boton_con_animacion(parent, texto, comando):
    boton = tk.Button(parent, text=texto, font=("Poppins", 12), bg="#2E2E2E", fg="white",
                      activebackground="#00FF7F", relief="flat", bd=0, command=comando)
    boton.config(width=12, height=2)
    boton.bind("<Enter>", lambda e: boton.config(bg="#00FF7F"))
    boton.bind("<Leave>", lambda e: boton.config(bg="#2E2E2E"))
    return boton

def ventana_agregar():
    ventana = tk.Toplevel(bg="#1C1C1C")
    ventana.title("Agregar Nodo")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Valor del Nodo:", font=("Poppins", 12), bg="#1C1C1C", fg="white").pack(pady=10)
    entrada_valor = tk.Entry(ventana, font=("Poppins", 12))
    entrada_valor.pack()

    tk.Label(ventana, text="Nodo Padre (opcional):", font=("Poppins", 12), bg="#1C1C1C", fg="white").pack(pady=10)
    entrada_padre = tk.Entry(ventana, font=("Poppins", 12))
    entrada_padre.pack()

    tk.Label(ventana, text="Dirección (i/d o izquierdo/derecho):", font=("Poppins", 12), bg="#1C1C1C", fg="white").pack(pady=10)
    entrada_direccion = tk.Entry(ventana, font=("Poppins", 12))
    entrada_direccion.pack()

    def agregar():
        valor = entrada_valor.get()
        nodo_padre = entrada_padre.get()
        direccion = entrada_direccion.get().lower()
        if valor.isdigit():
            valor = int(valor)
            nodo_padre = int(nodo_padre) if nodo_padre.isdigit() else None
            if arbol.agregar_nodo(valor, nodo_padre, direccion):
                messagebox.showinfo("Éxito", f"Nodo {valor} agregado.")
                actualizar_arbol()
            else:
                messagebox.showerror("Error", "No se pudo agregar el nodo.")
            ventana.destroy()
        else:
            messagebox.showerror("Error", "El valor debe ser un número.")

    crear_boton_con_animacion(ventana, "Agregar", agregar).pack(pady=20)

def actualizar_arbol():
    canvas.delete("all")
    arbol.mostrar_arbol(canvas)

ventana = tk.Tk()
ventana.title("Árbol Binario")
ventana.config(bg="#1C1C1C")

arbol = ArbolBinario()
canvas = tk.Canvas(ventana, bg="#1C1C1C", width=800, height=600, highlightthickness=0)
canvas.pack()

label_resultado = tk.Label(ventana, text="", font=("Poppins", 12), bg="#1C1C1C", fg="white")
label_resultado.pack(pady=10)

frame_botones = tk.Frame(ventana, bg="#1C1C1C")
frame_botones.pack(pady=10)

crear_boton_con_animacion(frame_botones, "Agregar Nodo", ventana_agregar).grid(row=0, column=0, padx=5)
crear_boton_con_animacion(frame_botones, "InOrden", lambda: arbol.animar_recorrido(canvas, 'InOrden', label_resultado)).grid(row=0, column=1, padx=5)
crear_boton_con_animacion(frame_botones, "PreOrden", lambda: arbol.animar_recorrido(canvas, 'PreOrden', label_resultado)).grid(row=0, column=2, padx=5)
crear_boton_con_animacion(frame_botones, "PostOrden", lambda: arbol.animar_recorrido(canvas, 'PostOrden', label_resultado)).grid(row=0, column=3, padx=5)

ventana.mainloop()
