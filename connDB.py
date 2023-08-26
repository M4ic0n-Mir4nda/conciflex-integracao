import pyodbc


class ConnectDB:
    def __init__(self, dsn_name):
        self.dsn_name = dsn_name

    def conecta(self):
        try:
            # Conectar ao DSN especificado
            self.conn = pyodbc.connect(f"DSN={self.dsn_name};")
            self.cursor = self.conn.cursor()

        except pyodbc.Error as e:
            print(f"Erro ao conectar com o DSN '{self.dsn_name}': {e}")
            return False

    def execute(self, query):
        self.cursor.execute(query)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall_dict(self):
        results = []
        columns = [column[0] for column in self.cursor.description]
        rows = self.fetchall()

        for row in rows:
            row_dict = dict(zip(columns, row))
            results.append(row_dict)

        return results

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def disconnect(self):
        self.cursor.close()
        self.conn.close()
