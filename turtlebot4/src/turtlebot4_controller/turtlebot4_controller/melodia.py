import numpy as np
import simpleaudio as sa
import time

# Definir las frecuencias de las notas
A = 440.0
Bb = 466.16
B = 493.88
C = 523.25
Db = 554.37
D = 587.33
Eb = 622.25
E = 659.25
F = 698.46
Gb = 739.99
G = 783.99
Ab = 830.61
A_high = 880.0

# Definir la duración de las notas en segundos
whole = 1.0
half = 0.5
quarter = 0.25
eighth = 0.125

# Función para reproducir una nota
def play_tone(frequency, duration):
    fs = 44100  # Frecuencia de muestreo
    t = np.linspace(0, duration, int(fs * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    audio = wave * (2**15 - 1) / np.max(np.abs(wave))
    audio = audio.astype(np.int16)
    play_obj = sa.play_buffer(audio, 1, 2, fs)
    play_obj.wait_done()

# Lista de notas y duraciones para la melodía completa
melody = [
    (A, quarter), (A, quarter), (F, eighth), (C, eighth), (A, quarter), (F, eighth), (C, eighth), (A, half),
    (E, quarter), (E, quarter), (E, quarter), (F, eighth), (C, eighth), (G, quarter), (F, eighth), (C, eighth), (A, half),
    (A_high, quarter), (A, eighth), (A, eighth), (A_high, quarter), (Ab, eighth), (G, eighth), (Gb, eighth), (F, eighth), (Gb, eighth),
    (Ab, eighth), (A, quarter), (F, eighth), (A, quarter), (C, eighth), (E, quarter), (C, eighth), (E, quarter), (A_high, eighth),
    (A, eighth), (A_high, quarter), (Ab, eighth), (G, eighth), (Gb, eighth), (F, eighth), (Gb, eighth), (Ab, eighth),
    (A, quarter), (F, eighth), (A, quarter), (C, eighth), (E, quarter), (C, eighth), (E, quarter), (A, half)
]

# Reproducir la melodía
for note, duration in melody:
    play_tone(note, duration)
    time.sleep(0.10)  # Pausa corta entre notas para un mejor efecto

print("Melodía terminada.")
