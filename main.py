from datetime import datetime
from distutils.log import error
from msilib.schema import Error
from bson import ObjectId
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
from pymongo.errors import WriteError



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

print("metodos: ")
print(lista_metodos)
print("cuencas: ")
print(lista_cuencas)

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
            return jsonize("[ERROR] Schema validation failed:" + str(e))    
        finally:
            client.close()



def jsonize(text):
    jsonized_text = json.dumps(text, ensure_ascii=False, default=str).encode('utf-8').decode()
    return jsonized_text


#Aquí los métodos paralas querys

#Read Collection
@eel.expose
def read(collection_name): #Collection is similar to table name on SQL scheme
    try:
        client = MongoClient(os.environ.get("CONNECTION_STRING"))
        pescasArtesanalesDB = client.PescasArtesanalesNoSQL
    except Exception as e:
        client.close()
        return jsonize("[ERROR] Conexión con mongo falló:" + str(e))

    try:
        if collection_name not in collections:
            return jsonize("[ERROR] El nombre de la colección no existe")

        collection = pescasArtesanalesDB[collection_name]
        values = collection.find()
        
        listaDocumentos = []
        for value in values:
            listaDocumentos.append(value)

    except Exception as e:
        client.close()
        return jsonize("[ERROR] " + str(e))
    finally:
        client.close()
        
    return jsonize(listaDocumentos)
    #return listaDocumentos

#InsertDocument
@eel.expose
def create(data, collection_name):
    try:
        client = MongoClient(os.environ.get("CONNECTION_STRING"))
        pescasArtesanalesDB = client.PescasArtesanalesNoSQL
    except Exception as e:
        return jsonize("[ERROR] Conexión con mongo falló:" + str(e))

    try:
        if collection_name not in collections:
            return jsonize("[ERROR] Nombre de colección no valido")
        data_keys = list(data.keys())
        data_keys.sort()
        if (collection_name == "pescas" and not array_equal(data_keys, l_attr_pescas)) or (collection_name == "cuencas" and not array_equal(list(data.keys()), 
            ['cuenca'])) or (collection_name == "metodos" and not array_equal(list(data.keys()), ['metodo'])):
            return jsonize("[ERROR] Llaves del documento a ingresar no validas")

        collection = pescasArtesanalesDB[collection_name]

        if collection_name == "cuencas":
            append_to_lista("lista_cuencas", data['cuenca'])
            update_schema_validation()
        elif collection_name == "metodos":
            append_to_lista("lista_metodos", data['metodo'])
            update_schema_validation()
        elif collection_name == "pescas":
            data['fecha'] = datetime.strptime(data['fecha'], "%Y-%m-%d")
            data['peso'] = float(data['peso'])
            

        collection.insert_one(data)
        
    except Exception as e:
        client.close()
        return jsonize("[ERROR] " + str(e))
    finally:
        client.close()
        return jsonize("[MSG] Documento creado con éxito")

#DeleteDocument
@eel.expose
def delete(_id, collection_name):
    try:
        client = MongoClient(os.environ.get("CONNECTION_STRING"))
        pescasArtesanalesDB = client.PescasArtesanalesNoSQL
    except Exception as e:
        return jsonize("[ERROR] Conexión con mongo falló:" + str(e))

    try:
        if collection_name not in collections:
            return jsonize("[ERROR] Nombre de colección no valido")
        collection = pescasArtesanalesDB[collection_name]
        _id = ObjectId(_id)
        old_doc = collection.find_one({'_id': _id})
        is_related = True

        if collection_name != "pescas":
            if collection_name == "cuencas":
                cuencas_count = pescasArtesanalesDB['pescas'].count_documents({"cuenca": old_doc['cuenca']})
                if cuencas_count == 0:
                    is_related = False
                    delete_from_lista("lista_cuencas", old_doc['cuenca'])
                    update_schema_validation()
            if collection_name == "metodos":
                metodos_count = pescasArtesanalesDB['pescas'].count_documents({'metodo': old_doc['metodo']})
                if metodos_count == 0:
                    is_related = False
                    delete_from_lista("lista_metodos", old_doc['metodo'])
                    update_schema_validation()
        else:
            is_related = False
        if not is_related:
            collection.find_one_and_delete({"_id": _id})
            return jsonize("[MSG] Documento eliminado con éxito")
        else:
            return jsonize("[ERROR] El doc se encuentra en uso en la colección Pescas")
    except Exception as e:
        return jsonize("[ERROR] Error al eliminar el documento:", e)
    finally:
        client.close()

    
#Update
@eel.expose
def update(_id, data, collection_name):
    try:
        client = MongoClient(os.environ.get("CONNECTION_STRING"))
        pescasArtesanalesDB = client.PescasArtesanalesNoSQL
    except Exception as e:
        return jsonize("[ERROR] Conexión con mongo falló:", e)

    try:
        if collection_name not in collections:
            return jsonize("[ERROR] Nombre de colección no valido")
        dict_keys = list(data.keys())
        dict_keys.sort()
        if (collection_name == "pescas" and not array_equal(dict_keys, l_attr_pescas)) or (collection_name == "cuencas" and not array_equal(list(data.keys()), 
                    ['cuenca'])) or (collection_name == "metodos" and not array_equal(list(data.keys()), ['metodo'])):
            return jsonize("[ERROR] datos no válidos")

        _id = ObjectId(_id)

        collection = pescasArtesanalesDB[collection_name]
        old_doc = collection.find_one({'_id': _id})
        
        if old_doc:
            if collection_name == "pescas":
                data['fecha'] = datetime.strptime(data['fecha'], "%Y-%m-%d")
                data['peso'] = float(data['peso'])

            update_json = {
                "$set": data
            }
            collection.find_one_and_update({'_id': _id}, update_json)

            if collection_name != "pescas":
                if collection_name == "cuencas":
                    update_lista("lista_cuencas", old_doc['cuenca'], data['cuenca'])
                    update_schema_validation()
                    pescasArtesanalesDB['pescas'].update_many({'cuenca': old_doc['cuenca']},{ "$set": { 'cuenca': data['cuenca']}})
                elif collection_name == "metodos":
                    update_lista("lista_metodos", old_doc['metodo'], data['metodo'])
                    update_schema_validation()
                    pescasArtesanalesDB['pescas'].update_many({'metodo': old_doc['metodo']},{ "$set": { 'metodo': data['metodo']}})        
    except Exception as e:
        return jsonize("[ERROR] Error al actualizar el documento: ", e)
    finally:
        client.close()
        return jsonize("[MSG] Documento actualizado con éxito")


#Start app
eel.start("pescas.html", size=(1920,1080), position=(0,0)) #El tamaño será 1920 x 1080 y se iniciará en la posicón 0,0 (ocupará toda la pantalla en un monitor 1080)