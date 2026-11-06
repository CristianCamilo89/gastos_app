"""Pantalla de resumen: gráfica de gastos por categoría y exportación a CSV."""
import os
from datetime import datetime

from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen

from utils.charts import build_category_chart
from utils.constants import MONTH_NAMES
from utils.export import export_csv, get_export_dir
from utils.formatters import money
from utils.ui import show_message


class SummaryScreen(Screen):
    """Gráfica mensual de gastos por categoría y botón de exportar."""
    month_text = StringProperty("")
    total_text = StringProperty("")

    def __init__(self, **kwargs):
        """Inicia en el mes actual."""
        super().__init__(**kwargs)
        now = datetime.now()
        self.year, self.month = now.year, now.month

    def on_pre_enter(self, *args):
        """Refresca la gráfica al entrar a la pantalla."""
        self.refresh()

    def change_month(self, delta: int):
        """Avanza (+1) o retrocede (-1) un mes y vuelve a dibujar."""
        self.month += delta
        if self.month > 12:
            self.month, self.year = 1, self.year + 1
        elif self.month < 1:
            self.month, self.year = 12, self.year - 1
        self.refresh()

    def refresh(self):
        """Carga los datos del mes y dibuja la gráfica (matplotlib o Kivy nativo)."""
        app = App.get_running_app()
        title = f"{MONTH_NAMES[self.month - 1]} {self.year}"
        self.month_text = title

        data = app.db.expenses_by_category(self.year, self.month)
        self.total_text = "Total gastos: " + money(sum(v for _, v in data))

        box = self.ids.chart_box
        box.clear_widgets()
        if not data:
            box.add_widget(Label(text="Sin gastos registrados en este mes"))
            return

        chart_path = os.path.join(app.user_data_dir, "chart.png")
        if build_category_chart(data, chart_path, f"Gastos por categoría - {title}"):
            box.add_widget(Image(source=chart_path, nocache=True))
        else:
            self._native_chart(box, data)

    def _native_chart(self, box, data):
        """Gráfica de respaldo (sin matplotlib): barras de progreso de Kivy."""
        biggest = max(v for _, v in data)
        for category, total in data:
            row = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(8))
            row.add_widget(Label(text=category, size_hint_x=0.3))
            row.add_widget(ProgressBar(max=biggest, value=total))
            row.add_widget(Label(text=money(total), size_hint_x=0.3))
            box.add_widget(row)

    def export(self):
        """Exporta todos los movimientos a un CSV e informa la ruta."""
        app = App.get_running_app()
        rows = app.db.all_transactions()
        if not rows:
            show_message("Exportar", "No hay movimientos para exportar.")
            return
        try:
            folder = get_export_dir(app.user_data_dir)
            path = export_csv(rows, folder)
            show_message("Exportación lista", f"Archivo guardado en:\n{path}")
        except Exception as exc:
            show_message("Error", f"No se pudo exportar:\n{exc}")
