"""Utilidades de interfaz reutilizables."""
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.popup import Popup


def show_message(title: str, text: str) -> None:
    """Muestra una ventana emergente simple con un mensaje."""
    label = Label(text=text, halign="center", valign="middle", color=(1, 1, 1, 1))
    label.bind(size=lambda inst, size: setattr(inst, "text_size", size))
    popup = Popup(title=title, content=label, size_hint=(0.85, None), height=dp(220))
    popup.open()
