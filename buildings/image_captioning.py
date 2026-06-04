# buildings/image_captioning.py
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image
import torch
from googletrans import Translator

class ImageCaptioner:
    """
    Класс для генерации описаний изображений с переводом на русский
    """
    
    def __init__(self):
        print("🖼️ Загрузка модели для описания изображений...")
        self.model_name = "nlpconnect/vit-gpt2-image-captioning"
        self.processor = ViTImageProcessor.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = VisionEncoderDecoderModel.from_pretrained(self.model_name)
        self.model.eval()
        
        self.translator = Translator()
        print("Модель загружена!")
    
    def generate_caption(self, image_path, max_length=50):
        """
        Генерирует описание для изображения и переводит на русский
        """
        try:
            # Загружаем изображение
            image = Image.open(image_path).convert("RGB")
            
            # Подготавливаем изображение
            pixel_values = self.processor(images=image, return_tensors="pt").pixel_values
            
            # Генерируем описание на английском
            with torch.no_grad():
                output_ids = self.model.generate(
                    pixel_values,
                    max_length=max_length,
                    num_beams=4,
                    early_stopping=True
                )
            
            # Декодируем в текст
            caption_en = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            print(f"🇬🇧 Английский: {caption_en}")
            
            # Переводим на русский
            caption_ru = self.translator.translate(caption_en, dest='ru').text
            print(f"🇷🇺 Русский: {caption_ru}")
            
            return caption_ru
            
        except Exception as e:
            print(f"Ошибка при генерации описания: {e}")
            return "Не удалось сгенерировать описание изображения."

# Создаём глобальный экземпляр
captioner = None

def get_captioner():
    global captioner
    if captioner is None:
        captioner = ImageCaptioner()
    return captioner