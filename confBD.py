#C:\xampp\miapp\confBD.py
import mysql.connector
from flask import Flask

def conectionBD():
    conexion = mysql.connector.connect(
        host="localhost", 
        user="root", 
        passwd="", 
        database="registro")
    
    if conexion:
        print("Conexión exitosa")
    else:
         print("Conexión fallida")
    return conexion

