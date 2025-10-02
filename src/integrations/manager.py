"""
Integration Manager for the AI Module Framework
"""

from typing import Dict, List, Any
import requests

class IntegrationManager:
    """Manages external integrations"""
    
    def __init__(self):
        self.integrations: Dict[str, Dict] = {}
        self.active_integrations: List[str] = []
    
    def register_integration(self, name: str, config: Dict):
        """Register an integration"""
        self.integrations[name] = config
    
    def activate_integration(self, name: str) -> bool:
        """Activate an integration"""
        if name in self.integrations:
            if name not in self.active_integrations:
                self.active_integrations.append(name)
            return True
        return False
    
    def deactivate_integration(self, name: str) -> bool:
        """Deactivate an integration"""
        if name in self.active_integrations:
            self.active_integrations.remove(name)
            return True
        return False
    
    def list_integrations(self) -> List[str]:
        """List all registered integrations"""
        return list(self.integrations.keys())
    
    def list_active_integrations(self) -> List[str]:
        """List active integrations"""
        return self.active_integrations.copy()
    
    def get_integration_config(self, name: str) -> Dict:
        """Get integration configuration"""
        return self.integrations.get(name, {})
    
    def test_integration(self, name: str) -> Dict[str, Any]:
        """Test an integration"""
        if name not in self.integrations:
            return {"error": f"Integration '{name}' not found"}
        
        config = self.integrations[name]
        
        # Simple HTTP test for URL-based integrations
        if "url" in config:
            try:
                response = requests.get(config["url"], timeout=5)
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "message": "Integration is reachable"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        return {"success": True, "message": "Integration configuration is valid"}