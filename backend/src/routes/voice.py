import os
import base64
import tempfile
from flask import Blueprint, request, jsonify
import openai

voice_bp = Blueprint('voice', __name__)

# Initialize OpenAI client
def get_openai_client():
    """Get OpenAI client with proper error handling"""
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or len(api_key) < 20:
            return None
        return openai.OpenAI(api_key=api_key)
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        return None

@voice_bp.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """Transcribe audio using OpenAI Whisper"""
    try:
        data = request.get_json()
        if not data or 'audio' not in data:
            return jsonify({'error': 'No audio data provided'}), 400
        
        audio_data = data['audio']
        if not audio_data:
            return jsonify({'error': 'Empty audio data'}), 400
        
        client = get_openai_client()
        if not client:
            return jsonify({'error': 'OpenAI services not available'}), 500
        
        try:
            # Decode base64 audio data
            audio_bytes = base64.b64decode(audio_data)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_bytes)
                temp_file_path = temp_file.name
            
            try:
                # Transcribe using OpenAI Whisper
                with open(temp_file_path, 'rb') as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="text"
                    )
                
                # Clean up temporary file
                os.unlink(temp_file_path)
                
                return jsonify({
                    'success': True,
                    'transcription': transcript.strip()
                })
                
            except Exception as e:
                # Clean up on error
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                raise e
                
        except Exception as e:
            return jsonify({'error': f'Transcription failed: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Error processing audio: {str(e)}'}), 500

@voice_bp.route('/synthesize', methods=['POST'])
def synthesize_speech():
    """Synthesize speech using ElevenLabs or OpenAI TTS"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        # Try ElevenLabs first (if API key available)
        elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
        if elevenlabs_key and len(elevenlabs_key) > 10:
            try:
                audio_data = synthesize_with_elevenlabs(text, elevenlabs_key)
                if audio_data:
                    return jsonify({
                        'success': True,
                        'audio': audio_data,
                        'provider': 'elevenlabs'
                    })
            except Exception as e:
                print(f"ElevenLabs synthesis failed: {e}")
        
        # Fallback to OpenAI TTS
        client = get_openai_client()
        if not client:
            return jsonify({'error': 'No TTS services available'}), 500
        
        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )
            
            # Convert to base64
            audio_data = base64.b64encode(response.content).decode('utf-8')
            
            return jsonify({
                'success': True,
                'audio': audio_data,
                'provider': 'openai'
            })
            
        except Exception as e:
            # If OpenAI TTS fails, provide a fallback response
            return jsonify({
                'success': True,
                'audio': None,
                'provider': 'fallback',
                'message': 'Text-to-speech temporarily unavailable, but text response is ready'
            })
            
    except Exception as e:
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500

def synthesize_with_elevenlabs(text, api_key):
    """Synthesize speech using ElevenLabs API"""
    try:
        import requests
        
        url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"  # Default voice
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return base64.b64encode(response.content).decode('utf-8')
        else:
            print(f"ElevenLabs API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"ElevenLabs synthesis error: {e}")
        return None

@voice_bp.route('/test', methods=['GET'])
def test_voice_services():
    """Test voice services availability"""
    client = get_openai_client()
    elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
    
    services = {
        'whisper': client is not None,
        'openai_tts': client is not None,
        'elevenlabs': elevenlabs_key is not None and len(elevenlabs_key) > 10
    }
    
    return jsonify({
        'status': 'healthy',
        'services': services,
        'primary_tts': 'elevenlabs' if services['elevenlabs'] else 'openai',
        'fallback_available': True  # Always have text fallback
    })

