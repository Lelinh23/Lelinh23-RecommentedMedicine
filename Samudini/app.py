from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from firebase_admin import credentials, firestore, initialize_app

# Import các module đã tách
from model.models import *
from model.recomment_df import *
from routes.auth import auth
from routes.pages import *
from routes.service import *
from forms import RegisterForm, LoginForm, medForm, serviceForm

app = Flask(__name__)
app.secret_key = 'CBKkwggSlAgEAAoIBAQDtAqren'
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(service, url_prefix='/service')
print(app.blueprints)  # This will list all registered blueprints.

# Firebase setup
try:
    cred = credentials.Certificate('data-recoment-drugs.json')
    initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print("Firebase initialization error:", e)

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.signin'

@login_manager.user_loader
def load_user(user_id):
    user_ref = db.collection('users').document(user_id).get()
    if user_ref.exists:
        user_data = user_ref.to_dict()
        return User(id=user_id, **user_data)
    return None

# Định nghĩa route (Ví dụ)
@app.route("/")
def index():
    # Lấy dữ liệu từ Firebase (collection 'home_page')
    home_page_ref = db.collection('home_page')
    docs = home_page_ref.stream()
    
    # Chuyển dữ liệu Firestore thành dictionary
    home_page_data = {}
    for doc in docs:
        home_page_data[doc.id] = doc.to_dict()

    # Tách dữ liệu cho từng phần
    data_header = home_page_data.get("header", {})
    data_section1 = home_page_data.get("section1", {}).get("content", [])
    data_section2 = home_page_data.get("section2", {})
    
    return render_template("home.html", data_header=data_header, data_section1=data_section1, data_section2=data_section2)

# Đăng ký blueprint
app.register_blueprint(auth) 

if __name__ == '__main__':
    app.run(debug=True)
