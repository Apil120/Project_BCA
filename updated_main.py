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
        num_words = int(request_data['num_words'])
        return topic, num_words
    except Exception as e:
        raise ValueError("Invalid input format")

# Run the blog generation process
def generate_blog():
    try:
        # Retrieve input data
        topic, num_words = get_input_data()

        # Running a search to get relevant information for the blog
        search_result = search.run(topic)

        # Calculating maximum words allowed
        max_words = num_words + 50
        if max_words < 0:
            max_words = max_words * -1

        # Defining prompt
        prompt = f"""
        Your task is to create a new blog on a topic of in about {num_words} words.\
        The maximum number of words that you can use is {max_words}.\
        DO NOT MAKE THE OUTPUT HAVE LESS WORDS THAN {num_words}.\
        You can use any relevant information or quotes that come up during this process.\
        You should create a title for the blog as well.\
        Incorporate content from {search_result} in the response as well.\
        Your response should be in JSON format.\
        Add the contents from as you seem fit.\
        DO NOT HALLUCINATE.
        ##Topic:{topic}
        """

        # Generating blog using the Language Model
        result = llm1.invoke(prompt)

        # Display the generated blog
        print(result)

        # Documenting chat history in a .txt file
        with open("Chat_history_Project.txt", "a") as file:
            file.write(f"User: {topic}\n")
            file.write(f"Response: {result}\n\n")

        with open("responses.txt", "a") as file:
            file.write(f"Blog: {result}\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_blog()
