from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import updated_main  #Contains the code for generating the blog

app = FastAPI()

# Mount the 'static' directory to serve static files like style.css and 1.css
app.mount("/static", StaticFiles(directory="static"), name="static")

class BlogInput(BaseModel):
    topic: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    """
    Endpoint to render the root page.

    Returns:
        HTMLResponse: HTML content of the root page.
    """
    return open('Template/semproject.html', 'r').read()

@app.get("/about.html", response_class=HTMLResponse)
def read_about():
    """
    Endpoint to render the about page.

    Returns:
        HTMLResponse: HTML content of the about page.
    """
    return open('Template/about.html', 'r').read()

@app.get("/contact.html", response_class=HTMLResponse)
def read_contact():
    """
    Endpoint to render the contact page.

    Returns:
        HTMLResponse: HTML content of the contact page.
    """
    return open('Template/contact.html', 'r').read()

@app.get("/1.css", response_class=HTMLResponse)
def read_css():
    """
    Endpoint to serve the 1.css file.

    Returns:
        HTMLResponse: Content of the 1.css file.
    """
    with open("static/1.css", "r") as css_file:
        css_content = css_file.read()
    return HTMLResponse(content=css_content, status_code=200)

@app.post("/generate_blog/")
async def generate_blog(data: BlogInput):
    """
    Endpoint to generate a blog based on the provided topic.

    Args:
        data (BlogInput): Input data containing the blog topic.

    Returns:
        dict: Dictionary containing the result of the blog generation.
    """
    try:
        # Extracting values from the request body
        title = data.topic

        # Call the function from updated_main.py with the extracted values
        blog_content = updated_main.generate_blog(title)

        return {'blog_result': blog_content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
