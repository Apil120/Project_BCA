from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import updated_main  # assuming updated_main.py contains the code for generating the blog

app = FastAPI()

# Mount the 'static' directory to serve static files like style.css and 1.css
app.mount("/static", StaticFiles(directory="static"), name="static")

class BlogInput(BaseModel):
    topic: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    return open('Template/semproject.html', 'r').read()

@app.get("/about.html", response_class=HTMLResponse)
def read_about():
    return open('Template/about.html', 'r').read()

@app.get("/contact.html", response_class=HTMLResponse)
def read_contact():
    return open('Template/contact.html', 'r').read()

@app.get("/1.css", response_class=HTMLResponse)
def read_css():
    with open("static/1.css", "r") as css_file:
        css_content = css_file.read()
    return HTMLResponse(content=css_content, status_code=200)

@app.post("/generate_blog/")
async def generate_blog(data: BlogInput):
    try:
        # Extracting values from the request body
        title = data.topic

        # Call the function from updated_main.py with the extracted values
        blog_content = updated_main.generate_blog(title)

        return {'blog_result': blog_content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
