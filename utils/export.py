"""Exportación de datos a CSV."""
import csv
import os
from datetime import datetime

from kivy.utils import platform


def get_export_dir(fallback_dir: str) -> str:
    """
    Devuelve la carpeta donde guardar el CSV.
    - Android: intenta la carpeta Download del almacenamiento externo.
    - Escritorio: la carpeta personal del usuario.
    - Si no se puede escribir, usa `fallback_dir`.
    """
    if platform == "android":
        try:
            from android.storage import primary_external_storage_path  # type: ignore

            folder = os.path.join(primary_external_storage_path(), "Download")
            if os.path.isdir(folder) and os.access(folder, os.W_OK):
                return folder
        except Exception:
            pass
    elif platform in ("win", "linux", "macosx"):
        return os.path.expanduser("~")
    return fallback_dir


def export_csv(rows, folder: str) -> str:
    """
    Escribe todos los movimientos en un CSV y devuelve la ruta del archivo.
    Usa utf-8-sig para que Excel abra bien las tildes.
    """
    os.makedirs(folder, exist_ok=True)
    name = f"gastos_{datetime.now():%Y%m%d_%H%M%S}.csv"
    path = os.path.join(folder, name)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Fecha", "Tipo", "Descripción", "Categoría", "Método de pago", "Monto"])
        for r in rows:
            writer.writerow([r["id"], r["date"], r["kind"], r["description"],
                             r["category"], r["payment_method"], f'{r["amount"]:.2f}'])
    return path
