import streamlit as st
import streamlit.components.v1 as components
from components.StreetBase_chatbot import init_bot, answer_query


def chatbot_popup():
    """
    Streamlit chat wired to the StreetBase bot.

    Behaviour:
    - NO auto-scroll on page load.
    - Auto-scroll ONLY when:
        → user sends a new message via st.chat_input.
    """

    # 1️⃣ One-time backend init
    if "chatbot_initialized" not in st.session_state:
        st.session_state.chunks, st.session_state.embeddings = init_bot()
        st.session_state.chat_history = []
        st.session_state.chatbot_initialized = True
        # ensure scroll flag starts clean
        st.session_state["_scroll_to_chat"] = False

    # Optional anchor (fallback target if no chat messages)
    st.markdown('<div id="streetbase-chat-anchor"></div>', unsafe_allow_html=True)

    # 2️⃣ Render existing chat history
    for sender, msg in st.session_state.chat_history:
        role = "user" if sender == "user" else "assistant"
        st.chat_message(role).markdown(msg)

    # 3️⃣ Chat input at bottom
    user_query = st.chat_input("Ask StreetBase anything...")

    if user_query:
        # Show user message
        st.chat_message("user").markdown(user_query)
        st.session_state.chat_history.append(("user", user_query))

        # Get bot reply
        reply = answer_query(
            user_query,
            st.session_state.chunks,
            st.session_state.embeddings,
        )

        st.chat_message("assistant").markdown(reply)
        st.session_state.chat_history.append(("assistant", reply))

        # 👉 Trigger scroll because a new exchange was added
        st.session_state["_scroll_to_chat"] = True

    # 4️⃣ Auto-scroll ONLY when a new message was just sent
    if st.session_state.get("_scroll_to_chat", False):

        # Reset immediately so it doesn't keep scrolling on future reruns
        st.session_state["_scroll_to_chat"] = False

        components.html(
            """
            <script>
            const streamlitDoc = window.parent.document;

            // Try to scroll to the last chat message
            const msgs = streamlitDoc.querySelectorAll('div[data-testid="stChatMessage"]');
            if (msgs.length > 0) {
                const lastMsg = msgs[msgs.length - 1];
                lastMsg.scrollIntoView({ behavior: "smooth", block: "end" });
            } else {
                // Fallback: scroll to our anchor
                const anchor = streamlitDoc.getElementById("streetbase-chat-anchor");
                if (anchor) {
                    anchor.scrollIntoView({ behavior: "smooth", block: "end" });
                }
            }
            </script>
            """,
            height=0,
            width=0,
        )
