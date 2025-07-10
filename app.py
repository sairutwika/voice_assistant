# app.py

import streamlit as st
from assistant import listen, process_command
import os

# ----------------- Page Config ------------------
st.set_page_config(page_title="Baby Siri", layout="centered")

# ----------------- Custom Styling ------------------
st.markdown("""
<style>
/* Background */
.stApp {
    background-image: url('https://images.unsplash.com/photo-1607082349566-c6f5c7aa5e86?auto=format&fit=crop&w=1350&q=80');
    background-size: cover;
    background-attachment: fixed;
    font-family: 'Segoe UI', sans-serif;
    color: #ffffff;
}

/* Headings */
h1, h2, h3 {
    text-align: center;
    color: #ffffff;
    font-weight: bold;
    text-shadow: 1px 1px 4px #000000;
}

/* Buttons */
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 16px;
    transition: all 0.3s ease-in-out;
    box-shadow: 1px 1px 6px black;
}

.stButton>button:hover {
    background-color: #ff7777;
    transform: scale(1.03);
}

/* Text input box */
input[type="text"] {
    background-color: skyblue;
    color: #fff !important;
    border: 2px solid #ffffff50;
    border-radius: 10px;
    padding: 10px;
}

/* Chat bubbles */
div[data-testid="stMarkdownContainer"] p {
    background-color: rgba(0,0,0,0.4);
    padding: 10px 15px;
    border-radius: 12px;
    font-size: 16px;
    margin-bottom: 8px;
    color: #ffffff;
    text-shadow: 1px 1px 2px #000;
}

/* Toasts */
.stToast {
    color: white;
}
</style>
""", unsafe_allow_html=True)


# ----------------- Sidebar Settings ------------------
with st.sidebar:
    st.header("⚙️ Settings")
    voice_type = st.selectbox("Choose Voice", ["Female", "Male"])
    input_mode = st.radio("Input Mode", ["🎙️ Voice", "⌨️ Type"])

# ----------------- Session State ------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ----------------- Title ------------------
st.title("🤖 Baby Siri - Your Voice Assistant")
st.markdown("### 🎙️ Ask me anything by voice or text")

# ----------------- Main Interaction ------------------
if input_mode == "🎙️ Voice":
    if st.button("🎤 Tap to Talk"):
        with st.spinner("🎧 Listening..."):
            command = listen()

        st.toast("🗣️ Heard you!", icon="🎙️")
        st.success(f"🗣️ You said: {command}")

        with st.spinner("🤖 Thinking..."):
            response = process_command(command)
        st.toast("✅ Siri replied", icon="✅")

        st.session_state.history.append((command, response))

elif input_mode == "⌨️ Type":
    command = st.text_input("Type your question and press Enter")
    if command:
        response = process_command(command)
        st.session_state.history.append((command, response))
        st.success(f"🤖 Siri: {response}")

# ----------------- Chat History ------------------
st.markdown("### 📝 Conversation History")
if st.session_state.history:
    for user, bot in reversed(st.session_state.history):
        st.markdown(f"🗣️ **You**: {user}")
        st.markdown(f"🤖 **Siri**: {bot}")
else:
    st.info("No conversations yet. Ask something!")

# ----------------- Show Notes ------------------
if os.path.exists("notes.txt"):
    if st.button("📒 Show My Notes"):
        with open("notes.txt", "r") as f:
            notes = f.readlines()
        st.markdown("### 📓 Your Last 5 Notes")
        for note in notes[-5:]:
            st.markdown(f"- {note}")
