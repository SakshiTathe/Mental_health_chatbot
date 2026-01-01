# analysis_service.py
import re
# Assuming 'predictor' is your loaded emotion detection model
# from your_emotion_model_file import predictor
from chatbot.config import AVAILABLE_TOPICS, EMOTION_MAP
from chatbot.hinglish import set1,exercise_keywords
from chatbot.empredict import EmotionPredictor
import os


class AnalysisService:
    _emotion_model = None
    def __init__(self):
        print(" Initializing Analysis Service...")
        #self.encoder_model = SentenceTransformer('all-MiniLM-L6-v2')
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        if AnalysisService._emotion_model is None:
            AnalysisService._emotion_model = EmotionPredictor(
                lstm_model_path=os.path.join(BASE_DIR, "models/lstm_model2.h5"),
                tokenizer_path=os.path.join(BASE_DIR, "models/tokenizer2.pkl"),
                label_encoder_path=os.path.join(BASE_DIR, "models/label_encoder2.pkl")
            )

        self.emotion_predictor = AnalysisService._emotion_model

        """ self.disease_predictor = DisorderPredictor(
            gru_model_path=os.path.join(BASE_DIR,'models/gru_model.h5'),
            tokenizer_path=os.path.join(BASE_DIR,'models/tokenizer.pkl'),
            label_encoder_path=os.path.join(BASE_DIR,'models/label_encoder.pkl')
        ) """
        print(" Analysis Service Initialized.")

    def detect_language(self, text):
        if re.search("[\u0900-\u097F]", text):
            return "hindi"
        #words = set(text.lower().split()) matches = [w for w in words if w in set1] phrase_hits = [p for p in set1 if p in text]
        words = set(re.findall(r"\b\w+\b", text.lower()))
        matches = [w for w in words if w in set1]
        phrase_hits = [
            p for p in set1
            if re.search(rf"\b{re.escape(p)}\b", text.lower())  # exact phrase, not substring
        ]
        if phrase_hits or (len(matches) / max(len(words),1) > 0.2):
            return "hinglish"
        return "english"

    def detect_exercise(self,text):
        words = set(re.findall(r"\b\w+\b", text.lower()))
        matches = [w for w in words if w in exercise_keywords]
        phrase_hits = [
            phrase for phrase in exercise_keywords
            if re.search(rf"\b{re.escape(phrase)}\b", text.lower())
        ]
        if phrase_hits or (len(matches) / max(len(words), 1) > 0.20):
            return True
        return False

    def detect_emotion(self, text):
        try:
            result = self.emotion_predictor.predict(text)
            print(result)
            # Ensure result returns something like {'category': idx, 'label': 'joy'}
            if isinstance(result, dict):
                if 'category' in result:
                    return EMOTION_MAP.get(result['category'], "neutral")
            elif isinstance(result, str):
                return result
            else:
                return "neutral"
        except Exception as e:
            print(f"Emotion detection error: {e}")
            return "neutral"

    """ def detect_disease(self, text):
        if not text or not isinstance(text, str):
            return {"category": "Unknown", "confidence": 0.0}

        try:
            result = self.disease_predictor.predict(text, model_type='gru')
            # Extract predicted disease and confidence
            disease = result.get("category", "Unknown")
            confidence = result.get("confidence", 0.0)
            # Optional: Add a confidence threshold
            if confidence < 0.5:
                disease = "Uncertain"
            print(f"[Disease Detection] {disease} ({confidence:.2f})")
            return {"category": disease, "confidence": confidence}
        except Exception as e:
            print(f"Error in detect_disease: {e}")
            #return {"category": "Error", "confidence": 0.0}
            return 'counseling-fundamentals' """