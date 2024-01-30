from fastapi import FastAPI, HTTPException
import subprocess
import os

app = FastAPI()

@app.post("/call_main")
def call_main():
    try:
        # Run Main.py using subprocess
        subprocess.run(['python', 'main.py'], check=True, capture_output=True)
        return {"success": True, "message": "Main.py executed successfully"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error executing Main.py: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
