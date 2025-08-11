from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agent import run_agent
from pydantic import BaseModel

app = FastAPI()


class Input(BaseModel):
    input:str
    
    
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(user_input:Input):
    try:
        tool_name, response = run_agent(user_input.input)
        return {
            "tool_called": tool_name,
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)