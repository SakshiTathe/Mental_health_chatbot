import numpy as np
import nltk
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TF_NUM_INTEROP_THREADS"] = "1"
os.environ["TF_NUM_INTRAOP_THREADS"] = "1"
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

class EmotionPredictor:
    def __init__(self, lstm_model_path, tokenizer_path, label_encoder_path):
        # --- Paths to assets ---
        self.lstm_model_path = lstm_model_path
        self.tokenizer_path = tokenizer_path
        self.label_encoder_path = label_encoder_path
        self.gru_model = None
        self.tokenizer = None
        self.label_encoder = None
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.max_len = 200 # Must be the same as used in training

        self._load_assets()

    def _clean_text(self, text):
        text = str(text).lower()
        words = nltk.word_tokenize(text)
        words = [self.lemmatizer.lemmatize(w) for w in words if w not in self.stop_words and len(w) > 2]
        return ' '.join(words)

    def _load_assets(self):
        print("Loading prediction models and assets...")
        try:
            self.gru_model = load_model(self.lstm_model_path, compile=False)
            print(" Model loaded")
            with open(self.tokenizer_path, 'rb') as f:
                self.tokenizer = pickle.load(f)
            print(" Tokenizer loaded")
            with open(self.label_encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
            print("Assets loaded successfully.")
        except Exception as e:
            print(f"Error loading assets: {e}")

    def predict(self, text):
        if not all([self.gru_model, self.tokenizer, self.label_encoder]):
            return {"error": "Models or assets not loaded."}
            
        # 1. Preprocess the input text
        cleaned_text = self._clean_text(text)
        
        # 2. Tokenize and pad
        sequence = self.tokenizer.texts_to_sequences([cleaned_text])
        padded_sequence = pad_sequences(sequence, maxlen=self.max_len)
        
        model = self.gru_model
        # 3. Choose model and predict
        prediction = model.predict(padded_sequence)
        
        # 4. Decode the prediction
        predicted_class_index = np.argmax(prediction, axis=1)[0]
        confidence = float(np.max(prediction, axis=1)[0])
        predicted_category = self.label_encoder.inverse_transform([predicted_class_index])[0]
        
        return {
            "category": predicted_category,
            "confidence": confidence
        }
