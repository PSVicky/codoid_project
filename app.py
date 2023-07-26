from flask import Flask, request, jsonify,render_template
from flask_restful import Resource, Api
import pymysql
import bcrypt
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
api = Api(app)

db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='codoid',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def main():
    return render_template("signin.html")
class SignUp(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if username and password:
           
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            cursor = db.cursor()
            try:
                cursor.execute("INSERT INTO users (username,email, password) VALUES (%s,%s ,%s)", (username,email, hashed_password))
                db.commit()
                return {'message': 'User created successfully'}, 201
            except pymysql.IntegrityError:
                db.rollback()
                return {'message': 'User already exists'}, 400
            finally:
                cursor.close()
        else:
            return {'message': 'Invalid input'}, 400

class SignIn(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'message': 'Invalid input'}, 400

        cur = db.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return {'token': token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

api.add_resource(SignUp, '/signup')
api.add_resource(SignIn, '/signin')

if __name__ == '__main__':
    app.run(debug=True)