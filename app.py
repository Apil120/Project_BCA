from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import subprocess
import sys
import os

app = FastAPI()

# Templates
templates = Jinja2Templates(directory="Template")


class BlogRequest(BaseModel):
    topic: str
    num_words: int

python_path = sys.executable
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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
            updateed_main.py,
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
