"""
Workflow Manager for the AI Module Framework
"""

from typing import Dict, List, Any, Callable
import json

class WorkflowManager:
    """Manages workflows and their execution"""
    
    def __init__(self):
        self.workflows: Dict[str, Dict] = {}
        self.workflow_functions: Dict[str, Callable] = {}
    
    def register_workflow(self, name: str, workflow: Dict, function: Callable = None):
        """Register a workflow with optional function"""
        self.workflows[name] = workflow
        if function:
            self.workflow_functions[name] = function
    
    def execute_workflow(self, name: str, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a workflow by name"""
        if name not in self.workflows:
            return {"error": f"Workflow '{name}' not found"}
        
        workflow = self.workflows[name]
        
        # If there's a registered function, use it
        if name in self.workflow_functions:
            try:
                result = self.workflow_functions[name](inputs or {})
                return {"success": True, "result": result}
            except Exception as e:
                return {"error": f"Workflow execution failed: {str(e)}"}
        
        # Otherwise, return workflow definition
        return {"workflow": workflow, "inputs": inputs}
    
    def list_workflows(self) -> List[str]:
        """List all registered workflows"""
        return list(self.workflows.keys())
    
    def get_workflow(self, name: str) -> Dict:
        """Get workflow definition"""
        return self.workflows.get(name, {})
    
    def create_simple_workflow(self, name: str, steps: List[str]) -> str:
        """Create a simple workflow from steps"""
        workflow = {
            "name": name,
            "steps": steps,
            "type": "simple"
        }
        self.workflows[name] = workflow
        return f"Workflow '{name}' created with {len(steps)} steps"