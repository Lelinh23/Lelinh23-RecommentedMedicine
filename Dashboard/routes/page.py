from datetime import datetime
import math
import uuid
from flask_bcrypt import Bcrypt
from flask import Blueprint, Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from forms import *
from firebase_admin import credentials, firestore, initialize_app
from modelsPages import *

admin = Blueprint('admin', __name__)
app = Flask(__name__)
bcrypt = Bcrypt(app)

global response

response=dict()
response2=dict()

# Route để hiển thị form chỉnh sửa
@admin.route('/')
def edit_pageTermsServices():
    # Lấy dữ liệu từ Firebase
    doc_ref = db.collection('term_servic_pages').document('samudi_terms')
    doc = doc_ref.get()
    if not doc.exists:
        return "No data found. Please initialize the data."
    data = doc.to_dict()
    return render_template('Pages/TermsandServices/edit_form.html', data=data)

@admin.route('/edit_page_home')
def edit_pageHome():
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
    
    return render_template('Pages/Home/home.html', data_header=data_header, data_section1=data_section1, data_section2=data_section2)

# Route để cập nhật dữ liệu
@admin.route('/update', methods=['POST'])
def update_pageTermsServices():
    # Lấy dữ liệu từ form
    title = request.form.get('title')
    description = request.form.get('description')
    terms = request.form.getlist('terms[]')
    confirmation = request.form.get('confirmation')

    # Cập nhật dữ liệu vào Firestore
    try:
        doc_ref = db.collection('term_servic_pages').document('samudi_terms')
        doc_ref.set({
            "title": title,
            "description": description,
            "terms": terms,
            "confirmation": confirmation
        })
        return jsonify({"success": True, "message": "Dữ liệu đã được cập nhật thành công!"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Lỗi: {str(e)}"})

@admin.route('/update_home_page', methods=['POST'])
def update_HomePage():
    try:
        # Lấy dữ liệu hiện tại từ Firestore
        header_data = db.collection('home_page').document("header").get().to_dict()
        section1_data = db.collection('home_page').document("section1").get().to_dict()
        section2_data = db.collection('home_page').document("section2").get().to_dict()

        # Lấy dữ liệu mới từ form
        header_title = request.form.get('header_title') or header_data['title']
        header_content = request.form.get('header_description') or header_data['content']

        # Xử lý Section 1
        section1_content = []
        index = 1
        while True:
            title = request.form.get(f"section1_title_{index}")
            content = request.form.get(f"section1_description_{index}")
            if not title or not content:
                break
            section1_content.append({"title": title, "content": content})
            index += 1

        # Nếu không có dữ liệu mới cho section1, giữ nguyên dữ liệu cũ
        if not section1_content:
            section1_content = section1_data['content']

        # Xử lý Section 2
        section2_title = request.form.get('section2_title') or section2_data['title']
        section2_content = request.form.get('section2_description') or section2_data['content']

        # Cập nhật dữ liệu vào Firestore
        db.collection('home_page').document("header").set({
            "title": header_title,
            "content": header_content
        })

        db.collection('home_page').document("section1").set({
            "content": section1_content
        })

        db.collection('home_page').document("section2").set({
            "title": section2_title,
            "content": section2_content
        })

        return jsonify({"success": True, "message": "Dữ liệu đã được cập nhật thành công!"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Lỗi: {str(e)}"})

# Lịch sử tư vấn bệnh   
@admin.route('/consultation-dease', methods=['GET'])
@login_required
def consultation_dease():
    # Lấy dữ liệu lịch sử từ Firestore
    consultations_ref = db.collection('consultation_dease')
    history = []
    consultations = consultations_ref.stream()
    for consultation in consultations:
        data = consultation.to_dict()
        timestamp = data.get("timestamp", "")
        if timestamp:  # Chuyển đổi từ chuỗi ISO 8601 sang datetime
            timestamp = datetime.fromisoformat(timestamp)
        history.append({
            "user_id": data.get("user_id", ""),
            "symptoms": data.get("symptoms", []),
            "predicted_result": data.get("predicted_result", ""),
            "description": data.get("description", ""),
            "precautions": data.get("precautions", ""),
            "workout": data.get("workout", ""),
            "diets": data.get("diets", ""),
            "timestamp": timestamp,  # Sử dụng timestamp đã chuyển đổi
        })

    # Render danh sách lịch sử ra HTML
    return render_template('history/consultation_dease.html', history=history)

@admin.route('/manager_pages', methods=['GET', 'POST'])
@login_required
def manager_pages():
    # Khởi tạo form cho tư vấn y tế
    form = medForm()

    # Lấy thông tin người dùng từ Firestore
    user_doc = db.collection('admins').document(current_user.id).get()
    
    if not user_doc.exists:
        return "User not found", 404
    
    if form.validate_on_submit():
        selectedOptions = [form.disease.data, form.age.data, form.gender.data, form.severity.data]

        # Trả kết quả ra giao diện
        return render_template(
            "med_service.html",
            form=form,
            id=current_user.id,  # Sử dụng ID từ current_user
            name=user_data.get('firstname', '').upper(),
            age=user_data.get('age', ''),
            gender=user_data.get('gender', ''),
        )

    # Chuyển dữ liệu người dùng sang dạng từ điển
    user_data = user_doc.to_dict()
    
    # Trả về template với các dữ liệu người dùng và form
    return render_template(
        "manage.html", 
        id=current_user.id,
        name=user_data.get('firstname', '').upper(),
        age=user_data.get('age', ''),
        gender=user_data.get('gender', ''),
    )