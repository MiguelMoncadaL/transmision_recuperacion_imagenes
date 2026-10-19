"""Genera, de forma reproducible, las figuras y tablas de results/ que se
muestran en el README. Usa semilla fija, así que siempre da lo mismo.

    python generar_resultados.py
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # no abrir ventanas

import numpy as np

from src.analysis import noise_statistics
from src.channel import transmit
from src.image_io import load_image, show_comparison
from src.metrics import evaluate, psnr, snr
from src.plots import plot_histogram, plot_metric_curve, plot_row_profile

SEMILLA = 42
SALIDA = Path("results")

# Imágenes usadas en los resultados (cámbialas si usan otras)
IMAGEN_GRISES = Path("data/reloj.jpg")   # se procesa en escala de grises
IMAGEN_COLOR = Path("data/casa.jpeg")     # se procesa a color (RGB)

# Parámetros del canal usados en los resultados (quedan documentados aquí y en el README)
CANALES = [
    ("awgn", 25.0, "Ruido gaussiano (AWGN), sigma = 25"),
    ("salt_pepper", 0.05, "Ruido sal y pimienta, prob = 0.05"),
    ("bsc", 0.01, "Canal binario simétrico, p = 0.01"),
]


def fila_de_metricas(nombre, canal, param, original, recibida):
    """Calcula las métricas y las estadísticas del error de una transmisión."""
    m = evaluate(original, recibida)
    e = noise_statistics(original, recibida)
    return [nombre, canal, param, round(m["MSE"], 2),
            round(m["PSNR (dB)"], 2), round(m["SNR (dB)"], 2),
            round(e["Media del error"], 2),
            round(e["Desviación estándar del error"], 2),
            round(e["Porcentaje de muestras alteradas"], 2)]


def resultados_principales():
    """Una imagen en grises por los tres canales + una imagen a color."""
    filas = []
    gris = load_image(IMAGEN_GRISES, grayscale=True)
    nombre_gris = IMAGEN_GRISES.stem
    for canal, param, etiqueta in CANALES:
        rx = transmit(gris, channel=canal, param=param, seed=SEMILLA)
        base = f"{nombre_gris}_{canal}"
        show_comparison(gris, rx, etiqueta, SALIDA / f"{base}_comparacion.png", show=False)
        if canal == "awgn":
            plot_row_profile(gris, rx, label_received=etiqueta,
                             save_path=SALIDA / f"{base}_perfil_fila.png", show=False)
            plot_histogram(gris, rx, label_received=etiqueta,
                           save_path=SALIDA / f"{base}_histograma.png", show=False)
        filas.append(fila_de_metricas(f"{nombre_gris} (grises)", canal, param, gris, rx))

    color = load_image(IMAGEN_COLOR)
    nombre_color = IMAGEN_COLOR.stem
    canal, param, etiqueta = CANALES[0]
    rx = transmit(color, channel=canal, param=param, seed=SEMILLA)
    show_comparison(color, rx, etiqueta, SALIDA / f"{nombre_color}_awgn_comparacion.png", show=False)
    filas.append(fila_de_metricas(f"{nombre_color} (color)", canal, param, color, rx))

    with open(SALIDA / "metricas.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["imagen", "canal", "parametro", "MSE", "PSNR_dB", "SNR_dB",
                    "media_error", "desv_error", "pct_alteradas"])
        w.writerows(filas)
    return filas


def barrido_awgn():
    """PSNR y SNR en función de sigma, junto con el valor teórico aproximado
    PSNR = 20 log10(255 / sigma) (válido si no hay recorte de valores)."""
    gris = load_image(IMAGEN_GRISES, grayscale=True)
    sigmas = np.array([5, 10, 15, 20, 25, 30, 40, 50, 60])
    p, s = [], []
    for sg in sigmas:
        rx = transmit(gris, channel="awgn", param=float(sg), seed=SEMILLA)
        p.append(psnr(gris, rx))
        s.append(snr(gris, rx))
    teorico = 20 * np.log10(255 / sigmas)
    plot_metric_curve(
        sigmas,
        [("PSNR medida", p, "o-"), ("SNR medida", s, "s-"),
         ("PSNR teórica 20·log10(255/sigma)", teorico, "k--")],
        "Desviación estándar del ruido sigma (niveles de intensidad)",
        f"Calidad de la imagen recibida vs. nivel de ruido AWGN ({IMAGEN_GRISES.stem})",
        save_path=SALIDA / "psnr_vs_sigma.png", show=False)


def barrido_bsc():
    """PSNR en función de la probabilidad de error de bit p, con el valor
    teórico PSNR = 10 log10(255^2 / (p (4^8 - 1) / 3))."""
    gris = load_image(IMAGEN_GRISES, grayscale=True)
    ps = np.array([0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05])
    medida = [psnr(gris, transmit(gris, "bsc", float(p), seed=SEMILLA)) for p in ps]
    teorico = 10 * np.log10(255 ** 2 / (ps * (4 ** 8 - 1) / 3))
    plot_metric_curve(
        ps,
        [("PSNR medida", medida, "o-"), ("PSNR teórica", teorico, "k--")],
        "Probabilidad de error de bit p (escala logarítmica en el eje x)",
        f"PSNR vs. probabilidad de error de bit en el canal binario ({IMAGEN_GRISES.stem})",
        save_path=SALIDA / "psnr_vs_ber.png", show=False, log_x=True)


if __name__ == "__main__":
    for ruta in (IMAGEN_GRISES, IMAGEN_COLOR):
        if not ruta.exists():
            sys.exit(f"No se encuentra la imagen '{ruta}'. "
                     "Revisa los nombres IMAGEN_GRISES e IMAGEN_COLOR al inicio de este archivo.")
    SALIDA.mkdir(exist_ok=True)
    for fila in resultados_principales():
        print(fila)
    barrido_awgn()
    barrido_bsc()
    print("Resultados guardados en results/")