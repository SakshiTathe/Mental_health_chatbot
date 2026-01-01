import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

class DisorderPredictor:
    def __init__(self, gru_model_path, tokenizer_path, label_encoder_path):
        # --- Paths to assets ---
        self.gru_model_path = gru_model_path
        self.tokenizer_path = tokenizer_path
        self.label_encoder_path = label_encoder_path
        self.gru_model = None
        self.tokenizer = None
        self.label_encoder = None
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.max_len = 400 # Must be the same as used in training
        
        self._load_assets()

    def _clean_text(self, text):
        text = str(text).lower()
        """ text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        text = re.sub(r'@\w+|#\w+', '', text)
        text = emoji.replace_emoji(text, replace='')
        text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
        text = re.sub(r'\d+', '', text) """
        text = re.sub(r'\s+', ' ', text).strip()
        words = nltk.word_tokenize(text)
        words = [self.lemmatizer.lemmatize(w) for w in words if w not in self.stop_words and len(w) > 2]
        return ' '.join(words)

    def _load_assets(self):
        """Loads all models and preprocessing objects from disk."""
        print("Loading prediction models and assets...")
        try:
            self.gru_model = load_model(self.gru_model_path)
            with open(self.tokenizer_path, 'rb') as f:
                self.tokenizer = pickle.load(f)
            with open(self.label_encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
            print("Assets loaded successfully.")
        except Exception as e:
            print(f"Error loading assets: {e}")

    def predict(self, text, model_type='gru'):
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
