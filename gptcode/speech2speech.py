import openai
from gtts import gTTS
import os
import pyttsx3
import speech_recognition as sr
import time
import sys

# Set your OpenAI API key
api_key = "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"
openai.api_key = api_key

# method for generate response to promt
def Gptrespones(promt):
    # Call the OpenAI API to generate text
    response = openai.Completion.create(
        engine="davinci-002",  # Specify the GPT model to use
        prompt=promt,
        max_tokens=500,  # Adjust as needed, controls the length of the response
        temperature=0.9,  # Set to 0 for deterministic output
        top_p=1.0,  # Ensure the generated text is from the top choice
        stop=None
    )
    print("AI:",response.choices[0].text.strip()) # print the response
    text_to_speech(response.choices[0].text.strip())    

def recognize_speech():
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
        Gptrespones(promt)
        
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
    print("AI assistant")

    while True:
       recognize_speech()

if __name__ == "__main__":
    main()