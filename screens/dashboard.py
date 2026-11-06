"""Pantalla principal: balance del mes y últimos movimientos."""
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from screens.widgets import TransactionItem
from utils.constants import COLOR_EXPENSE, COLOR_INCOME, MONTH_NAMES
from utils.formatters import money


class DashboardScreen(Screen):
    """Muestra balance, ingresos vs gastos y la lista de últimos movimientos."""
    month_text = StringProperty("")
    balance_text = StringProperty("$0.00")
    income_text = StringProperty("$0.00")
    expense_text = StringProperty("$0.00")

    def on_pre_enter(self, *args):
        """Se ejecuta cada vez que se entra a la pantalla: refresca los datos."""
        Clock.schedule_once(lambda dt: self.refresh(), 0)

    def refresh(self):
        """Consulta la BD y actualiza los textos y la lista."""
        if "list_box" not in self.ids:
            return
        db = App.get_running_app().db
        now = datetime.now()
        income, expense = db.month_totals(now.year, now.month)

        self.month_text = f"{MONTH_NAMES[now.month - 1]} {now.year}"
        self.income_text = money(income)
        self.expense_text = money(expense)
        self.balance_text = money(income - expense)

        box = self.ids.list_box
        box.clear_widgets()
        for row in db.recent(20):
            is_income = row["kind"] == "ingreso"
            box.add_widget(TransactionItem(
                tx_id=row["id"],
                description=row["description"],
                subtitle=f'{row["date"]} · {row["category"]} · {row["payment_method"]}',
                amount_text=("+" if is_income else "-") + money(row["amount"]),
                amount_color=COLOR_INCOME if is_income else COLOR_EXPENSE,
                on_release=lambda item: self.open_options(item.tx_id),
            ))
    def open_options(self, tx_id):
        """Muestra un menú emergente con Editar / Borrar / Cancelar."""
        content = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(10))
        popup = Popup(title="¿Qué quieres hacer?", content=content,
                    size_hint=(0.85, None), height=dp(260))

        def on_edit(*args):
            popup.dismiss()
            self.edit_transaction(tx_id)

        def on_delete(*args):
            popup.dismiss()
            self.open_confirmation(tx_id)

        btn_edit = Button(text="Editar")
        btn_delete = Button(text="Borrar", background_color=(0.86, 0.21, 0.21, 1))
        btn_cancel = Button(text="Cancelar", on_release=popup.dismiss)
        btn_edit.bind(on_release=on_edit)
        btn_delete.bind(on_release=on_delete)
        

        for btn in (btn_edit, btn_delete, btn_cancel):
            content.add_widget(btn)
        popup.open()

    def edit_transaction(self, tx_id):
        """Abre el formulario en modo edición con los datos del movimiento."""
        add_screen = self.manager.get_screen("add")
        add_screen.load_for_edit(tx_id)
        self.manager.current = "add"
    
    def open_confirmation(self, tx_id):
        """Muestra un menú emergente con “¿Seguro que quieres borrar?” con Sí y No."""
        content = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(10))
        popup = Popup(title="¿Seguro que quieres borrar?", content=content,
                    size_hint=(0.85, None), height=dp(260))
        
        def on_yes(*args):
            popup.dismiss()
            self.delete_transaction(tx_id)
                
        btn_no = Button(text="No", on_release=popup.dismiss)
        btn_si = Button(text="Si", background_color=(0.86, 0.21, 0.21, 1))
        btn_si.bind(on_release=on_yes)
        for btn in (btn_si, btn_no):
            content.add_widget(btn)
        popup.open()

    def delete_transaction(self, tx_id):
        """Borra el movimiento y vuelve a dibujar la lista."""
        App.get_running_app().db.delete_transaction(tx_id)
        self.refresh()
        

        

      
