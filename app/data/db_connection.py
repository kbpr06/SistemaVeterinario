import sqlite3
from sqlite3 import Error


class DBConnection:
    def __init__(self, db_path: str):
        """Inicializa la conexión a la base de datos.
        :param db_path: Ruta al archivo .db"""
        self.db_path = db_path
        self.connection = None

    def connect(self):
        """ Crea y retorna una conexión a la base de datos SQLite."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            return self.connection
        except Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
