from flask import Flask, jsonify, request
import uuid
from flask_cors import CORS
from dotenv import load_dotenv, dotenv_values 
from src.users.usersController import getUsers, setUser, deleteUser, editUser, getUsersByEmail

app = Flask(__name__)
CORS(app)

@app.route('/')
def homepage():
    return 'A Api está no ar'


@app.route('/api/createuser', methods=['POST'])
def createuser():
    # salvando o corpo da requisição em uma variavel 
    # para utilizar os valores nele para criar o usuário
    request_data = request.get_json()
    idUser = str(uuid.uuid4())
    nameUser = request_data['user']
    emailUser = request_data['email']
    keywordUser = request_data['password']
    fotoUser = "null"
    return setUser(idUser, nameUser, emailUser, keywordUser, fotoUser)

@app.route('/api/getusers', methods=['GET'])
def getAllUsers():
    return getUsers()

@app.route('/api/deleteusers', methods=['DELETE'])
def deleteUsers():
    emailUser = str(input("email:"))
    keywordUser = str(input("senha:"))
    deleteUser(emailUser, keywordUser)
    return 'Usuário deletado'

@app.route('/api/edituser')
def updateUser():
    email = str(input("email:"))
    fildToEdit = str(input("qual campo deseja alterar?"))
    edition = str(input(fildToEdit))
    editUser(email, fildToEdit, edition)
    return 'Usuário editado'

@app.route('/api/getuserbyemail/', methods=['GET'])
def getUserByEmail():
    # salvando o cabeçalho da requisição em uma variavel 
    # para utilizar o valor do email e da senha para verificar a existencia do usuário
    emailTarget = request.headers['email']
    keywordTarget = request.headers['password']
    print(emailTarget, keywordTarget)
    return jsonify(getUsersByEmail(emailTarget, keywordTarget))
    
            

if __name__ == '__main__':
    app.run()