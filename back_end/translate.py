import asyncio
from aiogoogletrans import Translator

translator = Translator()
base_lang = 'es'


async def translator_translate(word):
    result = await translator.translate(word, dest=base_lang, src='ru')  # Используем await здесь
    return result.text  # Возвращаем текст


async def main():
    while True:
        word = input('Введите текст для перевода или Enter: ')
        if not word:
            break

        # Ждем завершения корутины с переводом
        translated_text = await translator_translate(word)
        print(f'перевод: {translated_text}\n')

# Запускаем главный асинхронный цикл
asyncio.run(main())
