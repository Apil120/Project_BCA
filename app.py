from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import subprocess
import sys
import os
import asyncio
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="Template")


class BlogRequest(BaseModel):
    topic: str
    num_words: int

python_path = sys.executable

async def run_updated_main(topic: str, num_words: int):
    try:
        # Getting the absolute path to the Python interpreter
        python_path = sys.executable
        # Getting the absolute path to the current script
        script_path = os.path.abspath("updated_main.py")
        # Creating the command
        command = [
            python_path,
            script_path,
            topic,
            str(num_words),
        ]
        # Running the command asynchronously
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the process to finish
        stdout, stderr = await process.communicate()
        return {"blog_result": stdout.decode()}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error executing script: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("semproject.html", {"request": request})


@app.post("/generate_blog/")
async def generate_blog(blog_request: BlogRequest):
    result = await run_updated_main(blog_request.topic, blog_request.num_words)
    return result

