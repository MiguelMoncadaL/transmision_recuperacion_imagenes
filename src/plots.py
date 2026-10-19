"""Gráficas del análisis: perfil de una fila, histograma y curvas de PSNR."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.analysis import row_profile
from src.image_io import to_gray


def _finish(fig, save_path, show):
    plt.tight_layout()
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=120)
    if show:
        plt.show()
    plt.close(fig)


def plot_row_profile(original, received, row=None, window=60,
                     label_received="Recibida", save_path=None, show=True):
    """Compara una fila de la imagen original y de la recibida como señales 1D.

    Arriba: la fila completa. Abajo: una ventana de `window` muestras para
    ver el efecto del ruido muestra a muestra.
    """
    x0, fila = row_profile(original, row)
    xr, _ = row_profile(received, fila)
    n = np.arange(len(x0))
    centro = len(x0) // 2
    ini, fin = max(0, centro - window // 2), min(len(x0), centro + window // 2)

    fig, axes = plt.subplots(2, 1, figsize=(11, 7))
    axes[0].plot(n, x0, label="Original", linewidth=1.2)
    axes[0].plot(n, xr, label=label_received, linewidth=0.8, alpha=0.8)
    axes[0].set_title(f"Perfil de intensidad de la fila {fila}")
    axes[0].set_xlabel("Posición horizontal n (píxeles)")
    axes[0].set_ylabel("Intensidad (0-255)")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    axes[1].plot(n[ini:fin], x0[ini:fin], "o-", markersize=3, label="Original")
    axes[1].plot(n[ini:fin], xr[ini:fin], "s-", markersize=3, label=label_received)
    axes[1].set_title(f"Ventana de {fin - ini} muestras (columnas {ini} a {fin - 1})")
    axes[1].set_xlabel("Posición horizontal n (píxeles)")
    axes[1].set_ylabel("Intensidad (0-255)")
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    _finish(fig, save_path, show)


def plot_histogram(original, received, label_received="Recibida",
                   save_path=None, show=True):
    """Histograma de intensidades de la original y la recibida."""
    g0, gr = to_gray(original), to_gray(received)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.hist(g0.ravel(), bins=64, range=(0, 256), alpha=0.6, label="Original")
    ax.hist(gr.ravel(), bins=64, range=(0, 256), alpha=0.6, label=label_received)
    ax.set_title("Histograma de intensidades")
    ax.set_xlabel("Nivel de intensidad (0-255)")
    ax.set_ylabel("Número de muestras (píxeles)")
    ax.legend()
    ax.grid(alpha=0.3)
    _finish(fig, save_path, show)


def plot_metric_curve(x, curves, xlabel, title, save_path=None, show=True,
                      log_x=False):
    """Curvas de métricas (en dB) frente a un parámetro del canal.

    curves: lista de (etiqueta, valores, estilo).
    """
    fig, ax = plt.subplots(figsize=(8, 4.8))
    for etiqueta, valores, estilo in curves:
        ax.plot(x, valores, estilo, label=etiqueta)
    if log_x:
        ax.set_xscale("log")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Calidad (dB)")
    ax.legend()
    ax.grid(alpha=0.3)
    _finish(fig, save_path, show)
