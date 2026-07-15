import streamlit as st

# Page config - must be first
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="💬",
    layout="wide"
)

# Import with error handling
try:
    from pipeline import ask_rag
except Exception as e:
    st.error(f"❌ Error importing pipeline: {e}")
    st.stop()

# Custom CSS for ChatGPT-like styling
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .main {
        background-color: #f7f7f8;
    }
    .stTextInput > div > div > input {
        border-radius: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("💬 RAG Chatbot")
    st.markdown("---")
    st.markdown("### About")
    st.info("Chat with your RAG-powered assistant. Ask questions about courses and get intelligent responses!")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Stats")
    st.metric("Messages", len(st.session_state.messages))
    
    st.markdown("---")
    st.caption("Built with LangChain & Streamlit")

# Main chat interface
st.title("💬 Course RAG Assistant")
st.caption("Ask me anything about courses!")

# Display chat history
if len(st.session_state.messages) == 0:
    # Show welcome message when no chat history
    st.info("👋 Welcome! I'm your course assistant. Type a question below to get started.")
    st.markdown("**Example questions:**")
    st.markdown("- What courses are available?")
    st.markdown("- Tell me about beginner courses")
    st.markdown("- What's the duration of [course name]?")
else:
    # Show chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about courses..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = ask_rag(prompt)
            st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
