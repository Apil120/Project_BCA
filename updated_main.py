# Importing necessary libraries
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.tools import tool
import os
import streamlit as st
import pyperclip
from langchain.agents import load_tools
from langchain.llms import OpenAI
from langchain.tools import DuckDuckGoSearchRun

# Getting API keys
api_key = os.environ['OPENAI_API_KEY']

# Defining Title
st.title("Blog Generator")

# Initializing Language Model (LLM) and search tool
llm1 = OpenAI()  # Choosing LLM
search = DuckDuckGoSearchRun()

# Asking for and formatting user input
user_input = st.text_input("Enter a topic to create a blog on:")
no_words = st.number_input("Enter the number of words you want in your blog:")
no_words = int(no_words)

try:
    # Running a search to get relevant information for the blog
    a = search.run(user_input)
except Exception as e:
    st.write("Please Input the title!")

# Calculating maximum words allowed
max_words = no_words + 50
if max_words < 0:
    max_words = max_words * -1

# Defining prompt
try:
    prompt = f"""
    Your task is to create a new blog on a topic of in about {no_words} words.\
    The maximum number of words that you can use is {max_words}.\
    DO NOT MAKE THE OUTPUT HAVE LESS WORDS THAN {no_words}.\
    You can use any relevant information or quotes that come up during this process.\
    You should create a title for the blog as well.\
    Incorporate content from {a} in the response as well.\
    Add the contents from as you seem fit.\
    DO NOT HALLUCINATE.
    ##Topic:{user_input}
    """
except Exception as e:
    pass

# UI using Streamlit
if max_words < 150:
    st.write("Make sure that the number of words is more than 150 or equal to it!")
else:
    # Generating blog using the Language Model
    result = llm1.invoke(prompt)

    # Displaying the generated blog
    st.text("Blog:")
    st.write("\n")
    st.write(result)
    st.write("\n")

    # Copy to clipboard button
    if st.button("Copy"):
        pyperclip.copy(result)

    # Documenting chat history in a .txt file
    with open("Chat_history_Project.txt", "a") as file:
        file.write(f"User: {user_input}\n")
        file.write(f"Response: {result}\n\n")
