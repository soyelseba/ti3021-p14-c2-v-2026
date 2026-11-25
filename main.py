# 1. UML -> POO
class Departamento:
    def __init__(self, id_departamento, nombre):
        self.__id_departamento = id_departamento
        self.__nombre = nombre

    def obtener_id_departamento(self): return self.__id_departamento
    def obtener_nombre(self): return self.__nombre
departamento_informatica = Departamento(
    id_departamento=1,
    nombre="Departamento TI"
)
# 2. Conexion a la base de datos
import oracledb
import os
from dotenv import load_dotenv
load_dotenv()
class Database:
    def __init__(self, user, password, dsn):
        self.__user = user
        self.__password = password
        self.__dsn = dsn
    def get_connection(self):
        connection = oracledb.connect(
            user = self.__user,
            password = self.__password,
            dsn = self.__dsn
        )
        return connection
database = Database(
    user = os.getenv("user"),
    password = os.getenv("password"),
    dsn = os.getenv("dsn")
)
# 3. Implementar la clase Repositorio
class RepositorioDepartamento:
    def __init__(self):
        pass

    def crear_tabla(self, connection: oracledb.Connection):
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE DEPARTAMENTOS(
            id_departamento NUMBER PRIMARY KEY,
            nombre VARCHAR2(64) NOT NULL
        )""")
        connection.commit()
        connection.close()

    def listar(self, connection: oracledb.Connection):
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM DEPARTAMENTOS")
        for row in result:
            print(row)
        connection.close()

    def guardar(self, connection: oracledb.Connection, departamento: Departamento):
        cursor = connection.cursor()

        cursor.execute(
            statement = "INSERT INTO DEPARTAMENTOS(id_departamento, nombre) VALUES(:id_departamento, :nombre)",
            parameters = { 
                "id_departamento": departamento.obtener_id_departamento(),
                "nombre": departamento.obtener_nombre() 
                }
        )

        connection.commit()
        connection.close()

repositorio_departamento = RepositorioDepartamento()
repositorio_departamento.guardar(
    connection = database.get_connection(),
    departamento = departamento_informatica
)