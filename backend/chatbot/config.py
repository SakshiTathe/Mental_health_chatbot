# config.py
EMOTION_MAP = {
    0:"admiration", 1:"amusement", 2:"anger", 3:"annoyance", 4:"approval",
    5:"caring", 6:"confusion", 7:"curiosity", 8:"desire", 9:"disappointment",
    10:"disapproval", 11:"disgust", 12:"embarrassment", 13:"excitement", 14:"fear",
    15:"gratitude", 16:"grief", 17:"joy", 18:"love", 19:"nervousness", 20:"optimism",
    21:"pride", 22:"realization", 23:"relief", 24:"remorse", 25:"sadness",
    26:"surprise"
}
AVAILABLE_TOPICS = [
    'adhd','biopolar','ptsd','depression', 'anxiety', 'counseling-fundamentals', 'intimacy',
    'relationshipsandsocialdynamics', 'initial-screening','schizophrenia'
]
dialogues_path="./diags"
api_key="AIzaSyB-CFP9Bf61ot4G4CyiKMsq97jg9Q1B1tI"
gemini_model = "gemini-2.5-flash"

#flask, pandas, pymongo, faiss-cpu, sentence-transformers dotenv
#util torch re numpy emoji nltk,google-generativeai, tensorflow tf-keras
#venv\Scripts\activate
Dieases={'ADHD': 0,'Anxiety': 1,'Autism': 2,'BPD': 3,'Bipolar': 4,'Depression': 5,'schizophrenia': 6}

#pip install scikit-learn==1.6.1 E:\IMPORTANT\internship\backend\chatbot\venv\Lib\site-packages\sklearn\base.py:442: InconsistentVersionWarning: Trying to unpickle estimator LabelEncoder from version 1.6.1 when using version 1.7.2. This might lead to breaking code or invalid results. Use at your own risk. For more info please refer to:
#https://scikit-learn.org/stable/model_persistence.html#security-maintainability-limitations      
# warnings.warn(

for value in AVAILABLE_TOPICS:
    print(value,end=',',)
print(len(EMOTION_MAP))

