AI Tools Hub

Overview:
    AI Tools Hub is a unified platform providing multiple AI-powered tools including a chatbot, photo editor, and text-to-speech functionality.

Features:
    -)AI Chatbot powered by Google Gemini
    -)Advanced Photo Editing
    -)Text-to-Speech with Background Music
    -)User Activity Tracking

Prerequisites:
    -)Python 3.8+
    -)MongoDB
    -)API Keys:
        -)Google Gemini API
        -)Azure Cognitive Services
        -)ImageKit
        -)Freesound



Installation:
    1)Clone the repository
        git clone https://github.com/yourusername/ai-tools-hub.git
        cd ai-tools-hub
    2)Create virtual environment
        python -m venv venv
        source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    3)Install dependencies
        pip install -r requirements.txt
    4)Configure environment variables
        cp .env.example .env
        # Edit .env with your API keys
    5)Run the application
        streamlit run src/project.py

Configuration:
    Refer to .env.example for required environment variables

Testing:
    python -m pytest tests/

Contributing:
    -)Fork the repository
    -)Create your feature branch
    -)Commit changes
    -)Push to the branch
    -)Create pull request

