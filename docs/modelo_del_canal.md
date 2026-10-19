# Representación de la imagen y modelo del canal

## 1. La imagen como señal

Una imagen en escala de grises es una señal bidimensional discreta `f[m, n]`:

- **Muestreo espacial:** cada píxel es una muestra tomada en la posición (fila `m`, columna `n`).
  La resolución (por ejemplo 512 x 512) indica cuántas muestras hay por dimensión. En una
  imagen no existe una frecuencia de muestreo en Hz, pero el equivalente es la densidad de
  píxeles.
- **Cuantización:** cada muestra se guarda con 8 bits, es decir, 256 niveles posibles (0 = negro,
  255 = blanco). Se almacena como `uint8` en un arreglo de NumPy.
- **Color:** una imagen RGB tiene tres señales (canales rojo, verde y azul) y su arreglo tiene
  forma `(alto, ancho, 3)`.
- **Cantidad de información:** `alto x ancho x canales x 8` bits. Una imagen de 512 x 512 en
  grises tiene 2 097 152 bits.

## 2. Esquema del sistema

```
imagen (arreglo)  ->  [canal con ruido]  ->  imagen recibida  ->  comparación / métricas
                                                  (la recuperación se agregará en la siguiente entrega)
```

## 3. Modelos de canal implementados (`src/channel.py`)

| Canal | Modelo | Parámetro |
|---|---|---|
| `awgn` | `y[m,n] = x[m,n] + w[m,n]`, con `w ~ N(0, sigma^2)`, luego se recorta a [0, 255] | `sigma` |
| `salt_pepper` | Con probabilidad `prob` el píxel se reemplaza por 0 o 255 (mitad y mitad) | `prob` |
| `bsc` | La imagen se convierte en bits; cada bit se invierte con probabilidad `p`; se reconstruye la imagen | `p` |

El canal `bsc` es el más cercano a una transmisión digital real: modela errores de bit, y un
error en un bit de mayor peso (por ejemplo el bit 7, que vale 128) cambia mucho más el valor
del píxel que un error en el bit menos significativo (que vale 1).

## 4. Métricas (`src/metrics.py`)

Sea `x` la imagen original, `y` la recibida y `N` el número de muestras.

- **MSE** = (1/N) * suma((x - y)^2)
- **PSNR** (dB) = 10 * log10(255^2 / MSE). Mayor es mejor.
- **SNR** (dB) = 10 * log10(potencia de x / MSE). Mayor es mejor.
- **BER** = fracción de bits recibidos con error (función `bit_error_rate`).

## 5. Verificación con la teoría

- **AWGN:** si no hubiera recorte, el MSE sería sigma^2 y por tanto PSNR = 20 log10(255 / sigma).
  Para sigma = 25 daría 20.17 dB; se midió 20.58 dB. La diferencia se debe al recorte a [0, 255],
  que reduce el error efectivo.
- **BSC:** un error en el bit `k` cambia el valor en 2^k, así que
  MSE esperado = p * suma(4^k, k = 0..7) = p * (4^8 - 1) / 3. Para p = 0.01 da 218.45
  (PSNR = 24.74 dB); se midió 216.51 (24.78 dB).

## 6. Pendiente

Análisis frecuencial (transformada de Fourier) y etapa de recuperación (filtros y/o corrección
de errores): se incorporarán conforme se vean en la asignatura.
