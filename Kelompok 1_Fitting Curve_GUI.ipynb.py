import numpy as np
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt


def open_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry_var.set(file_path)


def jacobimethod(A, b):
    x = np.array([0] * len(b))
    err = np.inf
    it = 0
    while err > 1e-3:
        x_n = np.array([0.0] * len(x))
        for i in range(len(x)):
            x_n[i] = b[i]
            for j in range(len(x)):
                if i < j:
                    x_n[i] -= A[i][j]*x[j]
            x_n[i] /= A[i][i]
        err = np.linalg.norm(x_n-x, np.inf)/np.linalg.norm(x_n, np.inf)
        x = x_n
        it += 1
    return x


def lin():
    file_path = entry_var.get()
    if file_path:
        try:
            df1 = pd.read_csv(file_path)

            x = df1[str(ex.get())]
            y = df1[str(ey.get())]
            z = df1[str(ez.get())]
            
            A = np.array([
                [len(x), sum(x), sum(y)],
                [sum(x), sum(x**2), sum(x*y)],
                [sum(y), sum(x*y), sum(y*y)]
            ])
            b = np.array([sum(z), sum(x*z), sum(y*z)])
            
            res = jacobimethod(A, b)
            
            f1 = lambda x1, x2: res[0] + res[1]*x1 + res[2]*x2

            x_surf, y_surf = np.meshgrid(np.linspace(min(x), max(x), 100), np.linspace(min(y), max(y), 100))
            z_surf = f1(x_surf, y_surf)

            fig = plt.figure(figsize=(20,10))
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(x,y,z,c='red', marker='o', alpha=0.5)
            ax.plot_surface(x_surf,y_surf,z_surf, color='b', alpha=0.3)
            ax.set_xlabel(str(ex.get()))
            ax.set_ylabel(str(ey.get()))
            ax.set_zlabel(str(ez.get()))
            plt.show()

        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Silakan pilih file CSV terlebih dahulu.")


def nonlin():
    file_path = entry_var.get()
    if file_path:
        try:
            df2 = pd.read_csv(file_path)
            x = df2[str(ex.get())]
            y = df2[str(ey.get())]

            A = np.array([
                [len(x), sum(x), sum(x**2)],
                [sum(x), sum(x**2), sum(x**3)],
                [sum(x**2), sum(x**3), sum(x**4)]
            ])
            b = np.array([sum(y), sum(x*y), sum(x**2*y)])

            res = jacobimethod(A, b)

            f2 = lambda x: res[0] + res[1]*x + res[2]*x**2

            x_surf = np.linspace(min(x), max(x), 1000)
            y_surf = [f2(i) for i in x_surf]

            plt.plot(x, y, 'go')
            plt.plot(x_surf, y_surf)

        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Silakan pilih file CSV terlebih dahulu.")



root = tk.Tk()
root.title("FITTING CURVE")

judul = tk.Label( root, text = "FITTING CURVE", font=("Times New Roman", 20, "bold"), justify="center") 
judul.grid(row=0, column=0, columnspan=2, pady=5)

Anggota = tk.Label(root,text="Rachmad Rifai\t\t\t(24060122120014)\nDzu Sunan Muhammad\t\t(24060122120034)\nThoriq Hadiwinata\t\t(24060122130086)\nMuhammad Fakhrell Andreaz\t(24060122140042)\nFarid Rahman Fadhilah\t\t(24060122140142)\nAdib Willy Kusuma Adrigantara\t(24060122140158)",justify="center")
Anggota.grid(row=1,column=0, columnspan=2, padx=10)


butt = 0

def hasil():
    global butt
    if(butt==1):
        lin()
    elif(butt==2):
        nonlin()

def buttl():
    global butt
    butt = 1
    hasil()

def buttnl():
    global butt
    butt = 2
    hasil()





l = tk.Button(root, text="Hasil", command=buttl)
l.grid(row=8, column=0, columnspan=2, pady=5)

nl = tk.Button(root, text="Click me first", bg="red", command=buttnl)
nl.grid(row=9, column=0, columnspan=2, pady=5)




entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, width=30)
entry.grid(row=3, column=0, padx=10, pady=10)

open_button = tk.Button(root, text="Open CSV", command=open_csv_file)
open_button.grid(row=3, column=1, padx=10, pady=10)

ex = tk.StringVar()
ex = tk.Entry(root, textvariable="x", width=30)
ex.grid(row=4, column=0, padx=10, pady=10)

lx = tk.Label(text="as\t X", font=("Times New Roman", 10, "bold"))
lx.grid(row=4, column=1, padx=10, pady=10)

ey = tk.StringVar()
ey = tk.Entry(root, textvariable="y", width=30)
ey.grid(row=5, column=0, padx=10, pady=10)

ly = tk.Label(text="as\t Y", font=("Times New Roman", 10, "bold"))
ly.grid(row=5, column=1, padx=10, pady=10)

ez = tk.StringVar()
ez = tk.Entry(root, textvariable="z", width=30)
ez.grid(row=6, column=0, padx=10, pady=10)

lz = tk.Label(text="as\t Z", font=("Times New Roman", 10, "bold"))
lz.grid(row=6, column=1, padx=10, pady=10)


root.mainloop()
