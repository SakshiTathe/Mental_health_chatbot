""" 
from chatbot.analysis_service import AnalysisService
analysis_service = AnalysisService()
english_message="I feel incredibly happy today!"
emotion = analysis_service.detect_emotion(english_message)
print(english_message,":",emotion) """
""" 
message="main concentrate nahi kar pa raha"
original_lang = analysis_service.detect_language(message)
print("user text:",message)
print("original_lang:",original_lang) 

message="Give me some breathing exercises"
exercise = analysis_service.detect_exercise(message)
print("user text:",message)
print("user need exercies or not:",exercise)
"""
""" from chatbot.knowledge_graph_service import KnowledgeGraphService
graph=KnowledgeGraphService()
get_summary=graph.get_recent_summaries("691f384fdc1688c783f09e09")
print(get_summary) """