import time
from utils import clean_text, post_process
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, NllbTokenizer
import ctranslate2
import razdel
from utils_diacritics import cunia_to_diaro, diaro_to_cunia

model_load_name = "NLLB-rup-ron-eng-ct2-v2"

model = ctranslate2.Translator(model_load_name)
tokenizers = {
    'ron': AutoTokenizer.from_pretrained(model_load_name, src_lang = 'ron_Latn'),
    'rup': AutoTokenizer.from_pretrained(model_load_name, src_lang = 'rup_Latn'),
    'eng': AutoTokenizer.from_pretrained(model_load_name, src_lang = 'eng_Latn')
}
print("LOADED MODEL AND TOKENIZERS!!!")

def translate_text(text, lang_from, lang_to):
    MAX_INPUT_TOKENS = 1024
    BATCH_SIZE = 4
    MAX_OUTPUT_TOKENS = 1024 # per sentence, TODO: adjust!


    text = clean_text(text, lang_from)
    sents = [s.text for s in razdel.sentenize(text)]

    
    if len(tokenizers[lang_from].tokenize(text)) > MAX_INPUT_TOKENS:
        return "Text is too long (Tokenizer limit excedeed)"

   
    sents_batches = []
    for i in range(0, len(sents), BATCH_SIZE):
        sents_batches.append(sents[i:i+BATCH_SIZE])
    
    # do some check and stuff ...

    start_time = time.time()
    Y = []
    for batch in sents_batches:
        X = tokenizers[lang_from](batch, truncation=True)
        source = [tokenizers[lang_from].convert_ids_to_tokens(p) for p in X['input_ids']]
        target_prefix = [lang_to + '_Latn']
        results = model.translate_batch(source, max_decoding_length=MAX_OUTPUT_TOKENS, target_prefix=[target_prefix for _ in range(len(source))])
    
        Y.extend([tokenizers[lang_from].decode(tokenizers[lang_from].convert_tokens_to_ids(results[_].hypotheses[0][1:])) for _ in range(len(results))])
    total_time = time.time() - start_time

    return ' '.join(Y), total_time

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    # Get JSON data from the request
    data = request.get_json()

    # Extract input values
    input_text = data.get('input_text', '')
    input_language = data.get('input_language', '').strip()
    output_language = data.get('output_language', '').strip()

    # Validate inputs
    if not input_text or not input_language or not output_language:
        return jsonify({'error': 'Invalid input'}), 400

    lang_from, lang_to = '', ''
    if input_language == 'Romanian' or input_language == 'Română' or input_language == 'Romãnã':
        lang_from = 'ron'
    elif input_language == 'Aromanian' or input_language == 'Aromână' or input_language == 'Armãnã':
        lang_from = 'rup'
    elif input_language == "English" or input_language == "Engleză" or input_language == "Inglezã":
        lang_from = 'eng'

    if output_language == 'Romanian' or output_language == 'Română' or output_language == 'Romãnã':
        lang_to = 'ron'
    elif output_language == 'Aromanian' or output_language == 'Aromână' or output_language == 'Armãnã':
        lang_to = 'rup'
    elif output_language == "English" or output_language == "Engleză" or output_language == "Inglezã":
        lang_to = 'eng'

    translated_text, translate_time = translate_text(input_text, lang_from, lang_to)
    translated_text = post_process(translated_text)

    # Return the translated text as JSON
    return jsonify({'translated_text': translated_text, 'translate_time': str(round(translate_time, 5))   })

@app.route('/diacritics', methods=['POST'])
def convert_diacritics():
    data = request.get_json()

    init_graf = data.get('init_graf', '').strip()
    text = data.get('text', '').strip()

    if init_graf == "cunia":
        return jsonify({'text': cunia_to_diaro(text)})
    return jsonify({'text': diaro_to_cunia(text)})

@app.route('/about')
def index2():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=82, host="0.0.0.0")