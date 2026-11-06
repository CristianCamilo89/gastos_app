"""Punto de entrada de la app de control de gastos (Kivy + SQLite)."""
import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import platform

# Importar las clases las registra para poder usarlas desde los archivos .kv
from database.db import Database
from screens.add_transaction import AddTransactionScreen  # noqa: F401
from screens.dashboard import DashboardScreen              # noqa: F401
from screens.summary import SummaryScreen                  # noqa: F401
from screens.widgets import TransactionItem                # noqa: F401

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KV_FILES = ["common.kv", "dashboard.kv", "add_transaction.kv", "summary.kv", "main.kv"]

# Tamaño de ventana solo para probar en PC (en el celular se ignora)
if platform in ("win", "linux", "macosx"):
    Window.size = (400, 780)
Window.softinput_mode = "below_target"  # el teclado no tapa el campo activo


class GastosApp(App):
    """Aplicación principal."""
    title = "Mis Gastos"

    def build(self):
        """Crea la BD, pide permisos en Android y construye la interfaz."""
        # user_data_dir es una carpeta privada y persistente en cada plataforma
        self.db = Database(os.path.join(self.user_data_dir, "gastos.db"))

        if platform == "android":
            from android.permissions import Permission, request_permissions  # type: ignore
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                                 Permission.READ_EXTERNAL_STORAGE])

        root = None
        for name in KV_FILES:
            loaded = Builder.load_file(os.path.join(BASE_DIR, "kv", name))
            root = loaded or root   # solo main.kv devuelve un widget raíz
        return root


if __name__ == "__main__":
    GastosApp().run()
