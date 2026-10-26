import streamlit as st
from answer import answer_question

# Configure the webpage
st.set_page_config(
    page_title="My RAG Study Assistant",
    page_icon="📚",
)

# Display the title
st.title("📚 My RAG Study Assistant")
st.write("Ask questions about your indexed study materials.")

# Store chat history during the session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Show the question input box
question = st.chat_input("Ask a question about your notes or PDF...")

if question:
    # Display and save the user's question
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Generate and display the answer
    with st.chat_message("assistant"):
        with st.spinner("Searching your study materials..."):
            try:
                answer = answer_question(question)
                st.markdown(answer)

            except Exception as error:
                answer = f"Something went wrong: {error}"
                st.error(answer)

    # Save the answer in chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
