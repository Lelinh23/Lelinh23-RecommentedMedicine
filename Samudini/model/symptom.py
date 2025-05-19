from firebase_admin import credentials, firestore, initialize_app
import numpy as np
import requests
from django.shortcuts import render
from text_processing.matching import *
from utils.model_loader import *

def get_symptoms():
    return choices_symptom

def create_symptom_mapping(symptoms_list, symptom_names):
    symptom_map = [1 if symptom in symptoms_list else 0 for symptom in symptom_names]
    return symptom_map

# Hàm sử dụng API để tra cứu thông tin về thuốc dựa trên danh sách các bệnh và trả về một từ điển chứa tên bệnh và danh sách các loại thuốc phù hợp.
def get_medication_info(disease_list): #get medication using API
    medications_dict = {}
    
    # Đây là endpoint của API FDA, được sử dụng để tra cứu thông tin nhãn thuốc.
    base_url = "https://api.fda.gov/drug/label.json"

    for disease in disease_list:
        # Specify the query parameters for the API call
        params = {
            # Tìm kiếm thuốc có chỉ định sử dụng liên quan đến bệnh hiện tại.
            "search": f"indications_and_usage:{disease}",
            # Giới hạn kết quả trả về tối đa 5 loại thuốc
            "limit": 5
        }

        try:
            # Send a GET request to the API endpoint
            response = requests.get(base_url, params=params)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Extract relevant information from the response
                medication_list = []
                # Trích xuất thông tin thuốc
                for result in data['results']:
                    medication_name = result['openfda'].get('brand_name', None) # Lấy tên thương hiệu của thuốc từ trường result['openfda']['brand_name'] nếu có
                    if medication_name and 'N/A' not in medication_name:  # Loại bỏ giá trị "N/A" không hợp lệ
                        medication_list.append(medication_name[0])
                    
                # Lưu tên thuốc đầu tiên vào danh sách medication_list
                medications_dict[disease] = medication_list
            else:
                 print("error")
                 medications_dict[disease] = ["404-ERROR: connect to internet"]

        except requests.exceptions.RequestException as e:
            print("error 1")
            medications_dict[disease] = ["404-ERROR: connect to internet"]
    print("api func",medications_dict)
    return medications_dict

