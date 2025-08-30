from flask import Flask, request, jsonify
from database import db
from models.user import User
from flask_login import LoginManager, login_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Invalid credentials!"}), 400

    found_user = User.query.filter_by(username=username).first()
    is_password_equal = found_user.password == password
    if found_user and is_password_equal:
        login_user(found_user)
        return jsonify({"message": "Done!"})
    return jsonify({"message": "Invalid credentials!"}), 400


if __name__ == '__main__':
    app.run(debug=True, port=8000)