import openai
from gtts import gTTS
import os
import pyttsx3
import speech_recognition as sr
import time
import sys
import os
import sys
#from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import ChatOpenAI

import constants

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = constants.APIKEY

#method for load data from data center
def load_data():
    # Define the data directory
    data_directory = 'E:\\Gpt-robot\\gptcode\\data\\data.txt'

    # Create a TextLoader to load data from a text file
    loader = TextLoader(data_directory)

    # Create a VectorstoreIndexCreator and load data using the loader
    index = VectorstoreIndexCreator().from_loaders([loader])
    return index


# method for generate response to promt
def Gptresponse(query,index):
    # Set OpenAI API key
    os.environ["OPENAI_API_KEY"] = constants.APIKEY
    
    # Query the index with ChatOpenAI model
    
    result = index.query(query, llm=ChatOpenAI())
    text_to_speech(result)
    print("AI:",result) 

def recognize_speech(index):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Speech Recognition
        promt = recognizer.recognize_google(audio)
        print("You said:", promt)
        # call the function 
        Gptresponse(promt,index)
        
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        pass
        
        
# Method for converting text to audio using Google Text-to-Speech (gTTS)
def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech (words per minute)
    engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

    # Convert text to speech
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()

# main function
def main():
    index=load_data()
    print("AI assistant")
    while True:
       recognize_speech(index)

if __name__ == "__main__":
    main()