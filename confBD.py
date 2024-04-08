import mysql.connector
from flask import Flask
from flask_mysqldb import MySQL

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