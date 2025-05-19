import nltk
import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz
import re
from firebase_admin import credentials, firestore
from bs4 import BeautifulSoup
from utils.model_loader import *            

# Download required NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

stop = set(stopwords.words('english'))  # Use set for faster lookups
lemmatizer = WordNetLemmatizer()

def get_closest_match(input_disease, me_condition, similarity_threshold=99):
    max_similarity = 0
    best_match = None

    for disease in me_condition:
        similarity_score = fuzz.token_set_ratio(input_disease, disease)
        if similarity_score > max_similarity:
            max_similarity = similarity_score
            best_match = disease

    # Nếu điểm tương đồng lớn hơn ngưỡng, trả về kết quả
    if max_similarity >= similarity_threshold:
        return best_match
    else:
        return None

def review_to_words(raw_review):
    # 1. Delete HTML
    review_text = BeautifulSoup(raw_review, 'html.parser').get_text()
    # 2. Make a space
    letters_only = re.sub('[^a-zA-Z]', ' ', review_text)
    # 3. lower letters
    words = letters_only.lower().split()
    # 5. Stopwords
    meaningful_words = [w for w in words if not w in stop]
    # 6. lemmitization
    lemmitize_words = [lemmatizer.lemmatize(w) for w in meaningful_words]
    # 7. space join words
    return( ' '.join(lemmitize_words))

# Hàm dự đoán
def predict_condition(text):
    transformed_text = tfidf_vectorizer2.transform([text])
    prediction = condition_model.predict(transformed_text)
    return prediction[0]

def get_top_drug(condition):
    # Lọc các loại thuốc theo điều kiện
    filtered_drugs = drugs[drugs['condition'] == condition]
    
    # Nhóm các thuốc theo tên và tính trung bình của cột rating và userCount
    grouped_drugs = (
        filtered_drugs.groupby('drugName')
        .agg({'rating': 'mean', 'usefulCount': 'mean', 'date': 'first'})
        .reset_index()
    )
    
    # Sắp xếp các thuốc theo rating trung bình (giảm dần) và userCount trung bình (giảm dần)
    sorted_drugs = grouped_drugs.sort_values(by=['rating', 'usefulCount'], ascending=[False, False])
    
    # Trả về tối đa 3 loại thuốc hàng đầu
    return sorted_drugs.head(3).to_dict(orient='records')


