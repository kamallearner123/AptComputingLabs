#!/usr/bin/python3
# Install Module:
#  pip install googletrans==4.0.0-rc1


from googletrans import Translator

def translate_telugu_to_english(text):
    # Create a Translator object
    translator = Translator()

    # Detect the language of the input text
    detected_language = translator.detect(text).lang
    print(f"Detected Language: {detected_language}")

    # Translate from Telugu to English
    translated = translator.translate(text, src='te', dest='en')

    # Print the translated text
    print(f"Original (Telugu): {text}")
    print(f"Translated (English): {translated.text}")

# Example Telugu text
#telugu_text = "నాకు తెలుగులో అనువాదం కావాలి"
lines = ['''రోబోటిక్‌ యుగంలో రొటీన్‌గా చేసే అనేక ఉద్యోగాలు హుష్‌కాకి అవుతాయ్‌''',]
for line in lines:
    print("_"*100)
    translate_telugu_to_english(line)
    print("_"*100)

