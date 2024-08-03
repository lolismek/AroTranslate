import time
from utils import clean_text
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, NllbTokenizer
import ctranslate2
import razdel

model_load_name = '../models/ctranslate2_iter5-49999'

model = ctranslate2.Translator(model_load_name)
tokenizers = {
    'ron': AutoTokenizer.from_pretrained(model_load_name, src_lang = 'ron_Latn'),
    'rup': AutoTokenizer.from_pretrained(model_load_name, src_lang = 'rup_Latn')
}
print("LOADED MODEL AND TOKENIZERS!!!")

def translate_text(text, lang_from, lang_to):
    MAX_INPUT_TOKENS = 256
    BATCH_SIZE = 4
    MAX_OUTPUT_TOKENS = 50 # per sentence, TODO: adjust!


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

    print(len(Y))
    print(time.time() - start_time)
    return ' '.join(Y)

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
    if input_language == 'Romanian':
        lang_from = 'ron'
    elif input_language == 'Aromanian':
        lang_from = 'rup'

    if output_language == 'Romanian':
        lang_to = 'ron'
    elif output_language == 'Aromanian':
        lang_to = 'rup'

    translated_text = translate_text(input_text, lang_from, lang_to)

    # Return the translated text as JSON
    return jsonify({'translated_text': translated_text})

@app.route('/about')
def index2():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=82, host="0.0.0.0")