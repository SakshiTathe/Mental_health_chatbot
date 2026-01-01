# rag_system.py
import os
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from chatbot.config import AVAILABLE_TOPICS,api_key,dialogues_path
import pickle

class RAGSystem:
    def __init__(self):
        print(" Initializing RAG System...")
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel("gemini-2.5-flash")
        self.encoder_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.rag_contexts = {}
        self._load_dialogues()
        print(" RAG System Initialized.")

    def _load_dialogues(self):
        for topic in AVAILABLE_TOPICS:
            filepath = os.path.join(dialogues_path, f"{topic}.csv")
            if os.path.exists(filepath):
                df = pd.read_csv(filepath)

                docs = (df['questionText'].astype(str) + " " + df['answerText'].astype(str)).dropna().tolist()
                embeddings = self.encoder_model.encode(docs, convert_to_tensor=True).cpu().numpy().astype("float32")
                index = faiss.IndexFlatL2(embeddings.shape[1])
                index.add(embeddings)
                self.rag_contexts[topic] = {'docs': docs, 'index': index}


    def get_rag_context(self, query, topic, k=2):
        if(topic=="physical-activity"):
            """ index = faiss.read_index("chatbot/models/exercise_index.faiss")
            with open("chatbot/models/exercise_docs.pkl", "rb") as f:
                docs = pickle.load(f)
            q_emb = self.encoder_model.encode([query]).astype("float32")
            _, idx = index.search(q_emb, 1)
            retrieved = " ".join([self.exercise_docs[i] for i in idx[0]])
            """
            prompt = f"""Provide the Exercises activity to the user
            """
            return prompt

        context_data = self.rag_contexts.get(topic, self.rag_contexts.get('counseling-fundamentals'))
        print(context_data)
        if not context_data:
            return ""
        q_embed = self.encoder_model.encode([query]).astype("float32")
        _, indices = context_data['index'].search(q_embed, k)
        return ' '.join([context_data['docs'][i] for i in indices[0]])
        
    def generate_final_response(self, user_message, topic, lang,past_summaries=None):
        rag_context_str = self.get_rag_context(user_message, topic)
        summaries_str = ""
        if past_summaries:
            summaries_str = "\nPast user summaries:\n" + "\n".join(past_summaries)
        print(past_summaries)
        lang_instructions = {
            "hinglish": "Respond naturally in Hinglish with empathy.",
            "hindi": "Respond in simple Hindi empathetically.",
            "english": "Respond in English naturally and empathetically."
        }

        prompt = f"""
        You are a compassionate mental health chatbot. The user is talking about '{topic}'.
        Instruction: {lang_instructions.get(lang, lang_instructions['english'])}
        {summaries_str}
        Use these dialogue examples for tone: "{rag_context_str}"
        User's message: "{user_message}"

        Provide a supportive, brief, and natural response.add some slangs to look conversation more user friendly
        """
        response = self.gemini_model.generate_content(prompt)
        return response.text.strip()

    def translate_text(self, text, target_language="English"):
        prompt = f"Translate the following text to {target_language}, preserving the emotional tone: \"{text}\". Output only the translation."
        response = self.gemini_model.generate_content(prompt)
        return response.text.strip()

    def summarize_for_knowledge(self, user_message):
        prompt = f"""
        Analyze this user's message. Extract the primary mental health concern, key symptoms, and potential triggers.
        Message: "{user_message}"
        Summary:
        """
        response = self.gemini_model.generate_content(prompt)
        return response.text.strip()
    
    def predict_disease(self, user_message):
        topic_list_str = ", ".join(AVAILABLE_TOPICS)
        prompt = f"""
            You are a classifier. 
            Your job: Identify which topic the user message belongs to.
            Choose ONLY from this list:
            {topic_list_str}
            User message:
            "{user_message}"
            Return ONLY the topic name. No explanation.
            """
        response = self.gemini_model.generate_content(prompt)
        predicted = response.text.strip().lower()
        for topic in AVAILABLE_TOPICS:
            if topic.lower() == predicted:
                return topic
        return "counseling-fundamentals"
