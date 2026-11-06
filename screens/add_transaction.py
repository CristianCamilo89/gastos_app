"""Pantalla para registrar un gasto o ingreso."""
from datetime import datetime

from kivy.app import App
from kivy.properties import ListProperty, StringProperty
from kivy.uix.screenmanager import Screen
from utils.constants import CATEGORIES, KINDS, PAYMENT_METHODS
from utils.ui import show_message


class AddTransactionScreen(Screen):
    """Formulario de alta de movimientos."""
    categories = ListProperty(CATEGORIES)
    methods = ListProperty(PAYMENT_METHODS)
    kinds = ListProperty(KINDS)
    title_text = StringProperty("Nuevo movimiento")
    editing_id = None # None= creando uno nuevo; un numero = editando ese id

    def on_pre_enter(self, *args):
        """Si la fecha está vacía, la rellena con la fecha de hoy."""
        if not self.ids.date.text:
            self.ids.date.text = datetime.now().strftime("%Y-%m-%d")

    def load_for_edit(self, tx_id):
        """Rellena el formulario con los datos de un movimiento existente. """
        row = App.get_running_app().db.get_transaction(tx_id)
        if row is None:
            return
        self.editing_id = tx_id
        self.title_text = "Editar movimiento"
        self.ids.kind.text = row["kind"].capitalize()
        self.ids.description.text = str(row["amount"])
        self.ids.category.text = row["date"]
        self.ids.method.text = row["payment_method"]
    def on_leave(self, *args):
        """Al salir de la pantalla sin guardar, limpia el modo edicion. """
        self._reset_form()

    def save(self):
        """Valida los campos, guarda en SQLite y vuelve al dashboard."""
        ids = self.ids
        description = ids.description.text.strip()

        # Validación del monto
        try:
            amount = float(ids.amount.text.replace(",", "."))
            if amount <= 0:
                raise ValueError
        except ValueError:
            show_message("Dato inválido", "Ingresa un monto mayor que 0.")
            return

        # Validación de la descripción
        if not description:
            show_message("Dato inválido", "Escribe una descripción.")
            return

        # Validación de la fecha
        try:
            datetime.strptime(ids.date.text.strip(), "%Y-%m-%d")
        except ValueError:
            show_message("Dato inválido", "La fecha debe tener formato AAAA-MM-DD.")
            return
        data = dict(
            description=description,
            amount=amount,
            kind=ids.kind.text.lower(),
            category=ids.category.text,
            date=ids.date.text.strip(),
            payment_method=ids.method.text,
        )
        db = App.get_running_app().db
        if self.editing_id is None:
            db.add_transaction(**data)
        else:
            db.update_transaction(self.editing_id, **data)
            
        self._reset_form()
        self.manager.current = "dashboard"

    def _reset_form(self):
        """Limpia el formulario para el siguiente registro."""
        self.ids.description.text = ""
        self.ids.amount.text = ""
        self.ids.date.text = ""
        self.editing_id = None
        self.title_text = "Nuevo movimiento"
