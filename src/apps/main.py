import os
import sys
import requests
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

# Add src to Python path
sys.path.append('/app/src')
from ontologies.ontology_loader import OntologyLoader

app = FastAPI(title="Simple AI Agent with Ontology")

MODEL_URL = os.getenv("MODEL_URL", "http://host.docker.internal:11434")
ontology_loader = OntologyLoader()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint that uses ontology context with Qwen3"""
    try:
        # Get ontology context
        ontology_context = ontology_loader.get_ontology_context()
        
        # Prepare the message with ontology context
        full_message = f"""Context: {ontology_context}

User Question: {request.message}

Please answer the user's question using the provided ontology context when relevant."""
        
        # Call Ollama API
        response = requests.post(
            f"{MODEL_URL}/api/chat",
            json={
                "model": "qwen2.5-coder:7b",
                "messages": [{"role": "user", "content": full_message}],
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result["message"]["content"]
            return ChatResponse(response=ai_response)
        else:
            return ChatResponse(response=f"Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        return ChatResponse(response=f"Error: {str(e)}")

@app.post("/load-ontology")
async def load_ontology(file: UploadFile = File(...)):
    """Load an ontology file"""
    try:
        # Save uploaded file temporarily
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Load ontology
        success = ontology_loader.load_ontology(file_path)
        
        if success:
            return {"message": f"Ontology loaded successfully from {file.filename}"}
        else:
            return {"error": "Failed to load ontology"}
            
    except Exception as e:
        return {"error": f"Error loading ontology: {str(e)}"}

@app.get("/ontology-context")
async def get_ontology_context():
    """Get current ontology context"""
    return {"context": ontology_loader.get_ontology_context()}

@app.get("/ontologies")
async def list_ontologies():
    """List available ontologies in storage"""
    import os
    storage_path = "/app/storage/ontologies"
    ontologies = []
    
    if os.path.exists(storage_path):
        for file in os.listdir(storage_path):
            if file.endswith(('.json', '.ttl', '.rdf', '.owl')):
                ontologies.append(file)
    
    return {"ontologies": ontologies}

@app.post("/load-ontology-from-storage")
async def load_ontology_from_storage(request: ChatRequest):
    """Load an ontology from storage by filename"""
    try:
        file_path = f"/app/storage/ontologies/{request.message}"
        success = ontology_loader.load_ontology(file_path)
        
        if success:
            return {"message": f"Ontology loaded successfully from storage: {request.message}"}
        else:
            return {"error": f"Failed to load ontology: {request.message}"}
            
    except Exception as e:
        return {"error": f"Error loading ontology: {str(e)}"}

@app.post("/query-ontology")
async def query_ontology(request: ChatRequest):
    """Query the loaded ontology"""
    result = ontology_loader.query_ontology(request.message)
    return {"result": result}

@app.get("/")
async def root():
    return {
        "message": "Simple AI Agent with Ontology Support", 
        "model_url": MODEL_URL,
        "endpoints": {
            "chat": "/chat - Chat with AI using ontology context",
            "load_ontology": "/load-ontology - Upload and load an ontology file",
            "load_ontology_from_storage": "/load-ontology-from-storage - Load ontology from storage by filename",
            "ontologies": "/ontologies - List available ontologies in storage",
            "ontology_context": "/ontology-context - Get current ontology context",
            "query_ontology": "/query-ontology - Query the loaded ontology"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)