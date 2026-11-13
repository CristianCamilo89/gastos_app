"""Capa de acceso a datos (SQLite). Toda la lógica SQL vive aquí."""
import sqlite3
from utils.constants import CATEGORIES, PAYMENT_METHODS 
# Tablas que solo guardan una lista de nombres      
NAMED_TABLES = ("categories", "payment_methods", "suppliers")

class Database:
    """Encapsula la conexión y las consultas a la base de datos local."""

    def __init__(self, path: str):
        """Guarda la ruta del archivo .db y crea las tablas si no existen."""
        self.path = path
        self._create_tables()

    def _connect(self) -> sqlite3.Connection:
        """Abre una conexión nueva; las filas se pueden leer por nombre de columna."""
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_tables(self) -> None:
        """Crea la tabla de movimientos la primera vez que se ejecuta la app."""
        conn = self._connect()
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    description    TEXT    NOT NULL,
                    amount         REAL    NOT NULL CHECK (amount > 0),
                    kind           TEXT    NOT NULL CHECK (kind IN ('gasto', 'ingreso')),
                    category       TEXT    NOT NULL,
                    date           TEXT    NOT NULL,          -- formato AAAA-MM-DD
                    payment_method TEXT    NOT NULL,
                    created_at     TEXT    DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tx_date ON transactions(date)")
            for table in NAMED_TABLES:                                  # NUEVO
                conn.execute(                                           # NUEVO
                    f"CREATE TABLE IF NOT EXISTS {table} ("             # NUEVO
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "            # NUEVO
                    "name TEXT NOT NULL UNIQUE COLLATE NOCASE)"         # NUEVO
                )                                                       # NUEVO
            self._seed(conn, "categories", CATEGORIES)                  # NUEVO
            self._seed(conn, "payment_methods", PAYMENT_METHODS)   
        conn.close()

    def _seed(self, conn, table, names):
        """Si la tabla está vacía, la llena con los valores iniciales."""
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        if count == 0:
            conn.executemany(
                f"INSERT INTO {table} (name) VALUES (?)",
                [(n,) for n in names],
            )

    # ------------------------------------------------------------------ escritura
    def add_transaction(self, description, amount, kind, category, date, payment_method) -> int:
        """Inserta un movimiento y devuelve su id."""
        conn = self._connect()
        with conn:
            cur = conn.execute(
                "INSERT INTO transactions (description, amount, kind, category, date, payment_method) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (description, amount, kind, category, date, payment_method),
            )
            new_id = cur.lastrowid
        conn.close()
        return new_id
        def get_transaction(self, tx_id: int):
            """Devuelve un movimiento por su id (o None si no existe). """
        rows = self._query("SELECT * FROM transactions WHERE id = ?", (tx_id,))
        return rows[0] if rows else None

    def update_transaction(self, tx_id, description, amount, kind,
                           category, date, payment_method) -> None:
        """Actualiza todos los campos de un movimiento existente."""
        conn = self._connect()
        with conn:
            conn.execute(
                "UPDATE transactions SET description=?, amount=?, kind=?, "
                "category=?, date=?, payment_method=? WHERE id=?",
                (description, amount, kind, category, date, payment_method, tx_id),
            )
        conn.close()

    def delete_transaction(self, tx_id: int) -> None:
        """Elimina un movimiento por id."""
        conn = self._connect()
        with conn:
            conn.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
        conn.close()

    # ------------------------------------------------------------------ lectura
    def _query(self, sql: str, params=()):
        """Ejecuta un SELECT y devuelve todas las filas."""
        conn = self._connect()
        try:
            return conn.execute(sql, params).fetchall()
        finally:
            conn.close()

    def recent(self, limit: int = 20):
        """Devuelve los últimos movimientos (más recientes primero)."""
        return self._query(
            "SELECT * FROM transactions ORDER BY date DESC, id DESC LIMIT ?", (limit,)
        )

    def all_transactions(self):
        """Devuelve todos los movimientos (para exportar a CSV)."""
        return self._query("SELECT * FROM transactions ORDER BY date, id")

    def month_totals(self, year: int, month: int):
        """Devuelve (total_ingresos, total_gastos) del mes indicado."""
        ym = f"{year:04d}-{month:02d}"
        row = self._query(
            """
            SELECT
                COALESCE(SUM(CASE WHEN kind = 'ingreso' THEN amount END), 0) AS income,
                COALESCE(SUM(CASE WHEN kind = 'gasto'   THEN amount END), 0) AS expense
            FROM transactions WHERE substr(date, 1, 7) = ?
            """,
            (ym,),
        )[0]
        return row["income"], row["expense"]

    def expenses_by_category(self, year: int, month: int):
        """Devuelve [(categoria, total)] de gastos del mes, de mayor a menor."""
        ym = f"{year:04d}-{month:02d}"
        rows = self._query(
            """
            SELECT category, SUM(amount) AS total
            FROM transactions
            WHERE kind = 'gasto' AND substr(date, 1, 7) = ?
            GROUP BY category ORDER BY total DESC
            """,
            (ym,),
        )
        return [(r["category"], r["total"]) for r in rows]
