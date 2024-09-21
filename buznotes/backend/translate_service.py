from googletrans import Translator

translator = Translator()

def translate_text(text, target_language):
    translated = translator.translate(text, dest=target_language)
    return translated.text
