# chatbot_basic_app.py  (optional page)

import streamlit as st
from components.chatbot_ui import global_chatbot  # ✅ updated import

def main():
    st.title("StreetBase ChatBot")
    st.write("Ask away your queries...")

    # ✅ Attach the global chatbot UI here
    global_chatbot()

if __name__ == "__main__":
    main()
