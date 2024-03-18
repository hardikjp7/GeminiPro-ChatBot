import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Agri-Bot",
    page_icon="🌾",  # Favicon emoji for agriculture
    layout="centered",  # Page layout option
)

# Sidebar to input Google API Key
st.sidebar.title("Agriculture Chatbot Configuration")
GOOGLE_API_KEY = st.sidebar.text_input("Enter your Google API Key", type="password")
# Guide for obtaining Google API Key if not available
st.sidebar.subheader("Don't have a Google API Key?")
st.sidebar.write("Visit [Google Makersuite](https://makersuite.google.com/app/apikey) and log in with your Google account. Then click on 'Create API Key'.")


# Check if API key is provided
if not GOOGLE_API_KEY:
    st.error("Please enter your Google API Key.")
    st.stop()

# Set up Google Agriculture AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-1.0-pro')

# Function to translate roles between Agriculture-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("🌾 Agriculture Chatbot")

# Add small text below the header
st.markdown("Made by 😎 [Hardik](https://www.linkedin.com/in/hardikjp/)")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Agriculture-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Agriculture-Pro and get the response
    agriculture_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Agriculture-Pro's response
    with st.chat_message("assistant"):
        st.markdown(agriculture_response.text)
