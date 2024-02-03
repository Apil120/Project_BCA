# Importing necessary libraries
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.tools import tool
import os
import json
from langchain.agents import load_tools
from langchain.llms import OpenAI
from langchain.tools import DuckDuckGoSearchRun

# Getting API keys
api_key = os.environ.get('OPENAI_API_KEY')  # Use get to avoid KeyError if the key is not set

# Initializing Language Model (LLM) and search tool
llm1 = OpenAI()  # Choosing LLM
search = DuckDuckGoSearchRun()#Search Tool 

# Retrieve input data from the request
def get_input_data():
    try:
        request_data = json.loads(input())  # Assuming the input is in JSON format(If it's not, than our code will turn to JSON)
        topic = request_data['topic']
        return topic
    except Exception as e:
        raise ValueError("Invalid input format")

# Run the blog generation process
def generate_blog(title):
    try:
        # Running a search to get relevant information for the blog
        search_result = search.run(title)
        # Defining prompt
        prompt = f"""
        Generate a blog post with the following topic: "{title}". \
        The blog post should be concise and contain approximately 500 words. \
        Incorporate relevant information about {title} and provide insights into its applications.
        Use the content from {search_result} in your response as well. \
        Avoid abrupt endings and ensure that the response is complete.\
        Your output should be in the format shown below:\
        'Blog Title':{title}"\n"
        'Your generated content'

        """
        result = llm1.invoke(prompt, max_tokens=750)

        # Documenting chat history in a .txt file
        with open("static/Chat_history_Project.txt", "a") as file:
            file.write(f"User: {title}\n")
            file.write(f"Response: {result}\n\n")
     
        
        return result#Returning the blog
    #Exception Handling
    except Exception as e:
        print(f"Error: {e}")
        return str(e)