# chatbot_service.py
from chatbot.rag_system import RAGSystem
#from rag_system import RAGSystem
from chatbot.database_manager import DatabaseManager
from chatbot.knowledge_graph_service import KnowledgeGraphService
import networkx as nx

class ChatbotService:
    def __init__(self, users_collection,chat_collection,analysis_service):
        self.rag_system = RAGSystem()
        self.analysis_service = analysis_service
        self.db_manager = DatabaseManager(users_collection=users_collection,chat_collection=chat_collection)
        self.knowledge_graph_service = KnowledgeGraphService()
        
    def handle_chat_request(self, user_id, message):
        # 1. Detect original language
        original_lang = self.analysis_service.detect_language(message)
        print("original_lang:",original_lang)
        # 2. Translate to English if needed for processing
        english_message = message
        if original_lang in ["hindi", "hinglish"]:
            english_message = self.rag_system.translate_text(message, target_language="English")
        # 3. Get user data and determine disease/topic
        user_doc = self.db_manager.get_user_by_id(user_id)
        print(user_doc)
        disease = user_doc.get("topic") if user_doc else None

        # 4. Detect emotion from the English message
        emotion = self.analysis_service.detect_emotion(english_message)
        print("english_message:", english_message, emotion)
        exercise=self.analysis_service.detect_exercise(english_message)
        if (exercise):
            bot_response = self.rag_system.generate_final_response(
            english_message,"physical-activity",original_lang,past_summaries=None)
            self.db_manager.save_chat_history(user_id, message, bot_response, emotion)
            return {"reply": bot_response,"emotion": emotion}
        
        # 5. Summarize message for knowledge graph/future use (optional)
        summary = self.rag_system.summarize_for_knowledge(english_message)

        # You can now store this 'summary' in a separate collection or knowledge graph
        print(f"Knowledge Summary for {user_id}: {summary}")
        self.knowledge_graph_service.add_summary(
            user_id=user_id,
            summary_text=summary
        )
        if disease is None or not disease:
            print("dieases.............")
            message_history = self.db_manager.get_recent_user_messages(user_id, limit=10) or []
            print("messages")
            # Phase 1: RAG screening phase for new user
            if len(message_history) < 10:
                topic = "initial-screening"  # Force topic
                past_summaries = self.knowledge_graph_service.get_recent_summaries(user_id,limit=3)
                bot_response = self.rag_system.generate_final_response(
                    english_message,topic,original_lang,past_summaries=None)
                self.db_manager.save_chat_history(user_id, message, bot_response, emotion)
                return {"reply": bot_response,"emotion": emotion}
            else:
                combined_text = " ".join(message_history)
                disease = self.rag_system.predict_disease(combined_text)
                self.db_manager.create_or_update_user_disease(user_id, disease)

        # 6. Generate the RAG response in the original language
        past_summaries = self.knowledge_graph_service.get_recent_summaries(user_id,limit=3)
        bot_response = self.rag_system.generate_final_response(english_message, disease, original_lang,past_summaries)

        # 7. Save the conversation to the database
        self.db_manager.save_chat_history(user_id, message, bot_response, emotion)

        # 8. Return the final payload
        print(emotion)
        return {
            "reply": bot_response,
            "disease": disease,
            "emotion": emotion
        }