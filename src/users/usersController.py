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

def getUsers():
    conn = getDB()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM users""")
    resposta = {'users': cur.fetchall()}
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(resposta)

def getUsersByEmail(emailUser, keywordUser):
    conn = getDB()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM users
                WHERE email = '"""+ emailUser +"""' AND password = crypt('"""+ keywordUser +"""', password)
                """)
    resposta = {'user': cur.fetchall()}
    if resposta['user'][0] == '':
        return 'Usuário inválido'
    else:
        print(resposta)
        conn.commit()
        cur.close()
        conn.close()
        return resposta
        
        
        


def setUser(idUser, nameUser, emailUser, keywordUser, fotoUser):
    conn = getDB()
    cur = conn.cursor()
    print(idUser,  nameUser, emailUser, keywordUser, fotoUser)
    # stringConcat = """'"""+idUser+"""','"""+ nameUser +"""', '"""+ emailUser +"""', 'ENCRYPTBYPASSPHRASE("PSWD", '"""+ keywordUser +"""')', '"""+ fotoUser +"""'"""
    cur.execute("""INSERT INTO users (id_user, username, email, password, img_url) VALUES (%s, %s, %s, crypt('"""+keywordUser+"""', gen_salt('md5')), %s)""", (idUser,  nameUser, emailUser, fotoUser))
    conn.commit()
    cur.close()
    conn.close()
    
    resposta = {'res': 'O usuário foi criado'}

    return jsonify(resposta)

def editUser(emailUser, fieldToEdit, edition):
    conn = getDB()
    cur = conn.cursor()
    match fieldToEdit:
        case 'email':
            cur.execute("""UPDATE users
                        SET email = '""" + edition + """'
                        WHERE email = '"""+ emailUser + """'""")
            conn.commit()            
            cur.close()
            conn.close()
            return "Email alterado"
        case 'username':
            cur.execute("""UPDATE users
                        SET username = '""" + edition + """'
                        WHERE email = '"""+ emailUser + """'""")
            conn.commit()            
            cur.close()
            conn.close()
            return "Nome de usuário alterado"
        case 'password':
            cur.execute("""UPDATE users
                        SET password = '""" + edition + """'
                        WHERE email = '"""+ emailUser + """'""")
            conn.commit()
            cur.close()
            conn.close()
            return "Senha alterada"
        case 'img_url':
            cur.execute("""UPDATE users
                        SET img_url = '""" + edition + """'
                        WHERE email = '"""+ emailUser + """'""")
            conn.commit()
            cur.close()
            conn.close()
            return "Foto do usuário alterada"
        case _:
            cur.close()
            conn.close()
            return "Este campo não pode ser editado"

def deleteUser(emailUser, keywordUser):
    conn = getDB()
    cur = conn.cursor()
    cur.execute("""DELETE FROM users
                 WHERE email = '"""+ emailUser +"""' AND password = '"""+ keywordUser +"""'
                """)
    conn.commit()
    cur.close()
    conn.close()
    return 'Usuário deletado'