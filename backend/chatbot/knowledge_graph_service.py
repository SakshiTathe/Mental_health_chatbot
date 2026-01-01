# knowledge_graph_service.py
import networkx as nx
import os
import pickle
from datetime import datetime

class KnowledgeGraphService:
    def __init__(self, graph_path="chatbot/models/Knowledge_graph.gpickle"):
        self.graph_path = graph_path
        if os.path.exists(graph_path):
            try:
                self.graph = nx.read_gpickle(graph_path)
                print(" Loaded existing Knowledge Graph.")
            except Exception:
                with open(graph_path, "rb") as f:
                    self.graph = pickle.load(f)
                print(" Loaded Knowledge Graph using pickle (compatibility mode).")
        else:
            self.graph = nx.DiGraph()
            print(" Created new Knowledge Graph.")
    
    def add_summary(self, user_id, summary_text):
        print("not added")
        timestamp = datetime.utcnow().isoformat()
        node_id = f"{user_id}_{timestamp}"
        self.graph.add_node(
            node_id,
            user_id=str(user_id),
            summary=summary_text,
            timestamp=timestamp
        )
        last = self.graph.graph.get(f"last_summary_{user_id}")
        #last = self.get_last_summary_node(user_id)
        if last:
            self.graph.add_edge(last, node_id, relation="next")
        self.graph.graph[f"last_summary_{user_id}"] = node_id
        self._save()
    
    def get_last_summary_node(self, user_id):
        return self.graph.graph.get(f"last_summary_{user_id}")
    
    def get_all_summaries(self, user_id):
        summaries = []
        node = self.get_last_summary_node(user_id)
        while node:
            data = self.graph.nodes[node]
            summaries.append(data["summary"])
            preds = list(self.graph.predecessors(node))
            node = preds[0] if preds else None 
        return list(reversed(summaries))
    
    def get_recent_summaries(self, user_id, limit=2):
        node = self.get_last_summary_node(user_id)
        if not node:
            return []
        summaries = []
        while node and len(summaries) < limit:
            data = self.graph.nodes[node]
            summaries.append(data["summary"])
            preds = list(self.graph.predecessors(node))
            node = preds[0] if preds else None
        return list(reversed(summaries))  # so older first → newer last


    def _save(self):
        nx.write_gpickle(self.graph, self.graph_path)