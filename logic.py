
#Imports para el boton
from PIL import Image, ImageTk
from pathlib import Path
# Imports para todo lo demas

# Toda esta mamada es para que el boton de la carpeta este transparente asi que esto no le muevan
#
#
#
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\kv901\OneDrive\Desktop\LectorOCR\build\assets\frame0")

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


# Ya que aqui ahora si va la logica