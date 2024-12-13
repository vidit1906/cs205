import os
from typing import List
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, ServiceContext, VectorStoreIndex, Document
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.llms.together import TogetherLLM
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.core.base.llms.types import ChatMessage

# Load the Together API key from the environment variables
load_dotenv()
api_key = os.getenv('TOGETHER_API_KEY')
print(f"API Key: {api_key}")

def completion_to_prompt(completion: str, query: str, context: List[ChatMessage]) -> str:
    print(f"Debug: completion={completion}, query={query}, context={context}")
    if "visa requirements" in query.lower():
        prompt = f"You are an expert on USCIS visa processes. Provide a detailed explanation for the following query:\n\n{query}\n\nConsider the following context:\n{completion}"
    elif "document" in query.lower():
        prompt = f"Given the context of USCIS documentation, please answer the following query:\n\n{query}\n\nUse the information provided:\n{completion}"
    else:
        prompt = f"Answer the following query related to USCIS visa procedures:\n\n{query}\n\nBase your response on the following information:\n{completion}"
    
    return prompt

# Rename the class to reflect its new purpose
class USCISVisaRAG:
    def __init__(
        self,
        document_dir: str = "./docs",  # Default directory for USCIS documents
        embedding_model: str = "togethercomputer/m2-bert-80M-8k-retrieval",
        generative_model: str = "meta-llama/Llama-3-8b-chat-hf"
    ):
        self.document_dir = document_dir
        self.service_context = ServiceContext.from_defaults(
            llm=TogetherLLM(
                generative_model,
                temperature=0.8,
                max_tokens=512,
                top_p=0.7,
                top_k=15,
                is_chat_model=True,
                completion_to_prompt=lambda completion, query: completion_to_prompt(completion, query, self.chat_history)
            ),
            embed_model=TogetherEmbedding(embedding_model, api_key=api_key)
        )
        
        self.index = self.load_documents()
        self.chat_engine = self.create_chat_engine()
        self.chat_history: List[ChatMessage] = []

    def load_documents(self):
        # Load USCIS documents from the specified directory
        documents = SimpleDirectoryReader(self.document_dir).load_data()
        print(f"Loaded documents: {documents}")
        return VectorStoreIndex.from_documents(documents, service_context=self.service_context)
        
    def add_document(self, file_path: str):
        # Add a new USCIS document to the index
        try:
            documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
            print(f"Documents to add: {documents}")
            if isinstance(documents, list):
                for doc in documents:
                    self.index.insert(doc)
            else:
                self.index.insert(documents)
            self.chat_engine = self.create_chat_engine()
            print(f"Document added successfully: {file_path}")
        except Exception as e:
            print(f"Error adding document: {str(e)}")
            raise

    def create_chat_engine(self):
        # Create a chat engine using the loaded USCIS documents
        return CondenseQuestionChatEngine.from_defaults(
            query_engine=self.index.as_query_engine(similarity_top_k=5),
            service_context=self.service_context,
            verbose=True
        )

    def chat(self, query: str) -> str:
        # Handle chat queries related to USCIS visa processes
        try:
            print(f"Debug: Query received: {query}")
            response = self.chat_engine.chat(query, chat_history=self.chat_history)
            print(f"Debug: Response received: {response}")
            self.chat_history.append(ChatMessage(role='user', content=query))
            self.chat_history.append(ChatMessage(role='assistant', content=str(response)))
            return str(response)
        except Exception as e:
            print(f"Error in chat method: {str(e)}")
            return "An error occurred. Please try again."

    def clear_history(self):
        # Clear chat history
        self.chat_history.clear()

    def remove_all_documents(self):
        # Clear the index and reinitialize the chat engine
        self.index = VectorStoreIndex([], service_context=self.service_context)
        self.chat_engine = self.create_chat_engine()
        self.clear_history()

def run_cli_chatbot():
    chatbot = USCISVisaRAG()

    print("Welcome to the USCIS Visa Chatbot! Type 'exit' to quit.")
    
    while True:
        query = input("You: ")
        if query.lower() == "exit":
            print("Goodbye!")
            break
        
        response = chatbot.chat(query)
        print(f"Chatbot: {response}\n")

if __name__ == "__main__":
    run_cli_chatbot()
