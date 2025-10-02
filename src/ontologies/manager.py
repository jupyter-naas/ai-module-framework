"""
Ontology Manager for the AI Module Framework
"""

from .ontology_loader import OntologyLoader
from typing import Dict, List, Optional

class OntologyManager:
    """Manages multiple ontologies and their contexts"""
    
    def __init__(self):
        self.ontologies: Dict[str, OntologyLoader] = {}
        self.active_ontology: Optional[str] = None
    
    def load_ontology(self, name: str, file_path: str) -> bool:
        """Load an ontology with a given name"""
        try:
            loader = OntologyLoader()
            success = loader.load_ontology(file_path)
            if success:
                self.ontologies[name] = loader
                if not self.active_ontology:
                    self.active_ontology = name
                return True
            return False
        except Exception as e:
            print(f"Error loading ontology {name}: {e}")
            return False
    
    def set_active_ontology(self, name: str) -> bool:
        """Set the active ontology"""
        if name in self.ontologies:
            self.active_ontology = name
            return True
        return False
    
    def get_active_ontology_context(self) -> str:
        """Get context from the active ontology"""
        if self.active_ontology and self.active_ontology in self.ontologies:
            return self.ontologies[self.active_ontology].get_ontology_context()
        return "No active ontology loaded."
    
    def query_active_ontology(self, query: str) -> str:
        """Query the active ontology"""
        if self.active_ontology and self.active_ontology in self.ontologies:
            return self.ontologies[self.active_ontology].query_ontology(query)
        return "No active ontology loaded to query."
    
    def list_ontologies(self) -> List[str]:
        """List all loaded ontologies"""
        return list(self.ontologies.keys())
    
    def get_ontology_info(self, name: str) -> Optional[Dict]:
        """Get information about a specific ontology"""
        if name in self.ontologies:
            loader = self.ontologies[name]
            return {
                "name": name,
                "context": loader.get_ontology_context(),
                "is_active": name == self.active_ontology
            }
        return None
