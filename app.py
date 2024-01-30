from fastapi import FastAPI, HTTPException
import subprocess
import os

app = FastAPI()

def run_main_script():
    try:
        # Open a new terminal or command prompt window and run Main.py
        if os.name == 'posix':  # On Unix/Linux
            subprocess.run(['x-terminal-emulator', '-e', 'python', 'main.py'], check=True)
        elif os.name == 'nt':  # On Windows
            subprocess.run(['start', 'cmd', '/k', 'python', 'main.py'], check=True)
        else:
            raise HTTPException(status_code=500, detail="Unsupported operating system")
        
        return {"success": True, "message": "Main.py executed successfully"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error executing Main.py: {e}")

@app.post("/call_main")
def call_main():
    return run_main_script()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
