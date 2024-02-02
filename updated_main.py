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
search = DuckDuckGoSearchRun()

# Retrieve input data from the request
def get_input_data():
    try:
        request_data = json.loads(input())  # Assuming the input is in JSON format
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
        You can use any relevant information or quotes that come up during this process.\
        You should create a title for the blog as well.\
        Incorporate content from {search_result} in the response as well.\
        Your response should be in JSON format.\
        Add the contents from as you seem fit.\
        DO NOT HALLUCINATE.
        If your response ends abruptly than display upto the last sentence.\
        ##Topic:{title}
        """

        # Generating blog using the Language Model
        result = llm1.invoke(prompt)

        # Documenting chat history in a .txt file
        with open("Chat_history_Project.txt", "a") as file:
            file.write(f"User: {title}\n")
            file.write(f"Response: {result}\n\n")

        with open("responses.txt", "a") as file:
            file.write(f"Blog: {result}\n")

        return result
    except Exception as e:
        print(f"Error: {e}")
        return str(e)