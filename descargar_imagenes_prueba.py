import os
import requests
import subprocess

# Carpeta donde guardar las imágenes
IMG_DIR = "Imagen"
AUDIO_DIR = "audio"

# Crear carpetas si no existen
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# Lista de imágenes a descargar (nombre, tamaño deseado)
imagenes = [
    ("linea_tiempo.jpg", (800, 400)),
    ("despiece.jpg", (800, 400)),
    ("monedas.jpg", (800, 400)),
    ("interruptores.jpg", (800, 400)),
    ("circuito.jpg", (800, 400)),
    ("mapa_eps.jpg", (800, 400)),
    ("ensamblaje.jpg", (800, 400))
]

# Descargar imágenes desde picsum.photos (imágenes reales aleatorias)
for nombre, size in imagenes:
    ruta = os.path.join(IMG_DIR, nombre)
    if os.path.exists(ruta):
        print(f"⏭️  {nombre} ya existe, saltando.")
        continue
    width, height = size
    url = f"https://picsum.photos/{width}/{height}?random={hash(nombre)}"
    print(f"📥 Descargando {nombre}...")
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(ruta, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"✅ {nombre} descargado.")
        else:
            print(f"❌ Error al descargar {nombre}: {response.status_code}")
    except Exception as e:
        print(f"❌ Error con {nombre}: {e}")

# Crear audios de prueba (silencios de 5 segundos) usando ffmpeg si está instalado
# Si no tienes ffmpeg, puedes omitir esta parte y luego subir tus propios audios.
audios = [
    "linea_tiempo.mp3",
    "eps.mp3",
    "calculadora_humana.mp3"
]

for audio in audios:
    ruta = os.path.join(AUDIO_DIR, audio)
    if os.path.exists(ruta):
        print(f"⏭️  {audio} ya existe, saltando.")
        continue
    print(f"🎵 Generando {audio} (audio silencioso)...")
    # Generar 5 segundos de silencio usando ffmpeg (si está disponible)
    # Si no, dejamos que el usuario lo añada manualmente.
    try:
        subprocess.run([
            "ffmpeg", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
            "-t", "5", "-q:a", "9", "-acodec", "libmp3lame",
            ruta
        ], check=True, capture_output=True)
        print(f"✅ {audio} generado.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"⚠️  No se pudo generar {audio} porque ffmpeg no está instalado.")
        print("   Crea el archivo manualmente o instala ffmpeg.")

print("\n🎉 Proceso completado. Revisa las carpetas Imagen/ y audio/.")