
#Imports para el boton
from PIL import Image, ImageTk
from pathlib import Path
from tkinter import messagebox, filedialog
import os, sys
from OCR_MVP.backend import main
# Imports para todo lo demas

# Variables globales para rutas
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

carpeta_salida = os.path.join(BASE_DIR, "output")
os.makedirs(carpeta_salida, exist_ok=True)

# Toda esta mamada es para que el boton de la carpeta este transparente asi que esto no le muevan
#
#
#
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\kv901\OneDrive\Desktop\LectorOCR\build\assets\frame0")
entry_ref = None  # será asignado desde gui.py
def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

class cargarboton :
    
    def create_button_with_background():
        button_img = Image.open(relative_to_assets("botonsote.png"))
    
        bg_color = (19, 90, 74)
        background = Image.new('RGB', button_img.size, bg_color)
    
        if button_img.mode == 'RGBA':
            background.paste(button_img, (0, 0), button_img)
        else:
            background.paste(button_img, (0, 0))
    
        return ImageTk.PhotoImage(background)


class seleccionarCarpeta:
    def __init__(self, entry_widget):
        self.entry = entry_widget
        self.carpeta_tickets = ""
        self.carpeta_salida = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(self.carpeta_salida, exist_ok=True)

    def seleccionar_carpeta_tickets(self):
        carpeta = filedialog.askdirectory(title="Selecciona la carpeta con los tickets")
        if carpeta:
            self.carpeta_tickets = carpeta
            self.entry.delete(0, 'end')
            self.entry.insert(0, carpeta)

    def ejecutar_procesamiento(self):
        if not self.carpeta_tickets:
            messagebox.showerror("Error", "Debes seleccionar una carpeta con los tickets.")
            return
        try:
            main(self.carpeta_tickets, self.carpeta_salida)
            messagebox.showinfo("Éxito", f"PDF y JSONs guardados en:\n{self.carpeta_salida}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")