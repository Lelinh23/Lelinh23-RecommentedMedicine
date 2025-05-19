import Levenshtein
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from fuzzywuzzy import fuzz

bcrypt = Bcrypt()

# Kết nối với Firebase
try:
    cred = credentials.Certificate('data-recoment-drugs.json')
    firebase_admin.initialize_app(cred)
except Exception as e:
    print("Firebase initialization error:", e)
    
# Khởi tạo Firestore
db = firestore.client()

# Dữ liệu mặc định của dịch vụ và điều khoản
default_data = {
    "title": "WELCOME",
    "description": "Before using our application, please read carefully and accept our Terms and Services:",
    "terms": [
        "Non-Diagnostic Nature: Informational checkup only, not a medical diagnosis. Seek professional advice for personalized guidance.",
        "Not a Qualified Medical Opinion: Results do not replace professional medical opinions.",
        "Anonymous Information: User data remains anonymous and secure."
    ],
    "confirmation": "I hereby agree to the Terms and Conditions"
}

# Kiểm tra và tạo dữ liệu nếu chưa tồn tại
doc_ref = db.collection('term_servic_pages').document('samudi_terms')
doc = doc_ref.get()
if not doc.exists:
    doc_ref.set(default_data)
    print("Dữ liệu mặc định đã được tạo.")
else:
    print("Dữ liệu đã tồn tại.")
    
    
# Tạo dữ liệu mẫu cho home page
home_page_data = {
    "header": {
        "title": "Thuy Linh",
        "content": "Ayurveda for Everyone on Everyday..."
    },
    "section1": {
        "content": [  # Đặt mảng `section1` trong trường `content`
            {
                "title": "Drug Recommendation System",
                "content": "Our advanced model predicts Migraine, Gastric..."
            },
            {
                "title": "Recommending Ayurvedic Medicine",
                "content": "Personalized remedies based on symptoms."
            }
        ]
    },
    "section2": {
        "title": "Learn More About AyuCare",
        "content": "Machine learning models are revolutionizing..."
    }
}

# Thêm dữ liệu vào Firestore
for key, value in home_page_data.items():
    db.collection('home_page').document(key).set(value)

print("Collection `home_page` has been initialized!")
