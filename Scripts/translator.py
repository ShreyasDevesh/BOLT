from deep_translator import GoogleTranslator
from nltk.tokenize import sent_tokenize

def translate_extracted(Extracted):
    """Wrapper for Google Translate with upload workaround."""
    # Set-up and wrap translation client
    translate = GoogleTranslator(source='auto', target='fr').translate
    # Split input text into a list of sentences
    sentences = sent_tokenize(Extracted)
    # Initialize containers
    translated_text = ''
    source_text_chunk = ''
    # collect chuncks of sentences, translate individually

    for sentence in sentences:
        # if chunck + current sentence < limit, add the sentence
        if ((len(sentence.encode('utf-8')) +  len(source_text_chunk.encode('utf-8')) < 5000)):
            source_text_chunk += ' ' + sentence
        # else translate chunck and start new one with current sentence
        else:
            translated_text += ' ' + translate(source_text_chunk)
            # if current sentence smaller than 5000 chars, start new chunck
            if (len(sentence.encode('utf-8')) < 5000):
                source_text_chunk = sentence
            # else, replace sentence with notification message
            else:
                message = "<<Omitted Word longer than 5000bytes>>"
                translated_text += ' ' + translate(message)
                # Re-set text container to empty
                source_text_chunk = ''

    # Translate the final chunk of input text, if there is any valid   text left to translate
    if translate(source_text_chunk) != None:
        translated_text += ' ' + translate(source_text_chunk)
    return translated_text
