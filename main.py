# -*- coding: utf-8 -*-
import threading
import time
from pynput import keyboard
import pyautogui
import tkinter as tk
from tkinter import messagebox, simpledialog

# Variáveis globais
is_clicking = False
activation_key = "Delete"  # Tecla padrão para ativação/desativação
click_duration = None  # Duração definida pelo usuário (None para ilimitado)
waiting_for_key = False  # Controle para detectar nova tecla

# Função para simular o clique contínuo
def hold_left_click():
    start_time = time.time()
    while is_clicking:
        pyautogui.mouseDown()
        time.sleep(0.1)  # Pequena pausa para evitar uso excessivo de CPU
        if click_duration and time.time() - start_time >= click_duration:
            stop_clicking()
            break

# Função para ativar/desativar o clique
def toggle_click():
    global is_clicking
    is_clicking = not is_clicking
    update_status()
    if is_clicking:
        threading.Thread(target=hold_left_click, daemon=True).start()

# Função para parar o clique
def stop_clicking():
    global is_clicking
    is_clicking = False
    pyautogui.mouseUp()
    update_status()

# Função para atualizar o status na interface
def update_status():
    status_label.config(text=f"Status: {'Ativado' if is_clicking else 'Desativado'}")

# Função para exibir informações
def show_info():
    messagebox.showinfo("Informação", "Use a tecla configurada ou o botão no menu para ativar/desativar o clique contínuo.")

# Função para configurar a tecla de ativação
def set_activation_key():
    global waiting_for_key
    waiting_for_key = True
    messagebox.showinfo("Configuração", "Pressione a tecla que deseja configurar como tecla de ativação.")

# Função para configurar a duração do clique
def set_click_duration():
    global click_duration
    duration = simpledialog.askinteger("Configurar Duração", "Digite a duração em segundos (0 para ilimitado):")
    if duration is not None:
        click_duration = duration if duration > 0 else None
        messagebox.showinfo("Configuração", f"Duração configurada para: {'ilimitada' if click_duration is None else f'{click_duration} segundos'}")

# Função para sair do programa
def exit_program():
    stop_clicking()
    root.destroy()

# Listener para detectar a tecla configurada ou alternar o clique
def on_press(key):
    global activation_key, waiting_for_key
    try:
        key_name = key.char if hasattr(key, 'char') and key.char else key.name
        if waiting_for_key:
            activation_key = key_name
            waiting_for_key = False
            messagebox.showinfo("Configuração", f"Tecla de ativação alterada para: {activation_key}")
        elif key_name == activation_key:
            toggle_click()
    except AttributeError:
        pass

# Configuração da interface gráfica
root = tk.Tk()
root.title("Auto Clicker")
root.geometry("400x300")
root.resizable(False, False)

# Elementos da interface gráfica
status_label = tk.Label(root, text="Status: Desativado", font=("Arial", 14))
status_label.pack(pady=20)

frame = tk.Frame(root)
frame.pack(pady=10)

toggle_button = tk.Button(frame, text="Ativar/Desativar Clique", command=toggle_click, font=("Arial", 12), width=20)
toggle_button.grid(row=0, column=0, padx=10, pady=5)

info_button = tk.Button(frame, text="Informação", command=show_info, font=("Arial", 12), width=20)
info_button.grid(row=1, column=0, padx=10, pady=5)

config_key_button = tk.Button(frame, text="Configurar Tecla", command=set_activation_key, font=("Arial", 12), width=20)
config_key_button.grid(row=2, column=0, padx=10, pady=5)

config_duration_button = tk.Button(frame, text="Configurar Duração", command=set_click_duration, font=("Arial", 12), width=20)
config_duration_button.grid(row=3, column=0, padx=10, pady=5)

exit_button = tk.Button(root, text="Sair", command=exit_program, font=("Arial", 12), width=20)
exit_button.pack(pady=10)

# Inicia o listener do teclado em uma thread separada
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Loop principal da interface gráfica
root.mainloop()

# Garante que o listener pare ao sair do programa
listener.stop()