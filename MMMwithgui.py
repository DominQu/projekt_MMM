import matplotlib 
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
style.use('ggplot')

import tkinter as tk
from tkinter import ttk
import math

#create plot and initialize animation function
f = Figure(figsize=(10,8), dpi=100)
a = f.add_subplot(111)

def animate_plot():

    a.clear()
    a.plot(model.time, root.page1.model.y, "#00A3E0", label="sygnał y")
    a.plot(model.time, root.page1.model.c, "#183A54", label="sygnał c")
    a.plot(model.time, root.page1.model.u, "#EE8E3B", label="sygnał u")
    a.legend(loc=2, bbox_to_anchor=(0.22,1.1,), ncol=3, borderaxespad=0)

class Window(tk.Tk):

    def __init__(self, model):
    
        super().__init__()
        self.wm_title("MMM projekt")

        self.page1 = Page(model, self)
        self.page1.pack()

class Page(tk.Frame):

    def __init__(self,model, master=None):

        super().__init__(master)
        
        self.model = model
        
        #--------------------------
        # GUI elements:
        #--------------------------

        #wybór pobudzenia
        self.radio_var = tk.StringVar()
        self.label1 = ttk.Label(self, text="Pobudzenie:", font=("Verdana", 16))
        self.label1.grid(row=1, column=0, columnspan=3)
        self.radio1 = ttk.Radiobutton(self, text="sin", variable=self.radio_var, value="sin")
        self.radio2 = ttk.Radiobutton(self, text="rec", variable=self.radio_var, value="rec")
        self.radio3 = ttk.Radiobutton(self, text="unit", variable=self.radio_var, value="unit")
        self.radio_var.set("sin")
        self.radio1.grid(row=2, column=0)
        self.radio2.grid(row=2, column=1)
        self.radio3.grid(row=2, column=2, padx=15)

        #wybór rodzaju c
        self.c_var = tk.StringVar()
        self.label2 = ttk.Label(self, text="Rodzaj c:", font=("Verdana", 16))
        self.label2.grid(row=3, column=0, columnspan=3)
        self.c_radio1 = ttk.Radiobutton(self, text="Stałe", variable=self.c_var, value="const")
        self.c_radio2 = ttk.Radiobutton(self, text="Zmienne", variable=self.c_var, value="var")
        self.c_var.set("const")
        self.c_radio1.grid(row=4, column=0)
        self.c_radio2.grid(row=4, column=1)

        #wprowadzanie parametru a
        self.label3 = ttk.Label(self, text="Podaj a:", font=("Verdana", 12))
        self.label3.grid(row=5, column=0, columnspan=1)
        self.a_var = tk.StringVar()
        self.entry1 = tk.Entry(self, width=10, text=self.a_var)
        self.entry1.grid(row=5, column = 1)
        self.a_var.set("1") 

        #wprowadzanie parametru b
        self.label4 = ttk.Label(self, text="Podaj b:", font=("Verdana", 12))
        self.label4.grid(row=6, column=0, columnspan=1)
        self.b_var = tk.StringVar()
        self.entry2 = tk.Entry(self, width=10, text=self.b_var)
        self.entry2.grid(row=6, column = 1)
        self.b_var.set("1")

        #wprowadzanie parametru A
        self.label5 = ttk.Label(self, text="Podaj A:", font=("Verdana", 12))
        self.label5.grid(row=7, column=0, columnspan=1)
        self.A_var = tk.StringVar()
        self.entry3 = tk.Entry(self, width=10, text=self.A_var)
        self.entry3.grid(row=7, column = 1)
        self.A_var.set("1") 

        #wprowadzanie parametru Amp
        self.label5 = ttk.Label(self, text="      Podaj\n  amplitude\n pobudzenia:", font=("Verdana", 12))
        self.label5.grid(row=8, column=0, columnspan=1)
        self.Amp_var = tk.StringVar()
        self.entry4 = tk.Entry(self, width=10, text=self.Amp_var)
        self.entry4.grid(row=8, column = 1)
        self.Amp_var.set("1")

        #wprowadzanie parametru B
        self.label6 = ttk.Label(self, text="Podaj B:", font=("Verdana", 12))
        self.label6.grid(row=9, column=0, columnspan=1)
        self.B_var = tk.StringVar()
        self.entry5 = tk.Entry(self, width=10, text=self.B_var)
        self.entry5.grid(row=9, column = 1)
        self.B_var.set("1")

        #przycisk: pokazanie wyniku na wykresie
        self.button1 = ttk.Button(self, text="Start", command=lambda: self.UpdateSim())
        self.button1.grid(row=10, column=1)
        
        #tworzenie wykresu i panelu nawigacyjnego    
        canvas = FigureCanvasTkAgg(f, self)
        toolbar = NavigationToolbar2Tk(canvas, self, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=11, column=3)
        canvas.get_tk_widget().grid(row=1, column=3, rowspan=10)

    def UpdateSim(self):
        
        self.model.update(param_a = float(self.a_var.get()), 
                          param_b = float(self.b_var.get()),
                          param_A = float(self.A_var.get()),
                          param_Amp = float(self.Amp_var.get()),
                          param_B = float(self.B_var.get()),
                          rodzaj_c = self.c_var.get(),
                          pobudzenie = self.radio_var.get()
                          )
        animate_plot()
        f.canvas.draw()
        
class Taylor:

    def __init__(self):

        #constants
        self.T = 20.
        self.N = 10000                              #liczba kroków symulacji
        self.h = self.T / self.N                    #dyskretny krok symulacji
        self.P = 3.                                 #liczba okresów pobudzenia w czasie symulacji
        self.w = 1 / (self.T/self.P) * 2 * math.pi  #pulsacja pobudzenia (dla sinusoidy i fali prostokątnej)

        #lists for data
        self.time = [i*self.h for i in range(self.N)]
        self.u = [0 for i in range(self.N)]         #pobudzenie
        self.c = [0 for i in range(self.N)]         #zmienny parametr c
        self.y = [0 for i in range(self.N)]         #wartość wyjściowa
        self.y1p = [0 for i in range(self.N)]       #pierwsza pochodna wartości wyjściowej
        self.y2p = [0 for i in range(self.N)]       #druga pochodna wartości wyjściowej
        self.y3p = [0 for i in range(self.N)]       #trzecia pochodna wartości wyjściowej

    def update(self, param_a=1, param_b=1, param_A=3, param_B=1, param_Amp=1, rodzaj_c = "const", pobudzenie = "sin"):
        
        self.a = param_a
        self.b = param_b
        self.B = param_B
        self.A = param_A
        self.Amp = param_Amp

        if rodzaj_c == "const":

            for i in range(self.N):

                self.c[i] = self.A

        elif rodzaj_c == "var":

            for i in range(self.N):

                x = self.A + self.A*math.exp(-self.B * (i * self.h)**2 )
                self.c[i] = x
        
        if pobudzenie == "sin":

            for i in range(self.N):

                x = self.Amp * math.sin(self.w * i * self.h)
                self.u[i] = x

        elif pobudzenie == "rec":

            for i in range(self.N):

                x = self.Amp * math.sin(self.w * i * self.h)
                if x > 0:
                    self.u[i] = self.Amp
                else:
                    self.u[i] = -self.Amp

        elif pobudzenie == "unit":

            for i in range(self.N):

                self.u[i] = self.Amp
        
        self.calculate_y()
    
    def calculate_y(self):
        
        for i in range(self.N-1):

            self.y3p[i] = -self.a * self.y2p[i] - self.b * self.y1p[i] - self.c[i] * self.y[i] + self.u[i]
            self.y2p[i+1] = self.y2p[i] + self.h * self.y3p[i]
            self.y1p[i+1] = self.y1p[i] + self.h * self.y2p[i] + (self.h ** 2 / 2.) * self.y3p[i]
            self.y[i+1] = self.y[i] + self.h * self.y1p[i] + (self.h ** 2 / 2.) * self.y2p[i] + (self.h ** 3 / 6.) * self.y3p[i]

if __name__ == "__main__":

    model = Taylor()
    root = Window(model)
    root.mainloop()
