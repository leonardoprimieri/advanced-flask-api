from flask import Flask
from database import db
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route('/', methods=['GET'])
def hello():
    return 'oi'


if __name__ == '__main__':
    app.run(debug=True, port=8000)