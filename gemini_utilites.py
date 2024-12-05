import os
import json
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
working_dir = os.path.dirname(os.path.abspath(__file__))

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def load_gemini_model():
    return genai.GenerativeModel("gemini-1.5-pro")

#function for image captioning
def image_captioning(prompt , image):
    gemini_pro_vision_model = genai.GenerativeModel("gemini-1.5-flash-002")
    response = gemini_pro_vision_model.generate_content([prompt, image])
    result = response.text
    return result

#function for ask me anything
def ask_me_anything(prompt):
    gemini_pro_vision_model = genai.GenerativeModel("gemini-1.5-flash-002")
    response = gemini_pro_vision_model.generate_content([prompt])
    result = response.text
    return result