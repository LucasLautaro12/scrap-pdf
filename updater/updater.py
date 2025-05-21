import os
import shutil
import tempfile
import zipfile
import requests

REPO_ZIP_URL = "https://github.com/usuario/repositorio/archive/refs/heads/main.zip"  # Cambia esto
NOMBRE_CARPETA_INTERNA = "repositorio-main"  # Carpeta raíz dentro del ZIP

def check_and_update():
    print("Verificando actualizaciones...")

    try:
        # Descargar ZIP
        print("Descargando última versión del repositorio...")
        response = requests.get(REPO_ZIP_URL)
        response.raise_for_status()

        # Extraer a carpeta temporal
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "update.zip")
            with open(zip_path, "wb") as f:
                f.write(response.content)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)

            carpeta_extraida = os.path.join(tmpdir, NOMBRE_CARPETA_INTERNA)

            # Ruta del programa actual
            app_path = os.path.dirname(os.path.dirname(__file__))

            # Copiar archivos reemplazando los actuales (excepto .git, updater.py, etc.)
            for root, dirs, files in os.walk(carpeta_extraida):
                rel_path = os.path.relpath(root, carpeta_extraida)
                dest_path = os.path.join(app_path, rel_path)

                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)

                for file in files:
                    if file == "updater.py":
                        continue  # no sobrescribas este archivo
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(dest_path, file)
                    shutil.copy2(src_file, dst_file)

            print("✅ Aplicación actualizada con éxito.")

    except Exception as e:
        print(f"❌ Error al actualizar: {e}")
