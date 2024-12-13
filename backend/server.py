from flask import Flask, request, jsonify
from flask_cors import CORS
from visa import USCISVisaRAG  # Ensure this import matches where your USCISVisaRAG class is located

app = Flask(__name__)
CORS(app)  # Enable CORS for development purposes

# Initialize the chatbot instance
chatbot = USCISVisaRAG()

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat queries and return responses from the chatbot."""
    data = request.json
    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    response = chatbot.chat(query)
    return jsonify({'response': response})

@app.route('/add_document', methods=['POST'])
def add_document():
    """Add a new document to the chatbot's index."""
    data = request.json
    file_path = data.get('file_path', '')
    if not file_path:
        return jsonify({'error': 'No file path provided'}), 400
    try:
        chatbot.add_document(file_path)
        return jsonify({'message': 'Document added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear the chatbot's chat history."""
    chatbot.clear_history()
    return jsonify({'message': 'Chat history cleared'})

@app.route('/remove_all_documents', methods=['POST'])
def remove_all_documents():
    """Remove all documents from the chatbot's index."""
    chatbot.remove_all_documents()
    return jsonify({'message': 'All documents removed'})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
