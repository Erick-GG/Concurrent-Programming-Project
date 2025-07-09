import os
import re
import pytesseract
import cv2
import json
import multiprocessing
from collections import defaultdict
from fpdf import FPDF


# Asegurence que el path a tesseract este bien(tiene que ser el path donde se instalo tesseract),
# la libreria nomas es un wrapper
# https://github.com/UB-Mannheim/tesseract/wiki
# Info/tuto de tesseract
# https://nanonets.com/blog/ocr-with-tesseract/
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\erikg\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
CATEGORIAS = {
    "alimentos": ["pan", "tortilla", "refresco", "galleta", "pollo", "coca", "comida"],
    "hogar": ["foco", "cloro", "trapeador", "servilleta", "detergente"],
    "transporte": ["gasolina", "uber", "litros", "combustible"],
    "otros": []
}

def clasificar_producto(nombre):
    nombre = nombre.lower()
    for categoria, palabras in CATEGORIAS.items():
        if any(palabra in nombre for palabra in palabras):
            return categoria
    return "otros"

def procesar_ticket(path_imagen):
    try:
        imagen = cv2.imread(path_imagen)
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        _, binaria = cv2.threshold(gris, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        texto = pytesseract.image_to_string(binaria)
        lineas = texto.splitlines()

        ticket = {
            "archivo": os.path.basename(path_imagen),
            "total": 0.0,
            "productos": []
        }

        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue

            # Buscar total
            if re.search(r"total", linea, re.IGNORECASE):
                numeros = re.findall(r"\d+[.,]?\d*", linea)
                if numeros:
                    ticket["total"] = float(numeros[-1].replace(",", "."))

            # Buscar productos con formato simple: nombre cantidad precio
            match = re.match(r"([\w\s]+)\s+(\d+)\s+(\d+[.,]?\d*)", linea)
            if match:
                nombre = match.group(1).strip()
                cantidad = int(match.group(2))
                precio_unit = float(match.group(3).replace(",", "."))
                categoria = clasificar_producto(nombre)
                ticket["productos"].append({
                    "nombre": nombre,
                    "cantidad": cantidad,
                    "precio_unitario": precio_unit,
                    "categoria": categoria
                })

        return ticket
    except Exception as e:
        return {"error": str(e), "archivo": os.path.basename(path_imagen)}

def generar_reporte_pdf(tickets, salida_pdf):
    resumen = defaultdict(float)
    total_gastos = 0.0

    for ticket in tickets:
        if "productos" not in ticket:
            continue
        for prod in ticket["productos"]:
            subtotal = prod["cantidad"] * prod["precio_unitario"]
            resumen[prod["categoria"]] += subtotal
            total_gastos += subtotal

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, text="Reporte de gastos por categoria", ln=True, align='C')
    pdf.ln(10)
    for cat, total in resumen.items():
        pdf.cell(200, 10, txt=f"{cat.capitalize()}: ${total:.2f}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Gasto total: ${total_gastos:.2f}", ln=True)
    pdf.output(salida_pdf)


def main():
    carpeta_tickets = input("Ingresa el path a la carpeta con los tickets: ").strip()
    carpeta_salida = input("Ingresa el path de salida para el PDF generado: ").strip()

    archivos = [os.path.join(carpeta_tickets, f) for f in os.listdir(carpeta_tickets) if f.lower().endswith((".jpg", ".png", ".jpeg"))]

    print(f"Procesando {len(archivos)} tickets...")
    with multiprocessing.Pool() as pool:
        resultados = pool.map(procesar_ticket, archivos)

    os.makedirs(os.path.join(carpeta_salida, "jsons"), exist_ok=True)
    for ticket in resultados:
        if "archivo" in ticket:
            nombre_json = ticket["archivo"].rsplit(".", 1)[0] + ".json"
            with open(os.path.join(carpeta_salida, "jsons", nombre_json), "w", encoding="utf-8") as f:
                json.dump(ticket, f, indent=2, ensure_ascii=False)

    generar_reporte_pdf(resultados, os.path.join(carpeta_salida, "reporte_gastos.pdf"))
    print("Procesamiento terminado. Se ha generado un PDf y JSONs.")

if __name__ == "__main__":
    main()
