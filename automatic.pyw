import tkinter as tk
from tkinter import simpledialog
from random import randint
import matplotlib.pyplot as plt
import time, sqlite3
import datetime

def cooldConvert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def perform_iteration():
    global pile, face, maxpile, maxface, npile, nface, console, iteration_task

    if randint(0, 1) == 0:
        info_label.config(text=f"Pile - Max Pile: {maxpile:,} - Max Face: {maxface:,}")
        face = 1
        pile += 1
        result_label.config(text=f"Temps : {cooldConvert(time.time() - startTime)}")
        if pile == console:
            info_label.after_cancel(iteration_task)
            conn = sqlite3.connect("result.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO results (type, time, quarter, console) VALUES (0, ?, ?, ?)", (time.time() - startTime, npile, console))
            conn.commit()
            conn.close()
            console += 1
            objectif.config(text=f"Objectif : {console:,}")
        if pile > maxpile:
            maxpile = pile
        if pile > console / 4 * 3:
            npile += 1
    else:
        info_label.config(text=f"Face - Max Pile: {maxpile:,} - Max Face: {maxface:,}")
        pile = 1
        face += 1
        result_label.config(text=f"Temps : {cooldConvert(time.time() - startTime)}")
        if face == console:
            info_label.after_cancel(iteration_task)
            conn = sqlite3.connect("result.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO results (type, time, quarter, console) VALUES (1, ?, ?, ?)", (time.time() - startTime, nface, console))
            conn.commit()
            conn.close()
            console += 1
            objectif.config(text=f"Objectif : {console:,}")
        if face > maxface:
            maxface = face
        if face > console / 4 * 3:
            nface += 1

    iteration_task = info_label.after(1, perform_iteration)

def start_iterations():
    global startTime, pile, face, maxpile, maxface, npile, nface, console
    pile = 0
    face = 0
    maxpile = 0
    maxface = 0
    npile = 0
    nface = 0
    startTime = time.time()
    modify_button.pack_forget()  # Cacher le bouton "Modifier console" s'il était affiché
    chance_label.config(text=f"{round((1 / 2 ** console) * 100, 10)}% de chance de réussite")
    result_label.config(text=f"Temps : {str(datetime.timedelta(seconds=int(round(time.time() - startTime))))}")
    objectif.config(text=f"Objectif : {console:,}")
    perform_iteration()
    start_button.config(text="Arrêter les itérations", command=stop_iterations)  # Changer le texte et la commande du bouton

def stop_iterations():
    global iteration_task
    info_label.after_cancel(iteration_task)
    modify_button.pack_forget()
    modify_button.pack(pady=10)
    start_button.config(text="Commencer les itérations", command=start_iterations)

# Demander à l'utilisateur la valeur de 'console'
root = tk.Tk()
root.withdraw()  # Cacher la fenêtre principale pour afficher uniquement la boîte de dialogue
console = simpledialog.askinteger("Valeur de 'console'", "Entrez la valeur de 'console':", initialvalue=5)
root.destroy()  # Fermer la fenêtre principale après avoir obtenu la valeur de 'console'

# Créer une nouvelle fenêtre tkinter (fenêtre principale)
root = tk.Tk()
root.title("Simulateur")
root.geometry("350x330")

objectif = tk.Label(root, text="", font=("Consolas", 12))
objectif.pack(pady=10)
chance_label = tk.Label(root, text="", font=("Consolas", 12))
chance_label.pack(pady=5)
info_label = tk.Label(root, text="", font=("Consolas", 12))
info_label.pack(pady=5)
result_label = tk.Label(root, text="", font=("Consolas", 12))
result_label.pack(pady=10)

start_button = tk.Button(root, text="Commencer les itérations", font=("Consolas", 12), command=start_iterations)
start_button.pack(pady=10)

modify_button = tk.Button(root, text="Modifier console", font=("Consolas", 12), command=lambda: modify_console(console))
modify_button.pack_forget()

def modify_console(old_value):
    global console
    # Ouvrir une boîte de dialogue pour permettre à l'utilisateur de modifier 'console'
    root.withdraw()
    new_value = simpledialog.askinteger("Value", "Entrez la nouvelle valeur de 'console':", initialvalue=old_value)
    if new_value is not None:  # Si l'utilisateur a saisi une nouvelle valeur et n'a pas annulé la boîte de dialogue
        console = new_value
    # modify_button.pack_forget()
    info_label.config(text="")
    objectif.config(text="")
    result_label.config(text="")
    chance_label.config(text="")
    start_button.config(text="Commencer les itérations", command=start_iterations)
    root.deiconify()

root.mainloop()