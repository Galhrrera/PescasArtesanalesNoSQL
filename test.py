#from time import strftime
import time
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
import pprint
import pymongo

load_dotenv(find_dotenv())

client = MongoClient(os.environ.get("CONNECTION_STRING"))

dbs = client.list_database_names()

pescasArtesanales = client.PescasArtesanalesNoSQL

collections = pescasArtesanales.list_collection_names()

print(collections)

def ReadCollection(collectionName):
    print(collectionName)
    collection = pescasArtesanales[collectionName]
    
    values = collection.find()
    
    return values
    

def InsertMetodoDoc(nombreMetodo):
    collection = pescasArtesanales.metodos
    document = {
        "metodo": nombreMetodo
    }

    try:
        inserted_id = collection.insert_one(document).inserted_id
    except:
        print("Ups")
    
    print(inserted_id)


def InsertCuencaDoc(nombreCuenca):
    collection = pescasArtesanales.cuencas
    document = {
        "cuenca": nombreCuenca
    }

    try:
        inserted_id = collection.insert_one(document).inserted_id
    except:
        print("Ups")
    
    print(inserted_id)
    
def InsertPescaDoc(metodo, cuenca, fecha, peso):
    collection = pescasArtesanales.pescas
    print(metodo, cuenca, fecha, peso)
    document = {
        "cuenca": cuenca,
        "metodo": metodo,
        "fecha": fecha,
        "peso": peso
    }

    try:
        inserted_id = collection.insert_one(document).inserted_id
    except pymongo.errors.OperationFailure as err:
        print("Ups: ", err)
    
    print(inserted_id)
    
def UpdateCuencaDoc(cuenca):
    collection = pescasArtesanales["cuencas"]
    print(cuenca)
    actualValue = {
        "cuenca": "Un Río"
    }
    
    newvalues = {
        "$set": {
            "cuenca": cuenca
        }
    }
    
    try:
        collection.update_one(actualValue, newvalues)
    except pymongo.errors.OperationFailure as err:
        print("Ups: ", err)

def DeleteCuencaDoc(cuenca):
    collection = pescasArtesanales["cuencas"]
    
    cuencaToDelete = {
        "cuenca": cuenca
    }
    
    collection.delete_one(cuencaToDelete)

nombreCuenca = "Río Amazonas"
nombreMetodo = "Flecha de mano"
fecha = "2022-10-8"
peso = 52.3
date_object = datetime.strptime(fecha, '%Y-%m-%d')
datefinal = date_object.date()
date = datefinal.strftime("%Y-%m-%d")
#InsertPescaDoc(nombreMetodo, nombreCuenca, fecha, peso)
#InsertCuencaDoc(nombreCuenca)
#InsertMetodoDoc(nombreMetodo)

#print(type(datefinal))

#Imprimir las cuencas
print("las cuencas son: ")
cuencas = ReadCollection("cuencas")

for c in cuencas:
    print(c)
    

#Actualizar una cuenca
print("Actualizar una cuenca: ")
newCuenca = "Río azul"

UpdateCuencaDoc(newCuenca)

#Imprimir las cuencas
print("las cuencas son: ")
cuencas = ReadCollection("cuencas")
print(type(cuencas))

for c in cuencas:
    print(c)
    

#Actualizar una cuenca
print("Actualizar una cuenca: ")
newCuenca = "Río azul"

#Eliminar un cuenca
cuencaTOdelete = "Río azul"

#Imprimir las cuencas
print("las cuencas son: ")
cuencas = ReadCollection("cuencas")

for c in cuencas:
    print(c)
    
    
DeleteCuencaDoc(cuencaTOdelete)

#Imprimir las cuencas
print("las cuencas son: ")
cuencas = ReadCollection("cuencas")

for c in cuencas:
    print(c)
        