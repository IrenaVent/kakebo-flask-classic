import sqlite3

class DBManager():
    def __init__(self, ruta_basedatos):
        self.ruta_basedatos = ruta_basedatos

    def consultaSQL (self, consulta, params = []):
        # la conexion se abre cuando se abre la consulta
        conn = sqlite3.connect(self.ruta_basedatos)

        # es un objeto para realizar consultas y donde se queda el resultado de la consulta
        cur = conn.cursor() 
        
        # consulta es pasada desde la instancias en views
        cur.execute(consulta, params) 

        # creación de la lista de dicionarios /de lista de [{registro==movimientos}]
        keys = []
        for item in cur.description:
            keys.append(item[0])

        registros = []
        for registro in cur.fetchall():
            ix_clave = 0
            d = {}
            for columna in keys:
                d[columna] = registro [ix_clave]
                ix_clave += 1
            registros.append(d)

        conn.close()
        return registros
    
    def modificaSQL (self, consulta, params):
        conn = sqlite3.connect(self.ruta_basedatos)

        cur = conn.cursor()

        cur.execute(consulta, params)
        conn.commit()
        conn.close()
