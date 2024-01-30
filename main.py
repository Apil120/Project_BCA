import os
import openai
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

openai.api_key = os.environ['GOOGLE_API_KEY']
st.title("Blog Generator")

user_input = st.text_input("Enter a topic to create a blog on:")
no_words = st.number_input("Enter the number of words you want in your blog:", min_value=100, max_value=15000)
user_style = st.text_input("Enter the style of your blog:")


prompt=f"""
Your task is to create a new blog on the topic of {user_input} in about {no_words} words. The blog should be written to match the style of {user_style}.\
You should create a title for the blog as well.
"""
llm = ChatGoogleGenerativeAI(model="gemini-pro")


#UI using Streamlit:
query=prompt
if query:
    result = llm.invoke(prompt)
    st.text("Chat History:")
    st.write(result.content)
    st.write("Number of words:", len(result.content.split()))