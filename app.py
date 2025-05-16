import streamlit as st
from openai import OpenAI
# from dotenv import load_dotenv
import os

# Load environment variables from .env file
# load_dotenv()
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
    st.stop()

client = OpenAI(api_key=api_key)

def call_llm(prompt, input_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_text},
        ],
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

st.set_page_config(page_title="Smart Document Editor", page_icon="✍️")

st.title("Smart Document Editor ✍️")
st.write("Paste your text below and use the buttons to enhance your writing with AI:")

# Input area for user's text
text_input = st.text_area(
    "Your document text here...",
    height=300,
    placeholder="Type or paste your document here..."
)

col1, col2, col3, col4 = st.columns(4)
action = None

with col1:
    if st.button("Summarize"):
        action = "summarize"
with col2:
    if st.button("Rewrite (Formal)"):
        action = "rewrite_formal"
with col3:
    if st.button("Improve Clarity"):
        action = "clarify"
with col4:
    if st.button("Make Concise"):
        action = "concise"

output = ""

if action and text_input.strip():
    if action == "summarize":
        prompt = "Summarize the following text in 3-4 sentences."
    elif action == "rewrite_formal":
        prompt = "Rewrite the following text in a more formal and professional tone."
    elif action == "clarify":
        prompt = "Improve the clarity of the following text. Make it easy to understand."
    elif action == "concise":
        prompt = "Rewrite the following text to be more concise without losing important information."
    else:
        prompt = ""
    with st.spinner("AI is working..."):
        try:
            output = call_llm(prompt, text_input)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            output = ""

    if output:
        st.subheader("Editable AI Output")
        edited_output = st.text_area("Edit the AI's output as you wish:", value=output, height=250, key="output_editor")
        st.download_button("Download Output", edited_output, file_name="output.txt")
else:
    if action and not text_input.strip():
        st.warning("Please enter some text to process.")

st.markdown("---")
st.markdown("Powered by [OpenAI](https://openai.com) • Chadi Abi Fadel")
