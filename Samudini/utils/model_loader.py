import pickle
import pandas as pd
import joblib

def load_model(filename):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading model {filename}: {e}")
        return None

model_N = load_model('D:/DATN/datn/Samudini/file_model/symptoms/DecisionTree-Model (1).sav')
model_med = load_model('drugTree.pkl')
model_dis = load_model('D:/DATN/datn/Samudini/file_model/pre_no_login/pred-dis-4.pkl')

tfidf_vectorizer2 = load_model('D:/DATN/datn/Samudini/file_model/review/tfidf_vectorizer2.pkl')
condition_model = load_model('D:/DATN/datn/Samudini/file_model/review/condition_predictor_dnn.pkl')
df_t = load_model('D:/DATN/datn/Samudini/file_model/review/df_top_1.pkl')

precaution_df = pd.read_csv('D:/DATN/datn/Med_rec/disease_precaution.csv')
drugs = pd.read_csv('D:/Drugs-noDiscover/drugsComTrain_raw.tsv', delimiter='\t')
med = pd.read_csv("D:/DATN/datn/Med_rec/rec-med.csv")
doctype = pd.read_csv("D:/DATN/datn/Med_rec/Doctor_Versus_Disease.csv", encoding='ISO-8859-1')
descrip = pd.read_csv("D:/DATN/Medicine Recommendation System/dataset/description.csv")
# workout chứa các hướng dẫn liên quan đến chế độ ăn uống và thói quen có thể giúp điều trị hoặc phòng ngừa các bệnh lý
workout = pd.read_csv("D:/DATN/Medicine Recommendation System/dataset/workout_df.csv") 
# diets các chế độ ăn uống hoặc thực phẩm 
diets = pd.read_csv("D:/DATN/Medicine Recommendation System/dataset/diets.csv") 

conditions = ['Acne', 'ADHD', 'AIDS/HIV', 'Allergies', "Alzheimer's", 'Angina', 'Anxiety', 'Asthma', 'Bipolar Disorder', 'Bronchitis', 'Cancer', 'Cholesterol', 'Colds & Flu', 'Constipation', 'COPD', 'Depression', 'Diabetes (Type 1)', 'Diabetes (Type 2)', 'Diarrhea', 'Eczema', 'Erectile Dysfunction', 'Gastrointestinal', 'GERD (Heartburn)', 'Gout', 'Hair Loss', 'Hayfever', 'Herpes', 'Hypertension', 'Hypothyroidism', 'IBD (Bowel)', 'Incontinence', 'Insomnia', 'Menopause', 'Migraine', 'Osteoarthritis', 'Osteoporosis', 'Pain', 'Pneumonia', 'Psoriasis', 'Rheumatoid Arthritis', 'Schizophrenia', 'Seizures', 'Stroke', 'Swine Flu', 'UTI', 'Weight Loss', 'Jaundice', 'Urinary tract infection', 'Hepatitis A', 'Malaria', 'Peptic ulcer', 'Hypoglycemia', 'Hepatitis C', 'Varicose veins', 'Impetigo', 'Vertigo', 'Fungal Infections', 'Hepatitis B', 'Hemorrhoids', 'Myocardial infarction', 'Common Cold']

#Mapping Symptoms as indexes in dataset using dictionary
symptom_mapping_d = {'itching': 0, 'dischromic _patches': 1, 'continuous_sneezing': 2, 'chills': 3, 'acidity': 4, 
                'vomiting': 5, 'yellowish_skin': 6, 'abdominal_pain': 7, 'yellowing_of_eyes': 8, 
                'spotting_ urination': 9, 'passage_of_gases': 10, 'high_fever': 11, 
                'extra_marital_contacts': 12, 'increased_appetite': 13, 'dehydration': 14, 'diarrhoea': 15, 
                'breathlessness': 16, 'mucoid_sputum': 17, 'lack_of_concentration': 18, 'stiff_neck': 19, 
                'depression': 20, 'weakness_in_limbs': 21, 'altered_sensorium': 22, 'dark_urine': 23, 
                'muscle_pain': 24, 'mild_fever': 25, 'malaise': 26, 'red_spots_over_body': 27, 'joint_pain': 28, 
                'pain_behind_the_eyes': 29, 'acute_liver_failure': 30, 'swelling_of_stomach': 31, 
                'fast_heart_rate': 32, 'pain_during_bowel_movements': 33, 'cramps': 34, 'swollen_extremeties': 35, 
                'slurred_speech': 36, 'knee_pain': 37, 'unsteadiness': 38, 'pus_filled_pimples': 39, 
                'continuous_feel_of_urine': 40, 'skin_peeling': 41, 'red_sore_around_nose': 42}

symptom_mapping = {'high_fever': 0, 'fatigue': 1, 'vomiting': 2, 'mild_fever': 3, 'itching': 4, 'loss_of_appetite': 5, 'acute_liver_failure': 6, 'joint_pain': 7, 'headache': 8, 'weight_loss': 9, 'dark_urine': 10, 'yellowing_of_eyes': 11, 'muscle_pain': 12, 'abdominal_pain': 13, 'nausea': 14, 'diarrhoea': 15, 'yellowish_skin': 16, 'malaise': 17, 'visual_disturbances': 18, 'chest_pain': 19, 'sweating': 20, 'skin_rash': 21, 'pain_behind_the_eyes': 22, 'breathlessness': 23, 'receiving_blood_transfusion': 24, 'slurred_speech': 25, 'lack_of_concentration': 26, 'fast_heart_rate': 27, 'family_history': 28, 'irritability': 29, 'indigestion': 30, 'chills': 31, 'loss_of_balance': 32, 'cough': 33, 'anxiety': 34, 'red_spots_over_body': 35, 'muscle_weakness': 36, 'lethargy': 37, 'spotting_ urination': 38, 'sunken_eyes': 39, 'watering_from_eyes': 40, 'excessive_hunger': 41, 'acidity': 42, 'distention_of_abdomen': 43, 'history_of_alcohol_consumption': 44, 'neck_pain': 45, 'stomach_pain': 46, 'redness_of_eyes': 47, 'altered_sensorium': 48, 'swelled_lymph_nodes': 49, 'nodal_skin_eruptions': 50, 'swelling_joints': 51, 'skin_peeling': 52, 'painful_walking': 53, 'foul_smell_of urine': 54, 'spinning_movements': 55, 'phlegm': 56, 'silver_like_dusting': 57, 'swelling_of_stomach': 58, 'back_pain': 59, 'rusty_sputum': 60, 'blister': 61, 'knee_pain': 62, 'blurred_and_distorted_vision': 63, 'dizziness': 64, 'burning_micturition': 65, 'cramps': 66, 'swollen_extremeties': 67, 'abnormal_menstruation': 68, 'mucoid_sputum': 69, 'fluid_overload': 70, 'yellow_crust_ooze': 71, 'unsteadiness': 72, 'continuous_sneezing': 73, 'red_sore_around_nose': 74, 'increased_appetite': 75, 'passage_of_gases': 76, 'stiff_neck': 77, 'weakness_of_one_body_side': 78, 'inflammatory_nails': 79, 'pus_filled_pimples': 80, 'brittle_nails': 81, 'depression': 82, 'weakness_in_limbs': 83, 'polyuria': 84, 'weight_gain': 85, 'prominent_veins_on_calf': 86, 'extra_marital_contacts': 87, 'hip_joint_pain': 88, 'throat_irritation': 89, 'drying_and_tingling_lips': 90}

choices_symptom = [('itching', 'Itching'), ('skin_rash', 'Skin rash'), ('nodal_skin_eruptions', 'Nodal skin eruptions'),
                    ('continuous_sneezing', 'Continuous sneezing'), ('shivering', 'Shivering'),
                    ('chills', 'Chills'),('joint_pain', 'Joint pain'),('stomach_pain', 'Stomach pain'),
                    ('acidity', 'Acidity'), ('ulcers_on_tongue', 'Ulcers on tongue'), ('muscle_wasting', 'Muscle wasting'), ('vomiting', 'Vomiting'),
                    ('burning_micturition', 'Burning micturition'), ('spotting_ urination', 'Spotting urination'),
                    ('fatigue', 'Fatigue'), ('weight_gain', 'Weight gain'), ('anxiety', 'Anxiety'),
                    ('cold_hands_and_feets', 'Cold hands and feets'), ('mood_swings', 'Mood swings'),
                    ('weight_loss', 'Weight loss'), ('restlessness', 'Restlessness'), ('lethargy', 'Lethargy'),
                    ('patches_in_throat', 'Patches in throat'), ('irregular_sugar_level', 'Irregular sugar level'),
                    ('cough', 'Cough'), ('high_fever', 'High fever'), ('sunken_eyes', 'Sunken eyes'),
                    ('breathlessness', 'Breathlessness'), ('sweating', 'Sweating'), ('dehydration', 'Dehydration'),
                    ('indigestion', 'Indigestion'), ('headache', 'Headache'), ('yellowish_skin', 'Yellowish skin'),
                    ('dark_urine', 'Dark urine'), ('nausea', 'Nausea'), ('loss_of_appetite', 'Loss of appetite'),
                    ('pain_behind_the_eyes', 'Pain behind the eyes'), ('back_pain', 'Back pain'), ('constipation', 'Constipation'),
                    ('abdominal_pain', 'Abdominal pain'), ('diarrhoea', 'Diarrhoea'), ('mild_fever', 'Mild fever'),
                    ('yellow_urine', 'Yellow urine'), ('yellowing_of_eyes', 'Yellowing of eyes'), ('acute_liver_failure', 'Acute liver failure'),
                    ('fluid_overload', 'Fluid overload'), ('swelling_of_stomach', 'Swelling of stomach'), ('swelled_lymph_nodes', 'Swelled lymph nodes'),
                    ('malaise', 'Malaise'), ('blurred_and_distorted_vision', 'Blurred and distorted vision'), ('phlegm', 'Phlegm'),
                    ('throat_irritation', 'Throat irritation'), ('redness_of_eyes', 'Redness of eyes'), ('sinus_pressure', 'Sinus pressure'),
                    ('runny_nose', 'Runny nose'), ('congestion', 'Congestion'), ('chest_pain', 'Chest pain'), ('weakness_in_limbs', 'Weakness in limbs'),
                    ('fast_heart_rate', 'Fast heart rate'), ('pain_during_bowel_movements', 'Pain during bowel movements'),
                    ('pain_in_anal_region', 'Pain in anal region'), ('bloody_stool', 'Bloody stool'), ('irritation_in_anus', 'Irritation in anus'),
                    ('neck_pain', 'Neck pain'), ('dizziness', 'Dizziness'), ('cramps', 'Cramps'), ('bruising', 'Bruising'),
                    ('obesity', 'Obesity'), ('swollen_legs', 'Swollen legs'), ('swollen_blood_vessels', 'Swollen blood vessels'),
                    ('puffy_face_and_eyes', 'Puffy face and eyes'), ('enlarged_thyroid', 'Enlarged thyroid'), ('brittle_nails', 'Brittle nails'),
                    ('swollen_extremeties', 'Swollen extremities'), ('excessive_hunger', 'Excessive hunger'),
                    ('extra_marital_contacts', 'Extra marital contacts'), ('drying_and_tingling_lips', 'Drying and tingling lips'),
                    ('slurred_speech', 'Slurred speech'), ('knee_pain', 'Knee pain'), ('hip_joint_pain', 'Hip joint pain'),
                    ('muscle_weakness', 'Muscle weakness'), ('stiff_neck', 'Stiff neck'), ('swelling_joints', 'Swelling joints'),
                    ('movement_stiffness', 'Movement stiffness'), ('spinning_movements', 'Spinning movements'), ('loss_of_balance', 'Loss of balance'),
                    ('unsteadiness', 'Unsteadiness'), ('weakness_of_one_body_side', 'Weakness of one body side'),
                    ('loss_of_smell', 'Loss of smell'), ('bladder_discomfort', 'Bladder discomfort'), ('foul_smell_of_urine', 'Foul smell of urine'),
                    ('continuous_feel_of_urine', 'Continuous feel of urine'), ('passage_of_gases', 'Passage of gases'),
                    ('internal_itching', 'Internal itching'), ('toxic_look_(typhos)', 'Toxic look (typhos)'), ('depression', 'Depression'),
                    ('irritability', 'Irritability'), ('muscle_pain', 'Muscle pain'), ('altered_sensorium', 'Altered sensorium'),
                    ('red_spots_over_body', 'Red spots over body'), ('belly_pain', 'Belly pain'), ('abnormal_menstruation', 'Abnormal menstruation'),
                    ('dischromic_patches', 'Dischromic patches'), ('watering_from_eyes', 'Watering from eyes'), ('increased_appetite', 'Increased appetite'),
                    ('polyuria', 'Polyuria'), ('family_history', 'Family history'), ('mucoid_sputum', 'Mucoid sputum'),
                    ('rusty_sputum', 'Rusty sputum'), ('lack_of_concentration', 'Lack of concentration'), ('visual_disturbances', 'Visual disturbances'),
                    ('receiving_blood_transfusion', 'Receiving blood transfusion'), ('receiving_unsterile_injections', 'Receiving unsterile injections'),
                    ('coma', 'Coma'), ('stomach_bleeding', 'Stomach bleeding'), ('distention_of_abdomen', 'Distention of abdomen'),
                    ('history_of_alcohol_consumption', 'History of alcohol consumption'), ('fluid_overload.1', 'Fluid overload.1'),
                    ('blood_in_sputum', 'Blood in sputum'), ('prominent_veins_on_calf', 'Prominent veins on calf'),
                    ('palpitations', 'Palpitations'), ('painful_walking', 'Painful walking'), ('pus_filled_pimples', 'Pus filled pimples'),
                    ('blackheads', 'Blackheads'), ('scurring', 'Scurring'), ('skin_peeling', 'Skin peeling'), ('silver_like_dusting', 'Silver like dusting'),
                    ('small_dents_in_nails', 'Small dents in nails'), ('inflammatory_nails', 'Inflammatory nails'),
                    ('blister', 'Blister'), ('red_sore_around_nose', 'Red sore around nose'), ('yellow_crust_ooze', 'Yellow crust ooze')]