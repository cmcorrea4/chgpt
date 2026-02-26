import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Chat OpenAI", page_icon="💬", layout="centered")

st.title("💬 Chat con OpenAI")

# API Key input
api_key = st.text_input("🔑 OpenAI API Key", type="password", placeholder="sk-...")

# Model selector
model = st.selectbox("Modelo", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])

st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Escribe un mensaje..."):
    if not api_key:
        st.warning("Por favor ingresa tu API Key de OpenAI.")
        st.stop()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Call OpenAI
    client = OpenAI(api_key=api_key)
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=st.session_state.messages,
                )
                reply = response.choices[0].message.content
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")

# Clear button
if st.session_state.messages:
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.messages = []
        st.rerun()
