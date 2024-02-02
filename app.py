from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import subprocess
import sys
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="Template")  # Update this line to specify the correct template directory

class BlogRequest(BaseModel):
    topic: str
    num_words: int

python_path = sys.executable

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("semproject.html", {"request": request})

@app.post("/generate_blog/")
async def generate_blog(blog_request: BlogRequest):
    try:
        # Getting the absolute path to the Python interpreter
        python_path = sys.executable
        # Getting the absolute path to the current script
        script_path = os.path.abspath("updated_main.py")
        # Creating the command
        command = [
            python_path,
            script_path,
            blog_request.topic,
            str(blog_request.num_words),
        ]
        # Running the command
        result = subprocess.run(
            command, capture_output=True, text=True, check=True
        )
        return {"blog_result": result.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error executing script: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# Serve the responses.txt file
@app.get("/static/responses.txt", response_class=FileResponse)
async def read_responses():
    return FileResponse("responses.txt", media_type="text/plain")
