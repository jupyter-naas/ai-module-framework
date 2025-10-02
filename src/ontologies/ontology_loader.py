import os
import json
from typing import Dict, List, Optional

class OntologyLoader:
    """Simple ontology loader for context management"""
    
    def __init__(self):
        self.ontology_data = {}
        self.current_ontology = None
    
    def load_ontology(self, ontology_path: str) -> bool:
        """Load ontology from file"""
        try:
            if ontology_path.endswith('.json'):
                with open(ontology_path, 'r') as f:
                    self.ontology_data = json.load(f)
            elif ontology_path.endswith('.ttl') or ontology_path.endswith('.rdf'):
                # For now, just store the file path for RDF files
                self.ontology_data = {"file_path": ontology_path, "type": "rdf"}
            else:
                return False
            
            self.current_ontology = ontology_path
            return True
        except Exception as e:
            print(f"Error loading ontology: {e}")
            return False
    
    def get_ontology_context(self) -> str:
        """Get ontology as context string"""
        if not self.ontology_data:
            return "No ontology loaded."
        
        if isinstance(self.ontology_data, dict) and "file_path" in self.ontology_data:
            return f"Ontology loaded from: {self.ontology_data['file_path']}"
        
        # Convert JSON ontology to readable context
        context = "Current Ontology Context:\n"
        context += f"Loaded from: {self.current_ontology}\n\n"
        
        if isinstance(self.ontology_data, dict):
            context += self._format_json_ontology(self.ontology_data)
        
        return context
    
    def _format_json_ontology(self, data: Dict, indent: int = 0) -> str:
        """Format JSON ontology data as readable text"""
        result = ""
        spaces = "  " * indent
        
        for key, value in data.items():
            if isinstance(value, dict):
                result += f"{spaces}{key}:\n"
                result += self._format_json_ontology(value, indent + 1)
            elif isinstance(value, list):
                result += f"{spaces}{key}:\n"
                for item in value:
                    if isinstance(item, dict):
                        result += self._format_json_ontology(item, indent + 1)
                    else:
                        result += f"{spaces}  - {item}\n"
            else:
                result += f"{spaces}{key}: {value}\n"
        
        return result
    
    def query_ontology(self, query: str) -> str:
        """Simple ontology query (placeholder for more complex queries)"""
        if not self.ontology_data:
            return "No ontology loaded to query."
        
        # Simple keyword search in the ontology data
        query_lower = query.lower()
        results = []
        
        def search_in_data(data, path=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    current_path = f"{path}.{key}" if path else key
                    if query_lower in key.lower():
                        results.append(f"{current_path}: {value}")
                    if isinstance(value, (dict, list)):
                        search_in_data(value, current_path)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    current_path = f"{path}[{i}]"
                    if isinstance(item, (dict, list)):
                        search_in_data(item, current_path)
                    elif query_lower in str(item).lower():
                        results.append(f"{current_path}: {item}")
            elif query_lower in str(data).lower():
                results.append(f"{path}: {data}")
        
        search_in_data(self.ontology_data)
        
        if results:
            return f"Found {len(results)} matches for '{query}':\n" + "\n".join(results[:10])
        else:
            return f"No matches found for '{query}' in the ontology."
