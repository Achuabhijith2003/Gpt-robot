import os
import sys

from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
import chromadb

import constants

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Directory path for data
DATA_DIRECTORY = "E:\\Gpt-robot\\gptcode\\data"

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

# Load data from the specified directory
loader = DirectoryLoader(DATA_DIRECTORY)

# Create or reuse the vectorstore index
if PERSIST and os.path.exists("persist"):
    print("Reusing index...\n")
    vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
    index = VectorstoreIndexCreator(vectorstore=vectorstore)
else:
    index = VectorstoreIndexCreator().from_loaders([loader])

# Create the conversational retrieval chain
# Define the ChatGPT conversational model
chatgpt_model = ChatOpenAI(model="gpt-3.5-turbo")

# Create the conversational retrieval chain with both models
chain = ConversationalRetrievalChain.from_llm(
    llm=chatgpt_model,
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []

# Main loop for conversation
while True:
    # Prompt the user for input
    query = input("Prompt: ") if not sys.argv[1:] else " ".join(sys.argv[1:])
    
    # Check if the user wants to quit
    if query.lower() in ['quit', 'q', 'exit']:
        print("Goodbye!")
        break
    
    # Retrieve response from the conversational retrieval chain
    result = chain({"question": query, "chat_history": chat_history})
    
    # Display the response
    print("Response:", result['answer'])
    
    # Append the query and response to the chat history
    chat_history.append((query, result['answer']))
