from distutils.log import error
from msilib.schema import Error
import eel
import sys
import  sqlite3 as sql
import json
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
import pprint
import pymongo
from pyparsing import col
from sympy import arg



#Conexión a la base de datos
try:
    initial_client = MongoClient(os.environ.get("CONNECTION_STRING"))
except Exception as err:
    print("Error al conectarse a la base de datos de Mongo: ", err)
    
l_attr_pescas = ["cuenca", "metodo", "fecha", "peso"]

initial_db = initial_client.PescasArtesanalesNoSQL
lista_cuencas = [x['cuenca'] for x in list(initial_db['cuencas'].find({}, {'_id': 0, 'cuenca': 1}))]
lista_metodos = [x['metodo'] for x in list(initial_db['metodos'].find({}, {'_id': 0, 'metodo': 1}))]
collections = initial_db.list_collection_names()
initial_client.close()

#Configuración del entorno
sys.path.append("./")
eel.init("www")

#Editar listas de cuencas y métodos
def append_to_lista(nombre_lista, nuevo_valor):
    if nombre_lista == "lista_cuencas":
        global lista_cuencas
        lista_cuencas.append(nuevo_valor)
    elif nombre_lista == "lista_metodos":
        global lista_metodos
        lista_metodos.append(nuevo_valor)

def update_lista(nombre_lista, valor_anterior, nuevo_valor):
    if nombre_lista == "lista_cuencas":
        global lista_cuencas
        lista_cuencas = [nuevo_valor if x == valor_anterior else x for x in lista_cuencas]
    elif nombre_lista == "lista_metodos":
        global lista_metodos
        lista_metodos = [nuevo_valor if x == valor_anterior else x for x in lista_metodos]

def delete_from_lista(nombre_lista, valor):
    if nombre_lista == "lista_cuencas":
        global lista_cuencas
        lista_cuencas.remove(valor)
    elif nombre_lista == "lista_metodos":
        global lista_metodos
        lista_metodos.remove(valor)

#Actualizar el schema validation de JSON
def update_schema_validation():
    try:
        client = MongoClient(os.environ.get("CONNECTION_STRING"))
        db = client.PescasArtesanalesNoSQL
    except Exception as e:
        client.close()
        return jsonize("[ERR]Connection to DB failed:" + str(e))
    else:
        try:
            schema_validation = { 
            "$jsonSchema": { 
                "bsonType": "object", 
                "required": ["_id", "cuenca", "metodo", "fecha", "peso"], 
                "properties": { 
                    "_id": { "bsonType": "objectId" }, 
                    "cuenca": { 
                        "enum": lista_cuencas, 
                        "description": "El nombre de la cuenca ingresado no es válido" 
                    }, 
                    "metodo": { 
                        "enum": lista_metodos, 
                        "description": "El nombre del método de pesca ingresado no es válido" 
                    }, 
                    "fecha": { 
                        "bsonType": "date", 
                        "description": "La fecha debe estar en formato YYYY/MM/DD" 
                    }, 
                    "peso": { 
                        "bsonType": "double", 
                        "minimum": 1, 
                        "description": "El peso de la pesca debe ser un número y mayor a 1" 
                    }
                }, 
                "additionalProperties": False 
            } 
        }
            db.command("collMod", "pescas", validator=schema_validation)
        except Exception as e:
            client.close()
            return jsonize("[ERROR]Schema validation failed:" + str(e))    
        finally:
            client.close()





#Aquí los métodos
#Decodificar json en string
def jsonize(text):
    return json.dumps(text, ensure_ascii=False, default=str).encode('utf-8').decode()

#Read Collection
@eel.expose
def read(collection_name): #Collection is similar to table name on SQL scheme
    try:
        client = MongoClient(os.environ.get("CONNECTION_STRING"))
        pescasArtesanalesDB = client.PescasArtesanalesNoSQL
    except Exception as e:
        client.close()
        return jsonize("[ERROR]Conexión con mongo falló:" + str(e))

    try:
        if collection_name not in collections:
            return jsonize("[ERROR]El nombre de la colección no existe")

        col = pescasArtesanalesDB[collection_name]
        documents = col.find()

    except Exception as e:
        client.close()
        return jsonize("[ERROR]" + str(e))
    else:
        listaDocumentos = []
        for doc in documents:
            listaDocumentos.append(doc)
        client.close()
        return jsonize(listaDocumentos)
    

#Select / READ
@eel.expose       
def select(table_name):
    #decoded=""
    try:
        conn = sql.connect("./DataSource/PescasArtesanalesDB.sqlite")
        print("Conectado a la base de datos para ejecutar select...")
        print("TABLA: ", table_name)
        cursor = conn.cursor()
        lista_registros = []
        for row in cursor.execute("SELECT * FROM " + table_name):
            lista_registros.append(row)
        print("Query select ejecutado...")

        encoded = json.dumps(lista_registros, ensure_ascii=False).encode('utf8')
        decoded = encoded.decode()
    except sql.Error as error:
        print("Error al conectar con la base de datos - ",error)
    finally:
        if conn:
            conn.close()
            print("La conexión a la base de datos ha finalizado...")

    return decoded

#Create cuencas & metodos
@eel.expose
def create(table_name, args):
    
    try:
        conn = sql.connect("./DataSource/PescasArtesanalesDB.sqlite")
        print("Conectado a la base de datos para ejecutar create...")
        cursor = conn.cursor()
        columna=""
        if(table_name=="metodos"):
            columna = "metodo"
            query = "INSERT INTO " + table_name + " (" + columna + ") VALUES (?)"
        elif(table_name == "cuencas"):
            columna="cuenca"
            query = "INSERT INTO " + table_name + " (" + columna + ") VALUES (?)"
            
        cursor.execute(query,[args])
        conn.commit()
        print(columna+": registro creado satisfactoriamente")
    except sql.Error as error:
        print("Error al crear registro en la base de datos - ",error)
    finally:
        if conn:
            conn.close()
            print("La conexión a la base de datos ha finalizado...")
            
#Create pescas            
@eel.expose
def create_pescas(table_name, args):
    print("MÉTODO CREAR PESCAS")
    try:
        conn = sql.connect("./DataSource/PescasArtesanalesDB.sqlite")
        print("Conectado a la base de datos para ejecutar create...")
        cursor = conn.cursor()
        query = "INSERT INTO pescas (id_cuenca, id_metodo, fecha, peso_pesca) VALUES (?, ?, ?, ?)"
        print(query)
        cursor.execute(query, [args[0], args[1], args[2], args[3]])
        conn.commit()
    except sql.Error as error:
        print("Error al crear registro en la base de datos - ",error)
    finally:
        if conn:
            conn.close()
            print("La conexión a la base de datos ha finalizado...")


#Update cuencas & metodos
@eel.expose
def update(table_name, args):
    try:
        conn = sql.connect("./DataSource/PescasArtesanalesDB.sqlite")
        cursor = conn.cursor()
        columna=""
        id_column=""
        if (table_name =="metodos"):
            columna = "metodo"
            id_column = "id_metodo"
        elif(table_name=="cuencas"):
            columna="cuenca"
            id_column = "id_cuenca"
                
        query = "UPDATE " + table_name + " SET "+columna+"=(?) WHERE "+id_column+"=(?);"
        cursor.execute(query, [args[1], args[0]])
        conn.commit()
        print("Registo en ", columna, "Actualizado satisfactoriamente")
    except sql.Error as error:
        print("Error al Actualizar el registro en la base de datos", error)
    finally:
        if conn:
            conn.close()
            print("La conexión a la base de datos ha finalizado...")

#Update pescas
@eel.expose
def updatePescas(table_name, args):
    print("update pescas")
    try:
        conn = sql.connect("./DataSource/PescasArtesanalesDB.sqlite")
        cursor = conn.cursor()
        query = "UPDATE "+ table_name + " SET id_cuenca = (?), id_metodo = (?), fecha = (?), peso_pesca = (?) WHERE id_pesca = (?)"
        cursor.execute(query, [args[1], args[2], args[3], args[4], args[0]])
        conn.commit()
        print("Registo en ", table_name, "Actualizado satisfactoriamente")
    except sql.Error as error:
        print("Error al Actualizar el registro en la base de datos", error)
    finally:
        if conn:
            conn.close()
            print("La conexión a la base de datos ha finalizado...")
#Delete 
@eel.expose
def delete(table_name, args):
    print("la tabla en la que se va a eliminar el dato es: ", table_name)
    if (table_name == "cuencas") and validarUso(args, "pescas", "id_cuenca"):
        text ="[ERROR] La Cuenca #" + args + " está siendo usada en la tabla Pescas"
        return json.dumps(text, ensure_ascii=False).encode('utf-8').decode()
    if (table_name == "metodos") and validarUso(args, "pescas", "id_metodo"):
        text = "[ERROR] El Metodo #" + args + " está siendo usado en la tabla Pescas"
        return json.dumps(text, ensure_ascii=False).encode('utf-8').decode()
    try:
        conn = sql.connect("./DataSource/PescasArtesanalesDB.sqlite")
    except:
        print("Error al conectar con la base de datos")
    cursor = conn.cursor()
    if table_name == "metodos":
        try:
            query = "DELETE FROM " + table_name + " WHERE id_metodo=(?);"
            cursor.execute(query, [args])
            conn.commit()
        except sql.Error as error:
            print("Error al eliminar un dato en la tabla: "+table_name+" - "+error)
    elif table_name == "cuencas":
        try:
            query = "DELETE FROM " + table_name + " WHERE id_cuenca=(?);"
            cursor.execute(query, [args])
            conn.commit()
        except sql.Error as error:
            print("Error al eliminar un dato en la tabla: "+table_name+" - "+error)
    elif table_name == "pescas":
        print("ENTRA AL CONDICIONAL DE TABLA PESCAS DELETE")
        try:
            query = "DELETE FROM " + table_name + " WHERE id_pesca=(?);"
            cursor.execute(query, [args])
            conn.commit()
        except sql.Error as error:
            print("Error al eliminar un dato en la tabla: "+table_name+" - "+error)
    conn.close()
    

#Validar si un elemento está siendo usado en la tabla pescas
def validarUso(val, table, column):
    print(val)
    print(table)
    print(column)
    try:
        conn = sql.connect("./DataSource/PescasArtesanalesDB.sqlite")
    except:
        print("Error al conectar con la base de datos")
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM " + table + " WHERE " + column + "=(?)"
    rows = int(cursor.execute(query, [val]).fetchone()[0])
    print(rows)
    if(rows > 0):
        return True
    else:
        return False


#Start app
eel.start("pescas.html", size=(1920,1080), position=(0,0)) #El tamaño será 1920 x 1080 y se iniciará en la posicón 0,0 (ocupará toda la pantalla en un monitor 1080)