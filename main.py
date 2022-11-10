from datetime import datetime
from distutils.log import error
from msilib.schema import Error
import eel
import sys
import  sqlite3 as sql
import json
from numpy import array_equal
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
l_attr_pescas.sort()

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



def jsonize(text):
    jsonized_text = json.dumps(text, ensure_ascii=False, default=str).encode('utf-8').decode('utf-8')
    #print(type(text))
    #print(jsonized_text)
    return jsonized_text


#Aquí los métodos paralas querys

#Read Collection
@eel.expose
def read(collection_name): #Collection is similar to table name on SQL scheme
    #print(collection_name)
    try:
        client = MongoClient(os.environ.get("CONNECTION_STRING"))
        pescasArtesanalesDB = client.PescasArtesanalesNoSQL
    except Exception as e:
        client.close()
        return jsonize("[ERROR]Conexión con mongo falló:" + str(e))

    try:
        if collection_name not in collections:
            return jsonize("[ERROR]El nombre de la colección no existe")

        collection = pescasArtesanalesDB[collection_name]
        values = collection.find()
        
        listaDocumentos = []
        for value in values:
            listaDocumentos.append(value)

    except Exception as e:
        client.close()
        return jsonize("[ERROR]" + str(e))
    finally:
        client.close()
        
    return jsonize(listaDocumentos)
    #return listaDocumentos


@eel.expose
def create(data, collection_name):
    try:
        client = MongoClient(os.environ.get("CONNECTION_STRING"))
        pescasArtesanalesDB = client.PescasArtesanalesNoSQL
    except Exception as e:
        return jsonize("[ERROR]Conexión con mongo falló:" + str(e))

    try:
        if collection_name not in collections:
            return jsonize("[ERROR]Nombre de colección no valido")
        data_keys = list(data.keys())
        data_keys.sort()
        if (collection_name == "pescas" and not array_equal(data_keys, l_attr_pescas)) or (collection_name == "cuencas" and not array_equal(list(data.keys()), 
            ['cuenca'])) or (collection_name == "metodos" and not array_equal(list(data.keys()), ['metodo'])):
            return jsonize("[ERROR]Llaves del documento a ingresar no validas")

        if collection_name == "cuencas":
            append_to_lista("lista_cuencas", data['cuenca'])
            update_schema_validation()
        elif collection_name == "metodos":
            append_to_lista("lista_metodos", data['metodo'])
            update_schema_validation()

        col = pescasArtesanalesDB[collection_name]
        if collection_name == "pescas":
            data['fecha'] = datetime.strptime(data['fecha'], "%Y-%m-%d")
            data['peso'] = float(data['peso'])
        col.insert_one(data)
        
    except pymongo.errors as e:
        client.close()
        err_desc = str(e).split("'description': ",1)[1]
        return jsonize("[ERROR]" + err_desc.split("'", 2)[1])
    except Exception as e:
        client.close()
        return jsonize("[ERR]" + str(e))
    finally:
        client.close()
        with open("logs.txt", 'a', encoding='utf-8') as logs:
            logs.write("[" + str(datetime.now())[0:16] + "]\tCREATE on " + collection_name + ", args:" + str(data) + "<br>\n")
        return jsonize("[MSG]Operación realizada con exito :)")




#Start app
eel.start("pescas.html", size=(1920,1080), position=(0,0)) #El tamaño será 1920 x 1080 y se iniciará en la posicón 0,0 (ocupará toda la pantalla en un monitor 1080)