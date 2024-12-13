import streamlit as st
from visa import USCISVisaRAG  # Replace with the actual module name

# Initialize the chatbot
chatbot = USCISVisaRAG()

def display_chat_history(chat_history):
    # Display each message in chat bubbles
    for message in chat_history:
        role = message['role']
        content = message['content']
        
        if role == 'user':
            st.markdown(
                f"""
                <div style="text-align: right; padding: 5px;">
                    <div style="display: inline-block; max-width: 70%; padding: 10px; border-radius: 15px; background-color: #DCF8C6;">
                        {content}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        elif role == 'assistant':
            st.markdown(
                f"""
                <div style="text-align: left; padding: 5px;">
                    <div style="display: inline-block; max-width: 70%; padding: 10px; border-radius: 15px; background-color: #FFFFFF; border: 1px solid #E1E1E1;">
                        {content}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

def main():
    st.title("USCIS Visa Chatbot")

    # Initialize session state for chat history if not already done
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Text input for user query
    user_input = st.text_input("You:", "")

    # Button to submit query
    if st.button("Send"):
        if user_input:
            # Get the response from the chatbot
            response = chatbot.chat(user_input)
            
            # Append to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": response})

            # Display the chat history
            display_chat_history(st.session_state.chat_history)

            # Clear user input field
            st.text_input("You:", "", key="input_field")
        else:
            st.write("Please enter a query.")

    # Optionally, add buttons to clear history and remove documents
    if st.button("Clear History"):
        st.session_state.chat_history = []
        chatbot.clear_history()
        st.write("Chat history cleared.")

    if st.button("Remove All Documents"):
        chatbot.remove_all_documents()
        st.write("All documents removed and chatbot reset.")

if __name__ == "__main__":
    main()
