import streamlit as st
import openai
from PyPDF2 import PdfReader

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to interact with OpenAI chatbot
def chat_with_bot(api_key, system_prompt, user_message, chat_history=None):
    if chat_history is None:
        chat_history = []
    
    # Add user message to chat history
    chat_history.append({"role": "user", "content": user_message})
    
    # Create the message payload
    messages = [{"role": "system", "content": system_prompt}] + chat_history
    
    # Call the OpenAI API
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # Change to "gpt-4" if you want,
temperature=0.3,
        messages=messages
    )
    
    # Extract the bot's reply
    bot_reply = response['choices'][0]['message']['content']
    
    # Add bot reply to chat history
    chat_history.append({"role": "assistant", "content": bot_reply})
    
    return bot_reply, chat_history

# Streamlit App
def main():
    st.set_page_config(page_title="PDF Chatbot with OpenAI", layout="wide")
    st.title("🤖 PDF Chatbot")
    st.sidebar.title("Settings")

    # User input for OpenAI API key
    api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

    # Session state to store chat history and system prompt
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = ""

    # File uploader for PDF
    pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if pdf_file is not None:
        # Extract text from the uploaded PDF
        st.session_state.system_prompt = extract_text_from_pdf(pdf_file)
        # st.write("### Extracted Text Preview:")
        # st.write(st.session_state.system_prompt[:500] + "...")
        st.success("PDF processed successfully! You can now chat with the bot.")

    # Chat interface
    if st.session_state.system_prompt:
        st.write("## Chat with the Bot")

        # Display chat history with icons
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.write(f"🧑 **You:** {msg['content']}", unsafe_allow_html=True)
            elif msg["role"] == "assistant":
                st.write(f"🤖 **Bot:** {msg['content']}", unsafe_allow_html=True)

        # Input box at the bottom using st.chat_input
        user_message = st.chat_input("Type your message here...")
        if user_message and api_key:
            bot_reply, st.session_state.chat_history = chat_with_bot(
                api_key,
                st.session_state.system_prompt,
                user_message,
                st.session_state.chat_history,
            )
            st.rerun()  # Refresh the app to show new messages

if __name__ == "__main__":
    main()
