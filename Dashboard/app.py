from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from firebase_admin import credentials, firestore, initialize_app
# Import các module đã tách
from models import *
from routes.auth import *
from routes.page import *

app = Flask(__name__)
app.secret_key = 'thuylinh1'
app.register_blueprint(auth, url_prefix='/auth')  # Đăng ký với prefix '/auth'
app.register_blueprint(admin, url_prefix='/admin')

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

@login_manager.user_loader
def load_user(user_id):
    user_ref = db.collection('admins').document(user_id).get()
    if user_ref.exists:
        user_data = user_ref.to_dict()
        return Admin(id=user_id, **user_data)
    return None

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
