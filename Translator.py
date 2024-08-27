from deep_translator import GoogleTranslator

translated = GoogleTranslator(source='ru', target='en').translate('Привет, как дела?')
print(translated)
