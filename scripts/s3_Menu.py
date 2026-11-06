import os
import boto3
from botocore.exceptions import ClientError

# Bucket donde trabaja el menu (por defecto el del sitio publico).
# Para usar el privado: set BUCKET_NAME=miguel-privado0
BUCKET_NAME = os.environ.get("BUCKET_NAME", "mi-sitio-miguel")

s3 = boto3.client("s3")


def subir():
    ruta = input("Ruta del archivo a subir: ").strip().strip('"')
    nombre = input("Nombre en el bucket (Enter = mismo nombre): ").strip()
    if not nombre:
        nombre = os.path.basename(ruta)
    try:
        s3.upload_file(ruta, BUCKET_NAME, nombre)
        print(f"✅ Subido: {nombre}")
    except (ClientError, FileNotFoundError) as e:
        print(f"❌ Error: {e}")


def descargar():
    nombre = input("Nombre del archivo en el bucket: ").strip()
    destino = input("Guardar como (Enter = mismo nombre): ").strip() or os.path.basename(nombre)
    try:
        s3.download_file(BUCKET_NAME, nombre, destino)
        print(f"✅ Descargado en: {destino}")
    except ClientError as e:
        print(f"❌ Error: {e}")


def eliminar():
    nombre = input("Nombre del archivo a eliminar: ").strip()
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=nombre)
        print(f"🗑️ Eliminado: {nombre}")
    except ClientError as e:
        print(f"❌ Error: {e}")


def listar():
    try:
        resp = s3.list_objects_v2(Bucket=BUCKET_NAME)
        items = resp.get("Contents", [])
        if not items:
            print("📂 El bucket está vacío")
        for obj in items:
            print(f" - {obj['Key']} ({obj['Size']} bytes)")
    except ClientError as e:
        print(f"❌ Error: {e}")


def menu():
    opciones = {"1": subir, "2": descargar, "3": eliminar, "4": listar}
    while True:
        print(f"\n=== Menú S3 ({BUCKET_NAME}) ===")
        print("1. Subir archivo")
        print("2. Descargar archivo")
        print("3. Eliminar archivo")
        print("4. Listar archivos")
        print("5. Salir")
        op = input("Elige una opción: ").strip()
        if op == "5":
            print("👋 Hasta luego")
            break
        accion = opciones.get(op)
        if accion:
            accion()
        else:
            print("Opción no válida")


if __name__ == "__main__":
    menu()
