"""Transmisión de una imagen a través de un canal con ruido.

Carga una imagen, la caracteriza como señal, la envía por un canal ruidoso
simulado y compara la imagen recibida con la original (figuras y métricas).

Ejemplos:
    python main.py                       (se abre una ventana para elegir la imagen)
    python main.py --image data/cameraman.png --channel awgn --param 25
    python main.py --image foto.jpg --channel salt_pepper --param 0.08 --gray
    python main.py --image foto.png --channel bsc --param 0.01 --seed 1
    python main.py --prueba              (imagen sintética, sin elegir archivo)
"""
import argparse
from pathlib import Path

import numpy as np

from src.analysis import characterize, noise_statistics
from src.channel import transmit
from src.image_io import (choose_image_file, describe_image, load_image,
                          save_image, show_comparison)
from src.metrics import evaluate
from src.plots import plot_histogram, plot_row_profile

NOMBRES = {"awgn": "Ruido gaussiano (AWGN)",
           "salt_pepper": "Ruido sal y pimienta",
           "bsc": "Canal binario simétrico (errores de bit)"}


def imagen_de_prueba(size=256):
    """Imagen sintética para probar el sistema si no se indica ninguna."""
    y, x = np.mgrid[0:size, 0:size]
    img = (x + y) / (2 * size - 2) * 255
    img[size // 4: size // 2, size // 4: size // 2] = 255
    img[size // 2 + 20:, size // 2 + 20:] = 40
    return img.astype(np.uint8)


def imprimir(titulo, datos):
    print(f"\n{titulo}")
    for clave, valor in datos.items():
        texto = f"{valor:.2f}" if isinstance(valor, float) else valor
        print(f"  {clave}: {texto}")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--image", help="ruta de cualquier imagen (si se omite, se abre un selector de archivos)")
    parser.add_argument("--prueba", action="store_true", help="usar una imagen sintética de prueba")
    parser.add_argument("--channel", choices=NOMBRES.keys(), default="awgn")
    parser.add_argument("--param", type=float, default=None,
                        help="sigma (awgn), probabilidad (salt_pepper) o prob. de error de bit (bsc)")
    parser.add_argument("--gray", action="store_true", help="usar escala de grises")
    parser.add_argument("--seed", type=int, default=None, help="semilla para repetir resultados")
    parser.add_argument("--fila", type=int, default=None, help="fila para el perfil de intensidad (por defecto, la central)")
    parser.add_argument("--no-show", action="store_true", help="no abrir las ventanas de las figuras")
    args = parser.parse_args()

    if args.prueba:
        original = imagen_de_prueba()
        nombre = "prueba"
    else:
        ruta = args.image or choose_image_file()
        if not ruta:
            print("No se seleccionó ninguna imagen. Programa terminado.")
            return
        try:
            original = load_image(ruta, grayscale=args.gray)
        except Exception as error:
            print(f"No se pudo abrir la imagen '{ruta}': {error}")
            return
        nombre = Path(ruta).stem

    imprimir("Representación numérica de la imagen:", describe_image(original))
    imprimir("Caracterización de la señal original:", characterize(original))

    recibida = transmit(original, channel=args.channel, param=args.param, seed=args.seed)

    print(f"\nCanal: {NOMBRES[args.channel]} (parámetro: {args.param}, semilla: {args.seed})")
    imprimir("Estadísticas del error (recibida - original):", noise_statistics(original, recibida))
    imprimir("Métricas de calidad:", evaluate(original, recibida))

    salida = Path("results")
    base = f"{nombre}_{args.channel}"
    show = not args.no_show
    save_image(recibida, salida / f"{base}.png")
    show_comparison(original, recibida, title_received=NOMBRES[args.channel],
                    save_path=salida / f"{base}_comparacion.png", show=show)
    plot_row_profile(original, recibida, row=args.fila, label_received=NOMBRES[args.channel],
                     save_path=salida / f"{base}_perfil_fila.png", show=show)
    plot_histogram(original, recibida, label_received=NOMBRES[args.channel],
                   save_path=salida / f"{base}_histograma.png", show=show)
    print(f"\nFiguras guardadas en la carpeta '{salida}/'")


if __name__ == "__main__":
    main()
