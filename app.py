import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import time


# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Page settings
st.set_page_config(
    page_title="Nexus - AI Research Agent",
    page_icon="🤖",
    layout="wide"
)
# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.markdown("""
<div style='text-align:center; padding: 20px 0 10px 0;'>

<h1 style='
color:#2563EB;
font-size:48px;
margin-bottom:10px;
'>
🧠 Nexus
</h1>

<p style='
font-size:20px;
color:gray;
margin-top:0;
'>
Your AI Research Agent
</p>

</div>
""", unsafe_allow_html=True)
# Custom UI Styling
st.markdown("""
<style>

/* Entire app */
.stApp {
    background-color: #F5F7FA;
    font-family: 'Segoe UI', sans-serif;
}

/* Main content area */
.main {
    background-color: #F5F7FA;
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 950px;
}

/* Title */
.main-title {
    font-size: 3rem;
    font-weight: bold;
    color: #2563EB;
    margin-bottom: 1rem;
    margin-top: 1rem;
}

/* Chat messages */
/* Chat bubbles */
[data-testid="stChatMessage"] {
    background-color: white;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 16px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}
/* Chat input */
.stChatInput input {
    background-color: white !important;
    border: 2px solid #E5E7EB !important;
    border-radius: 14px !important;
    padding: 14px !important;
    color: black !important;
    font-size: 16px !important;
}

/* Buttons */
.stButton button {
    width: 100%;
    border-radius: 10px;
    background-color: #2563EB;
    color: white;
    border: none;
    padding: 10px;
    font-weight: 600;
    transition: 0.2s;
}

.stButton button:hover {
    background-color: #1D4ED8;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #E5E7EB;
}
/* Sidebar headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #1D4ED8;
}

/* Research mode dropdown */
.stSelectbox div[data-baseweb="select"] {
    background-color: white !important;
    border-radius: 10px !important;
    border: 1px solid #D1D5DB !important;
}

/* Dropdown text */
.stSelectbox * {
    color: black !important;
}

/* Header area */
header {
    background-color: #F5F7FA !important;
}

/* Bottom area */
[data-testid="stBottomBlockContainer"] {
    background-color: #F5F7FA !important;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #C7CBD1;
    border-radius: 10px;
}
/* Smooth transitions */
* {
    transition: 0.2s ease;
}
/* Hover effect for chat bubbles */
[data-testid="stChatMessage"]:hover {
    transform: translateY(-2px);
}
/* Smooth animations */
* {
    transition: all 0.2s ease;
}

</style>
""", unsafe_allow_html=True)
# Sidebar
with st.sidebar:
    st.header("🧠 Nexus Tools")
    st.write("### Research Mode")
    st.divider()

    research_mode = st.selectbox(
        "Choose response style",
        [
            "Beginner Explanation",
            "Detailed Research",
            "Exam Preparation",
            "Technical Explanation"
        ]
    )

    st.write("### Suggested Topics")

    if st.button("Machine Learning"):
        st.session_state.suggested_prompt = "Explain Machine Learning in detail."

    if st.button("Deep Learning"):
        st.session_state.suggested_prompt = "Explain Deep Learning with examples."

    if st.button("Cloud Computing"):
        st.session_state.suggested_prompt = "What is Cloud Computing?"

    if st.button("Artificial Intelligence"):
        st.session_state.suggested_prompt = "Explain Artificial Intelligence."

    if st.button("Neural Networks"):
        st.session_state.suggested_prompt = "Explain Neural Networks clearly."


    # Clear broken old messages once
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# User input
user_input = st.chat_input("Ask anything about AI, research, technology, or academics...")

# Use suggested prompt if selected
if "suggested_prompt" in st.session_state:
    user_input = st.session_state.suggested_prompt
    del st.session_state.suggested_prompt




if not user_input:

    st.markdown("""
    ### 👋 Welcome to Nexus

    Ask questions about:
    - Machine Learning
    - Artificial Intelligence
    - Cloud Computing
    - Research Topics
    - Exam Preparation
    - Technical Concepts

    Use the sidebar to explore different response modes.
    """)

if user_input:

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })    

   
    # Generate AI response
    with st.spinner("AI is thinking..."):
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": f"""
    You are an advanced AI Research Assistant.

You MUST strictly follow the selected response mode.

Current Mode:
{research_mode}

========================

If the mode is "Beginner Explanation":

- Explain concepts like teaching a school student
- Use very simple language
- Keep answers short and intuitive
- Use real-world analogies
- Avoid technical jargon unless necessary
- Focus on understanding rather than detail

========================

If the mode is "Detailed Research":

- Provide detailed academic explanations
- Include multiple concepts and subtopics
- Structure answers with headings and bullet points
- Explain theory and applications
- Use moderate technical depth

========================

If the mode is "Exam Preparation":

- Give concise revision-style notes
- Use bullet points heavily
- Focus only on important concepts
- Include definitions and key points
- Keep answers short and easy to memorize

========================

If the mode is "Technical Explanation":

- Respond like an expert engineer/researcher
- Use technical terminology confidently
- Include deeper insights and advanced concepts
- Assume the user already knows fundamentals
- Focus on precision and technical accuracy

========================

General Rules:

- Keep formatting clean
- Avoid giant paragraphs
- Use headings when useful
- Stay educational and accurate
- Use proper markdown formatting
- Use ## for headings
- Use bullet points properly
- Keep responses visually clean
- Respond like a modern AI assistant, not a textbook
"""
            },
            
        ]+ st.session_state.messages[-6:]
    )

        

        ai_reply = completion.choices[0].message.content

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_reply
        })

    # Show AI response with typing effect
        with st.chat_message("assistant"):

            message_placeholder = st.empty()

            full_response = ""

            words = ai_reply.split(" ")

            for word in words:

                full_response += word + " "

                time.sleep(0.01)

                message_placeholder.markdown(full_response)

            message_placeholder.markdown(full_response)
            st.download_button(
                label="📋 Copy Response",
                data=full_response,
                file_name="response.txt",
                mime="text/plain"
            )

            
            st.markdown(
                "<center><sub>Built with ❤️ using Streamlit + Groq AI</sub></center>",
                unsafe_allow_html=True
            )
            