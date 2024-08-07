import google.generativeai as genai
from gtts import gTTS
import os
import pyttsx3
import speech_recognition as sr
import time
import sys
import datetime


# gemini respones method
def gpt_response(prompt):
  """Generates a response using the generativeai library with safety settings.

  Args:
      prompt: The user's input prompt for the chatbot.

  Returns:
      The response generated by the Gemini-1.0-pro model.
  """

  # API Key Configuration (Replace with your actual API key)
  API_KEY = "AIzaSyClZFTc5kyUjvJYf5AO7FgYYPRLkTF4eAM"
  genai.configure(api_key=API_KEY)

  # Model Configuration
  generation_config = {
      "temperature": 0.9,  # Controls randomness in responses
      "top_p": 1,          # Focuses generation on high probability tokens
      "top_k": 1,          # Limits considered tokens at each step
      "max_output_tokens": 2048,  # Maximum length of generated text
  }

  safety_settings = [
      {
          "category": "HARM_CATEGORY_HARASSMENT",
          "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
          "category": "HARM_CATEGORY_HATE_SPEECH",
          "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
          "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
          "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
          "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
          "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
  ]

  # Create the GenerativeModel Instance with Safety Measures
  model = genai.GenerativeModel(
      model_name="gemini-1.0-pro",
      generation_config=generation_config,
      safety_settings=safety_settings
  )

  # Start a Conversation (Optional for Multi-Turn Interactions)
  convo = model.start_chat(history=[])  # Empty history for new conversation

  # Send the User's Prompt and Return the Model's Response
  response = convo.send_message(prompt)
  print ("AI: ", response.text)
  text_to_speech(response.text)
  return response.text


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
    
def recognize_speech():
  """Continuously listens for user speech and responds with either the current time or a response from the AI model"""

  recognizer = sr.Recognizer()

  while True:
    # Listen for user input
    with sr.Microphone() as source:
      print("Speak something...")
      recognizer.adjust_for_ambient_noise(source)
      audio = recognizer.listen(source)

    try:
      # Recognize speech
      promt = recognizer.recognize_google(audio).lower()
      print("You said:", promt)

      # Check for time request
      if promt.lower() == "what time is it" or promt.lower() == "what's the time now":
  # Your code to tell the time

        now = datetime.datetime.now().strftime("%H:%M:%S")  # Get current time
        print("AI:", now)
        text_to_speech(now)  # Speak the current time
      else:
        gpt_response(promt)  # Call AI response function
    except sr.UnknownValueError:
      print("Sorry, could not understand audio")
    except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Rest of your code (main function etc.)


#main menthod
def main():
    print("AI assistant")

    while True:
    # Example Usage
        print("\n")
        recognize_speech()
       
        
        #main call
if __name__ == "__main__":
    main()
