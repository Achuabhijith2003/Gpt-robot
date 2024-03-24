import os
import sys
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.indexes import VectorstoreIndexCreator

import constants

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Define the query
query = input("You:")

def Gptresponse(query):
    # Set OpenAI API key
    os.environ["OPENAI_API_KEY"] = constants.APIKEY

    # Define the data directory
    data_directory = 'E:\\Gpt-robot\\gptcode\\data\\data.txt'

    # Create a TextLoader to load data from a text file
    loader = TextLoader(data_directory)

    # Create a VectorstoreIndexCreator and load data using the loader
    index = VectorstoreIndexCreator().from_loaders([loader])

    # Query the index with ChatOpenAI model
    result = index.query(query, llm=ChatOpenAI())

    return result
