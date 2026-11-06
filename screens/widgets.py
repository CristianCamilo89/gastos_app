"""Widgets personalizados reutilizables (su diseño está en kv/common.kv)."""
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout


class TransactionItem(ButtonBehavior, BoxLayout):
    """Fila de la lista de movimientos (se puede tocar)."""
    tx_id = NumericProperty(0)  # id del movimiento en la base de datos
    description = StringProperty("")
    subtitle = StringProperty("")
    amount_text = StringProperty("")
    amount_color = ListProperty([0, 0, 0, 1])
