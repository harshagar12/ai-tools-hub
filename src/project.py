import streamlit as st
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import tempfile

# Import components
from components.chatbot import get_gemini_response
from components.photo_editor import PhotoEditor
from components.text_to_speech import TextToSpeechProcessor

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = "ai_tools_hub"

def init_db():
    """Initialize MongoDB connection"""
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    return db["user_history"]

def store_activity(collection, username, activity_type, details, output_url=None):
    """Store user activity in MongoDB"""
    timestamp = datetime.utcnow().isoformat()
    activity = {
        "username": username,
        "activity_type": activity_type,
        "details": details,
        "output_url": output_url,
        "timestamp": timestamp
    }
    collection.insert_one(activity)

def main():
    st.set_page_config(page_title="AI Tools Hub", layout="wide")
    
    # Initialize database
    collection = init_db()
    
    # Initialize components
    photo_editor = PhotoEditor()
    tts_processor = TextToSpeechProcessor()
    
    # Authentication check (simplified)
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if not st.session_state['logged_in']:
        st.title("Login")
        username = st.text_input("Enter Username")
        if st.button("Login"):
            if username:
                st.session_state['username'] = username
                st.session_state['logged_in'] = True
    
    if st.session_state.get('logged_in', False):
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox(
            "Choose a Tool",
            ["Chatbot", "Photo Editor", "Text to Speech"]
        )
        
        # Logout option
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.experimental_rerun()
        
        # Page routing
        if page == "Chatbot":
            st.title("AI Chatbot")
            user_input = st.text_input("Your message:")
            if st.button("Send"):
                response = get_gemini_response(user_input)
                store_activity(
                    collection, 
                    st.session_state['username'], 
                    "chat", 
                    {"user_message": user_input, "bot_response": response}
                )
                st.write(f"Bot: {response}")
        
        elif page == "Photo Editor":
            st.title("Photo Editor")
            uploaded_file = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])
            
            if uploaded_file:
                transformation = st.selectbox(
                    "Select transformation", 
                    ["Blur", "Grayscale", "Sepia", "Flip Horizontal", "Flip Vertical"]
                )
                
                if st.button("Transform"):
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                        tmp_file.write(uploaded_file.getbuffer())
                        tmp_path = tmp_file.name
                    
                    # Map Streamlit selection to component method
                    transform_map = {
                        "Blur": "blur",
                        "Grayscale": "grayscale",
                        "Sepia": "sepia",
                        "Flip Horizontal": "flip_horizontal",
                        "Flip Vertical": "flip_vertical"
                    }
                    
                    transformed_url = photo_editor.transform_image(
                        tmp_path, 
                        transform_map[transformation]
                    )
                    
                    if transformed_url:
                        st.image(transformed_url, caption="Transformed Image")
                        store_activity(
                            collection, 
                            st.session_state['username'], 
                            "photo_edit", 
                            {"transformation": transformation},
                            transformed_url
                        )
                    
                    # Clean up temporary file
                    os.unlink(tmp_path)
        
        elif page == "Text to Speech":
            st.title("Text to Speech")
            voices = tts_processor.get_available_voices()
            
            text = st.text_area("Enter text to convert:")
            selected_voice = st.selectbox(
                "Select Voice", 
                [voice[1] for voice in voices]
            )
            
            if st.button("Convert"):
                # Find full voice name
                full_voice = next(
                    voice[0] for voice in voices 
                    if voice[1] == selected_voice
                )
                
                # Generate speech
                speech_path = tts_processor.text_to_speech(text, full_voice)
                
                if speech_path:
                    st.audio(speech_path, format="audio/wav")
                    store_activity(
                        collection, 
                        st.session_state['username'], 
                        "text_to_speech", 
                        {"text": text, "voice": selected_voice}
                    )

if __name__ == "__main__":
    main()