"""
Pipeline Manager for the AI Module Framework
"""

from typing import Dict, List, Any, Callable
import json

class PipelineManager:
    """Manages data processing pipelines"""
    
    def __init__(self):
        self.pipelines: Dict[str, Dict] = {}
        self.pipeline_functions: Dict[str, Callable] = {}
    
    def create_pipeline(self, name: str, steps: List[Dict]) -> str:
        """Create a pipeline with steps"""
        pipeline = {
            "name": name,
            "steps": steps,
            "status": "created"
        }
        self.pipelines[name] = pipeline
        return f"Pipeline '{name}' created with {len(steps)} steps"
    
    def register_pipeline_function(self, name: str, function: Callable):
        """Register a function for pipeline execution"""
        self.pipeline_functions[name] = function
    
    def execute_pipeline(self, name: str, data: Any = None) -> Dict[str, Any]:
        """Execute a pipeline"""
        if name not in self.pipelines:
            return {"error": f"Pipeline '{name}' not found"}
        
        pipeline = self.pipelines[name]
        
        # If there's a registered function, use it
        if name in self.pipeline_functions:
            try:
                result = self.pipeline_functions[name](data)
                return {"success": True, "result": result}
            except Exception as e:
                return {"error": f"Pipeline execution failed: {str(e)}"}
        
        # Otherwise, simulate step-by-step execution
        try:
            results = []
            for i, step in enumerate(pipeline["steps"]):
                step_result = {
                    "step": i + 1,
                    "name": step.get("name", f"Step {i + 1}"),
                    "status": "completed",
                    "result": f"Processed: {step}"
                }
                results.append(step_result)
            
            return {
                "success": True,
                "pipeline": name,
                "steps": results
            }
        except Exception as e:
            return {"error": f"Pipeline execution failed: {str(e)}"}
    
    def list_pipelines(self) -> List[str]:
        """List all pipelines"""
        return list(self.pipelines.keys())
    
    def get_pipeline(self, name: str) -> Dict:
        """Get pipeline definition"""
        return self.pipelines.get(name, {})
    
    def delete_pipeline(self, name: str) -> bool:
        """Delete a pipeline"""
        if name in self.pipelines:
            del self.pipelines[name]
            if name in self.pipeline_functions:
                del self.pipeline_functions[name]
            return True
        return False
