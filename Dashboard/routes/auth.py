import math
import uuid
from flask_bcrypt import Bcrypt
from flask import Blueprint, Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from forms import *
from firebase_admin import credentials, firestore, initialize_app
from models import *

auth = Blueprint('auth', __name__)
app = Flask(__name__)
bcrypt = Bcrypt(app)

global response

response=dict()
response2=dict()

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user_data = Admin.get_admin_by_email(form.email.data)
        if user_data and bcrypt.check_password_hash(user_data['password'], form.password.data):
            user_obj = Admin(**user_data)
            login_user(user_obj)
            flash('Login successful!', 'success')
            return redirect(url_for('auth.manage'))
        flash('Invalid email or password.', 'error')
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try: 
            user_id = Admin.add_admin(
                id=request.form.get('email'),
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                age=form.age.data,
                gender=form.gender.data,
                email=form.email.data,
                address=form.address.data,
                password=form.password.data,
                pastcondition=form.pastcondition.data
            )
            flash('Registration successful! Please log in!', 'success')
        except Exception as e:
            flash(f"Registration failed: {e}", 'error')
            print(e)
        return redirect(url_for('auth.signin'))
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất thành công!', 'success')
    return redirect(url_for('index'))

@auth.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
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
    
@auth.route('/add-doctor', methods=['GET', 'POST'])
@login_required
def add_doctor():
    # Khởi tạo form cho thêm bác sĩ
    form_add_doctor = AddDoctor()
    
    # Kiểm tra khi form thêm bác sĩ được submit
    if form_add_doctor.validate_on_submit():
        try:
            # Lấy danh sách bác sĩ hiện có để tìm ID cao nhất
            doctors = Doctor.get_all_doctors()  # Hàm này trả về danh sách bác sĩ
            if not doctors:
                new_id = "Dr1"  # ID khởi tạo đầu tiên nếu chưa có bác sĩ nào
            else:
                # Lấy ID cuối cùng, loại bỏ phần "Dr" và tăng số lên
                max_id = max(int(doc.id[2:]) for doc in doctors if doc.id.startswith("Dr"))
                new_id = f"Dr{max_id + 1}"
            
            # Thêm bác sĩ với ID mới
            doctor_id = Doctor.add_doctor(
                id=new_id,  # ID tự động tạo
                firstname=form_add_doctor.firstname.data,
                lastname=form_add_doctor.lastname.data,
                age=form_add_doctor.age.data,
                gender=form_add_doctor.gender.data,
                email=form_add_doctor.email.data,
                address=form_add_doctor.address.data,
                disease=form_add_doctor.disease.data,
                specialization=form_add_doctor.specialization.data,
                star=form_add_doctor.star.data
            )
            flash('Doctor added successfully!', 'success')
        except Exception as e:
            flash(f"Failed to add doctor: {e}", 'error')
            print(e)
        return redirect(url_for('auth.list_doctor'))  # Chuyển hướng đến danh sách bác sĩ
    
    # Trả về danh sách bác sĩ dưới dạng template
    return render_template('Doctor/add.html', form_add_doctor=form_add_doctor)


@auth.route('/list_doctor', methods=['GET', 'POST'])
@login_required
def list_doctor():
    
    # Lấy danh sách bác sĩ từ Firestore
    doctors = Doctor.get_all_doctors()
    
    # Trả về danh sách bác sĩ dưới dạng template
    return render_template('Doctor/doctor.html', doctors=doctors)

@auth.route('/funtionD', methods=['GET', 'POST'])
@login_required
def funtionD():
    
    return render_template('Doctor/funtionD.html')

@auth.route('/list_user', methods=['GET', 'POST'])
@login_required
def list_user():
    
    # Lấy danh sách bác sĩ từ Firestore
    users = User.get_all_user()
    
    # Trả về danh sách bác sĩ dưới dạng template
    return render_template('user/user_list.html', users=users)


