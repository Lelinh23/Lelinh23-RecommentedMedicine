from firebase_admin import credentials, firestore, initialize_app
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from flask_login import UserMixin
from sklearn.metrics import classification_report, confusion_matrix
from text_processing.matching import *
from utils.model_loader import *


def predict_text(lst_text):
    df_test = pd.DataFrame(lst_text, columns = ['test_sent'])
    df_test["test_sent"] = df_test["test_sent"].apply(review_to_words)
    tfidf_bigram = tfidf_vectorizer2.transform(lst_text)
    prediction = condition_model.predict(tfidf_bigram)
    df_test['prediction'] = prediction
    return df_test

# Lọc và chọn danh sách các loại thuốc từ một DataFrame (med) dựa trên các tiêu chí như bệnh, tuổi, tình trạng mang thai, tương tác với rượu, v.v.
# Trả về danh sách các tên thuốc phù hợp.
def recmedicine(disease, age, gender, pregnancy_condition, alcohol, duration=None):
    print("rec medic dataset filter method")
    print(disease, age, gender, pregnancy_condition, alcohol, duration)
    
    # Tìm bệnh khớp chính xác nhất
    closest_disease = get_closest_match(disease, conditions, similarity_threshold=99)
    
    if closest_disease is None:
        print("No matching disease found in the database. Please try again.")
        return []

    # Lọc các dòng trong DataFrame 'med' sao cho medical_condition_description khớp với tên bệnh (closest_disease):
    filtered_df = med[med['medical_condition_description'] == closest_disease]

    if pregnancy_condition is not None:
        # Lọc theo loại an toàn trong thai kỳ
        filtered_df = filtered_df[filtered_df['pregnancy_category'].isin([pregnancy_condition])]

    if alcohol is not None:
        # Lọc theo khả năng tương tác với rượu
        filtered_df = filtered_df[filtered_df['alcohol'].isin([alcohol])]

    # Lọc thêm theo độ tuổi
    if int(age) < 10:
        # Lấy ít nhất 5 loại thuốc hoạt động tốt nhất
        filtered_df = filtered_df.nsmallest(5, 'activity')
    elif 10 <= int(age) <= 15:
        # Lấy ít nhất 10 loại thuốc hoạt động tốt nhất
        filtered_df = filtered_df.nsmallest(10, 'activity')

    # Kiểm tra kết quả sau khi lọc
    if filtered_df.empty:
        print("No suitable medications found for your condition.")
        return []
    
    # Lấy danh sách tên thuốc
    drug_names = filtered_df.head(5)['drug_name'].tolist()
    print(drug_names)
    return drug_names


