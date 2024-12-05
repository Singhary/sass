import streamlit as st
from streamlit_option_menu import option_menu
import os
from gemini_utilites import load_gemini_model
from gemini_utilites import image_captioning
from gemini_utilites import ask_me_anything
from PIL import Image

working_dir = os.path.dirname(os.path.abspath(__file__))

#setting up page configuration
st.set_page_config(page_title="SASS" , page_icon="📊", layout="centered", initial_sidebar_state="expanded")

with st.sidebar:
    selected = option_menu(menu_title="Features", options=["Chatbot" , "Image Captioning" , "Ask me anything"], menu_icon="🔥", icons=["chat-dots-fill","image-fill","patch-question-fill"] , default_index=0)

#iT JUST TRANSLATE the role for streamlit 
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role
    
if selected=='Chatbot':
    model = load_gemini_model()
    
    #Initilize the chat session in streamlit if not already present as model need to keep track of the conversation
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
        
    st.title("Chatbot 🤖")
    
    #now we will display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            print(message.parts[0].text)
            st.markdown(message.parts[0].text)
    
    #field for input message
    user_prompt = st.chat_input("Ask me anything...")
    
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        
        gemini_respone = st.session_state.chat_session.send_message(user_prompt)
        
        #displaying respone
        with st.chat_message("assistant"):
            st.markdown(gemini_respone.text)
            
elif selected=='Image Captioning':
    st.title("Image Captioning 🖼️")
    
    #field for image upload
    image = st.file_uploader("Upload an image" , type=["jpg","jpeg","png"])
    
    if st.button("Generate Caption"):
        
        image = Image.open(image)
        
        col1 , col2 = st.columns(2)
        
        with col1:
            resized_image = image.resize((800,500))
            st.image(resized_image)
            
        default_prompt = "Your a caption generator generate a caption for the provided image try to be creative"
        
        caption = image_captioning(default_prompt, image)
        
        with col2:
            st.info(caption)
            
elif selected=='Ask me anything':
    st.title("Ask me anything 🤔")
    
    user_prompt = st.text_area("Ask me anything...")
    
    if st.button("Generate Answer"):
        response = ask_me_anything(user_prompt)
        st.info(response)