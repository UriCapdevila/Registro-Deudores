# database.py
import mysql.connector
from flask import current_app, g
from mysql.connector import Error

def get_db_connection():
    if 'db' not in g:
        try:
            config = current_app.config
            g.db = mysql.connector.connect(
                host=config['DB_HOST'],
                user=config['DB_USER'],
                password=config['DB_PASSWORD'],
                database=config['DB_NAME']
            )
        except Error as e:
            current_app.logger.error(f"Error de conexión a la base de datos: {e}")
            g.db = None
    return g.db

def close_db_connection(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()