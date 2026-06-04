# buildings/tts_generator.py
from gtts import gTTS
import os
from django.conf import settings
from django.core.files import File

class AudioGenerator:
    """
    Класс для преобразования текста в аудио-гид (MP3)
    """
    
    def __init__(self):
        self.audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio_guides')
        # Создаём папку, если её нет
        os.makedirs(self.audio_dir, exist_ok=True)
    
    def text_to_audio(self, text, building_id, building_name):
        if not text or len(text) < 10:
            print(f"⚠️ Текст для '{building_name}' слишком короткий, аудио не создано")
            return None
        
        safe_name = "".join(c for c in building_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        
        filename = f"{safe_name}_{building_id}.mp3"
        filepath = os.path.join(self.audio_dir, filename)
        
        try:
            tts = gTTS(text=text, lang='ru', slow=False)
            tts.save(filepath)
            
            relative_path = f"audio_guides/{filename}"
            print(f"🎧 Аудиогид создан для '{building_name}': {filename}")
            return relative_path
            
        except Exception as e:
            print(f"❌ Ошибка создания аудио для '{building_name}': {e}")
            return None

# Глобальный экземпляр
audio_generator = None

def get_audio_generator():
    global audio_generator
    if audio_generator is None:
        audio_generator = AudioGenerator()
    return audio_generator