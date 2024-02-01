from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.tools import tool
import requests
import os
import streamlit as st
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
api_key = os.environ['OPENAI_API_KEY']
serpapi=os.environ['SERPAPI_API_KEY']
st.title("Blog Generator")
llm1 = OpenAI()

user_input = st.text_input("Enter a topic to create a blog on:")
no_words = st.number_input("Enter the number of words you want in your blog:")
no_words=int(no_words)
if no_words<0:
    no_words=no_words*-1
else:
    pass

tool_names = ["serpapi"]
tools = load_tools(tool_names)

agent = initialize_agent(tools, llm1, agent="zero-shot-react-description", verbose=False)
new=agent.run(user_input)
prompt=f"""
Your task is to create a new blog on the topic of {user_input} in about {no_words} words.\
DO NOT MAKE THE OUTPUT HAVE LESS WORDS THAN {no_words}.\    
You can use any relevant information or quotes that come up during this process.\
You should create a title for the blog as well. If {user_input} is empty, do not generate blogs.\
Incorporate content from {new} in the response as well.\
Add the contents from  as you seem fit.\
DO NOT HALLUCINATE. 
"""
#UI using Streamlit:
if len(user_input)==0:
    st.write("Input text to generate blog! or make sure that the number of words is more than 150 or equal to it")
else :
    result = llm1.invoke(prompt)
    st.text("Blog:")
    st.write("\n")
    st.write(result)
    st.write("\n")
    # st.write("Number of words:", len(result.content.split()))
    with open("Chat_history_Project.txt", "a") as file:
        file.write(f"User: {user_input}\n")
        file.write(f"AI: {result}\n\n")