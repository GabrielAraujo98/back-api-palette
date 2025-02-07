from flask import jsonify
import psycopg2
import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv()

def getDB():
    db_connector = psycopg2.connect(database = os.getenv('DB_NAME'), 
                        user = os.getenv('DB_USERNAME'), 
                        host= os.getenv('DB_HOST'),
                        password = os.getenv('DB_PASSWORD'),
                        port = os.getenv('DB_PORT'))
    return db_connector

def getSugestedPalettes():
    conn = getDB()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM sugested_palettes""")
    resposta = {'palettes': cur.fetchall()}
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(resposta)

def setSugestedPalette(idPalette, schemeLength, colors, scheme, variation):
    conn = getDB()
    cur = conn.cursor()
    cur.execute("""INSERT INTO sugested_palettes (id_palette, scheme_length, colors, scheme, variation) VALUES (%s, %s, %s, %s, %s)""", (idPalette, schemeLength, colors, scheme, variation))
    conn.commit()
    cur.close()
    conn.close()
    
    resposta = {'palette': 'A paleta foi criado'}

    return jsonify(resposta)