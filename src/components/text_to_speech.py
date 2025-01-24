import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
from pydub import AudioSegment
import requests
import tempfile

load_dotenv()

class TextToSpeechProcessor:
    def __init__(self):
        """Initialize Azure Speech configuration"""
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.speech_region = os.getenv("AZURE_SPEECH_REGION")
        self.freesound_api_key = os.getenv("FREESOUND_API_KEY")
    
    def get_available_voices(self):
        """Retrieve available English voices"""
        speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, 
            region=self.speech_region
        )
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        voices_result = synthesizer.get_voices_async().get()
        
        if voices_result.reason == speechsdk.ResultReason.VoicesListRetrieved:
            return [
                (voice.short_name, voice.short_name.split('-')[-1])
                for voice in voices_result.voices 
                if voice.locale.startswith('en')
            ]
        return []
    
    def text_to_speech(self, text, voice):
        """Convert text to speech audio"""
        speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, 
            region=self.speech_region
        )
        speech_config.speech_synthesis_voice_name = voice
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_file.name)
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config, 
                audio_config=audio_config
            )
            
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return temp_file.name
        
        return None
    
    def search_background_music(self, query):
        """Search for background music using Freesound API"""
        headers = {'Authorization': f'Token {self.freesound_api_key}'}
        params = {
            'query': query,
            'filter': 'duration:[1 TO 60]',
            'fields': 'id,name,duration,previews',
            'page_size': 5
        }
        
        try:
            response = requests.get(
                'https://freesound.org/apiv2/search/text/',
                headers=headers,
                params=params
            )
            response.raise_for_status()
            results = response.json().get('results', [])
            return [
                result for result in results 
                if 'previews' in result and 'preview-hq-mp3' in result['previews']
            ]
        except Exception as e:
            print(f"Music search error: {str(e)}")
            return []
    
    def mix_audio(self, speech_path, background_music, output_path='final_output.wav'):
        """Mix speech audio with background music"""
        try:
            speech = AudioSegment.from_wav(speech_path)
            background = AudioSegment.from_mp3(background_music)
            
            # Loop background music if shorter than speech
            while len(background) < len(speech):
                background += background
            
            background = background[:len(speech)]
            final_audio = background.overlay(speech)
            
            final_audio.export(output_path, format='wav')
            return output_path
        
        except Exception as e:
            print(f"Audio mixing error: {str(e)}")
            return None