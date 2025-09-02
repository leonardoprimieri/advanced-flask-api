from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from database import db
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@127.0.0.1:3306/flask-crud'

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

    if found_user and found_user.password == password:
        login_user(found_user)
        return jsonify({"message": "Done!"}), 200

    return jsonify({"message": "Invalid credentials!"}), 400


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "User logged out."}), 200


@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing username or password."}), 400

    found_user = User.query.filter_by(username=username).first()
    if found_user:
        return jsonify({"message": "User already exists."})

    new_user = User(username=username, password=password, role='user')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created."})


@app.route("/user/<int:user_id>")
@login_required
def read_user(user_id):
    found_user = User.query.get(user_id)

    if not found_user:
        return jsonify({"message": "User not found."}), 404
    return jsonify({"username": found_user.username}), 200


@app.route("/user/update-password/<int:user_id>", methods=['PUT'])
@login_required
def update_user_password(user_id):
    new_password = request.json.get('password')
    found_user = User.query.get(user_id)

    same_user = current_user.id == found_user.id

    if not same_user:
        if current_user.role == 'user':
            return jsonify({"message": "You don't have permission to perform this action."}), 403

    if not new_password:
        return jsonify({"message": "A password is required."}), 403

    if not found_user:
        return jsonify({"message": "User not found."}), 404

    found_user.password = new_password
    db.session.commit()
    return jsonify({"message": "Password successfully changed."})


@app.route('/user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    found_user = User.query.get(user_id)

    if not found_user:
        return jsonify({"message": "User not found."}), 404

    if current_user.id == found_user.id:
        return jsonify({"message": "You can't delete your own user."}), 409

    db.session.delete(found_user)
    db.session.commit()
    return jsonify({"message": "User successfully deleted."})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
